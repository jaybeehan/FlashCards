"""Alberta flash card maker (fully offline, no API key).

Run it (via run.bat / run.command). A web page opens: pick grade / subject / course / unit /
number of cards and a printable PDF is downloaded.

Cards live in the cards/*.txt files (see the format note at the top of cards/math.txt).
Add more cards there at any time - they show up automatically.
"""
import io
import json
import random
import threading
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs
from xml.sax.saxutils import escape

from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph

from curriculum import ALL_UNITS, CORE_LABEL, CORE_SUBJECTS, CURRICULUM

HOST, PORT = "127.0.0.1", 8765
MAX_CARDS = 500
CARD_DIR = Path(__file__).parent / "cards"


# ---------------------------------------------------------------- card bank
def all_courses():
    return [c for g in CURRICULUM.values() for subj in g.values() for c in subj]


def load_bank():
    """Return {(course, unit): [(front, back), ...]} from cards/*.txt."""
    courses = all_courses()
    bank = {}
    for path in sorted(CARD_DIR.glob("*.txt")):
        targets = []
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#") and not line.startswith("##"):
                continue
            if line.startswith("##"):
                names, unit = [s.strip() for s in line[2:].split("|", 1)]
                targets = []
                for name in names.split(","):
                    name = name.strip()
                    if name.endswith("*"):  # wildcard: every course with this prefix
                        targets += [(c, unit) for c in courses if c.startswith(name[:-1])]
                    else:
                        targets.append((name, unit))
            elif " :: " in line and targets:
                front, back = (s.strip() for s in line.split(" :: ", 1))
                for key in targets:
                    cards = bank.setdefault(key, [])
                    if all(front.lower() != f.lower() for f, _ in cards):  # skip duplicate questions
                        cards.append((front, back))
    return bank


BANK = load_bank()


def pools_for(grade, subject, course, unit):
    """List of (label, cards) pools for a selection."""
    if subject == CORE_LABEL:
        courses = [c for s in CORE_SUBJECTS for c in CURRICULUM[grade][s]]
        units = [(c, u) for c in courses for u in unit_names(grade, c)]
    elif unit == ALL_UNITS:
        units = [(course, u) for u in unit_names(grade, course)]
    else:
        units = [(course, unit)]
    return [(f"{c} · {u}", BANK.get((c, u), [])) for c, u in units]


def unit_names(grade, course):
    for subj in CURRICULUM[grade].values():
        if course in subj:
            return subj[course]
    return []


def pick_cards(pools, count):
    """Round-robin across pools so every unit is represented; returns up to `count` cards."""
    pools = [(label, random.sample(cards, len(cards))) for label, cards in pools if cards]
    out, seen = [], set()
    while pools and len(out) < count:
        for pool in list(pools):
            label, cards = pool
            front, back = cards.pop(0)
            if front not in seen:  # ELA courses share cards, so skip repeats in mixed decks
                seen.add(front)
                out.append({"front": front, "back": back, "label": label})
            if not cards:
                pools.remove(pool)
            if len(out) >= count:
                break
    random.shuffle(out)
    return out


# ---------------------------------------------------------------- PDF
COLS, ROWS = 2, 4
CW, CH = 4.0 * inch, 2.5 * inch
MX, MY = (letter[0] - COLS * CW) / 2, (letter[1] - ROWS * CH) / 2
PER_PAGE = COLS * ROWS


def fit_paragraph(text, width, height, color, max_size=18, min_size=7):
    size = max_size
    while True:
        style = ParagraphStyle("c", fontName="Helvetica", fontSize=size, leading=size * 1.25,
                               alignment=1, textColor=color)
        p = Paragraph(escape(text), style)
        _, h = p.wrap(width, height)
        if h <= height or size <= min_size:
            return p, h
        size -= 1


def draw_card(c, x, y, text, label, number, color, tint):
    c.setFillColor(tint)
    c.rect(x, y, CW, CH, stroke=0, fill=1)
    c.setStrokeColor(HexColor("#999999"))
    c.setDash(3, 3)
    c.rect(x, y, CW, CH, stroke=1, fill=0)
    c.setDash()
    c.setFillColor(HexColor("#666666"))
    c.setFont("Helvetica", 7.5)
    c.drawString(x + 10, y + CH - 14, label[:70])
    c.drawRightString(x + CW - 10, y + 8, f"#{number}")
    pad = 18
    p, h = fit_paragraph(text, CW - 2 * pad, CH - 2 * pad - 10, color)
    p.drawOn(c, x + pad, y + (CH - h) / 2 - 2)


def make_pdf(cards, title):
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=letter)
    c.setTitle(title)
    dark = HexColor("#111111")
    for start in range(0, len(cards), PER_PAGE):
        page = cards[start:start + PER_PAGE]
        for side in ("front", "back"):
            for i, card in enumerate(page):
                col, row = i % COLS, i // COLS
                if side == "back":  # mirror columns so it lines up when printed double-sided (long edge)
                    col = COLS - 1 - col
                x = MX + col * CW
                y = letter[1] - MY - (row + 1) * CH
                if side == "front":
                    draw_card(c, x, y, card["front"], card["label"], start + i + 1, dark, HexColor("#ffffff"))
                else:
                    draw_card(c, x, y, card["back"], "Answer", start + i + 1, dark, HexColor("#eef4ff"))
            c.showPage()
    c.save()
    return buf.getvalue()


# ---------------------------------------------------------------- web page
PAGE = """<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>Alberta Flash Cards</title>
<style>
body{font-family:system-ui,sans-serif;max-width:520px;margin:2rem auto;padding:0 1rem;color:#222}
label{display:block;margin-top:1rem;font-weight:600}
select,input{width:100%;padding:.55rem;margin-top:.3rem;font-size:1rem;box-sizing:border-box}
button{margin-top:1.5rem;padding:.8rem;width:100%;font-size:1.05rem;background:#0b5fff;color:#fff;border:0;border-radius:6px;cursor:pointer}
button:disabled{background:#889}
button.alt{background:#fff;color:#0b5fff;border:2px solid #0b5fff;margin-top:.7rem}
button.small{width:auto;margin:0;padding:.4rem .9rem;font-size:.9rem}
button.ok{background:#1a8f4c}button.warn{background:#c2410c}
.bar{display:flex;justify-content:space-between;align-items:center;margin-bottom:1rem}
.row{display:flex;gap:.8rem}.row button{flex:1}
#card{margin-top:.5rem;min-height:14rem;border:2px solid #999;border-radius:12px;padding:1.2rem;display:flex;flex-direction:column;
justify-content:space-between;align-items:center;text-align:center;cursor:pointer;background:#fff;user-select:none}
#card.back{background:#eef4ff;border-color:#0b5fff}#ctext{font-size:1.4rem;line-height:1.4;margin:1rem 0}small{color:#666;font-weight:400}#msg{margin-top:1rem}
</style></head><body>
<h1>Alberta Flash Cards</h1>
<form id="f">
<label>Grade<select name="grade" id="grade"></select></label>
<label>Subject<select name="subject" id="subject"></select></label>
<label>Course<select name="course" id="course"></select></label>
<label>Unit<select name="unit" id="unit"></select></label>
<label>Number of cards <small id="avail"></small><input type="number" name="count" id="count" min="1" value="20" required></label>
<button id="go">Create PDF</button>
<button id="studybtn" type="button" class="alt">Study on screen</button><div id="msg"></div>
</form>
<div id="study" hidden>
<div class="bar"><span id="prog"></span><button type="button" id="exit" class="alt small">Back</button></div>
<div id="card" tabindex="0"><small id="clabel"></small><div id="ctext"></div><small id="hint">click the card to flip</small></div>
<div class="row"><button type="button" id="again" class="warn">Review again</button><button type="button" id="know" class="ok">Got it</button></div>
<div class="row"><button type="button" id="shuf" class="alt">Shuffle remaining</button></div>
<small>Keys: Space = flip, Left arrow = review again, Right arrow = got it</small>
</div>
<script>
const C=__DATA__, N=__COUNTS__, CORE="__CORE__", ALL="__ALL__", COREN=__COREN__;
const $=id=>document.getElementById(id);
const fill=(el,items)=>{el.innerHTML=items.map(v=>`<option>${v}</option>`).join('')};
const n=(c,u)=>N[c+'|'+u]||0;
function avail(){
  const g=$('grade').value,s=$('subject').value,c=$('course').value,u=$('unit').value;
  if(s===CORE)return COREN[g]||0;
  const units=C[g][s][c];
  return u===ALL?units.reduce((a,x)=>a+n(c,x),0):n(c,u)}
function update(){const a=avail();$('avail').textContent='('+a+' available)';$('count').max=Math.max(a,1);
  if(+$('count').value>a)$('count').value=Math.max(a,1)}
function onGrade(){fill($('subject'),[CORE,...Object.keys(C[$('grade').value])]);onSubject()}
function onSubject(){
  const g=$('grade').value,s=$('subject').value;
  if(s===CORE){fill($('course'),['All core courses']);fill($('unit'),[ALL]);update();return}
  fill($('course'),Object.keys(C[g][s]));onCourse()}
function onCourse(){
  const g=$('grade').value,s=$('subject').value;
  if(s!==CORE)fill($('unit'),[ALL,...C[g][s][$('course').value]]);update()}
fill($('grade'),Object.keys(C));
$('grade').onchange=onGrade;$('subject').onchange=onSubject;$('course').onchange=onCourse;$('unit').onchange=update;onGrade();
$('f').onsubmit=async e=>{
  e.preventDefault();$('go').disabled=true;$('msg').textContent='Making your PDF...';
  try{
    const r=await fetch('/generate',{method:'POST',body:new URLSearchParams(new FormData($('f')))});
    if(!r.ok)throw new Error(await r.text());
    const made=r.headers.get('X-Cards-Made');
    const a=document.createElement('a');a.href=URL.createObjectURL(await r.blob());
    a.download='flashcards.pdf';a.click();$('msg').textContent='Done: '+made+' cards - check your downloads.';
  }catch(err){$('msg').textContent='Error: '+err.message}
  $('go').disabled=false};

let queue=[],total=0,known=0,showBack=false;
const show=()=>{
  if(!queue.length){$('card').className='';$('clabel').textContent='';$('ctext').textContent='All '+total+' cards learned - nice work!';
    $('hint').textContent='';$('prog').textContent=total+' / '+total+' learned';return}
  const c=queue[0];$('card').className=showBack?'back':'';$('clabel').textContent=showBack?'Answer':c.label;
  $('ctext').textContent=showBack?c.back:c.front;$('hint').textContent=showBack?'':'click the card to flip';
  $('prog').textContent=known+' / '+total+' learned, '+queue.length+' to go'};
const next=gotIt=>{if(!queue.length)return;const c=queue.shift();if(gotIt)known++;else queue.push(c);showBack=false;show()};
$('card').onclick=()=>{if(queue.length){showBack=!showBack;show()}};
$('know').onclick=()=>next(true);$('again').onclick=()=>next(false);
$('shuf').onclick=()=>{queue.sort(()=>Math.random()-.5);showBack=false;show()};
$('exit').onclick=()=>{$('study').hidden=true;$('f').hidden=false};
document.onkeydown=e=>{if($('study').hidden)return;
  if(e.key===' '){e.preventDefault();$('card').onclick()}else if(e.key==='ArrowRight')next(true);else if(e.key==='ArrowLeft')next(false)};
$('studybtn').onclick=async()=>{
  $('msg').textContent='Loading cards...';
  try{
    const r=await fetch('/cards',{method:'POST',body:new URLSearchParams(new FormData($('f')))});
    if(!r.ok)throw new Error(await r.text());
    queue=await r.json();total=queue.length;known=0;showBack=false;
    $('msg').textContent='';$('f').hidden=true;$('study').hidden=false;show();
  }catch(err){$('msg').textContent='Error: '+err.message}};
</script></body></html>"""


def page_html():
    counts = {f"{c}|{u}": len(v) for (c, u), v in BANK.items()}
    core_n = {g: sum(len(BANK.get((c, u), [])) for s in CORE_SUBJECTS for c, units in subs[s].items() for u in units)
              for g, subs in CURRICULUM.items()}
    return (PAGE.replace("__DATA__", json.dumps(CURRICULUM)).replace("__COUNTS__", json.dumps(counts))
            .replace("__COREN__", json.dumps(core_n)).replace("__CORE__", CORE_LABEL)
            .replace("__ALL__", ALL_UNITS))


class Handler(BaseHTTPRequestHandler):
    def _send(self, code, ctype, body, extra=None):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        for k, v in (extra or {}).items():
            self.send_header(k, v)
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        self._send(200, "text/html; charset=utf-8", page_html().encode())

    def _selection(self):
        form = parse_qs(self.rfile.read(int(self.headers["Content-Length"])).decode())
        get = lambda k: form.get(k, [""])[0].strip()
        grade, subject, course, unit = get("grade"), get("subject"), get("course"), get("unit")
        count = max(1, min(MAX_CARDS, int(get("count") or 20)))
        if grade not in CURRICULUM:
            raise RuntimeError("Unknown grade.")
        if subject != CORE_LABEL:
            if course not in CURRICULUM[grade].get(subject, {}):
                raise RuntimeError("Unknown course for that grade/subject.")
            if unit != ALL_UNITS and unit not in CURRICULUM[grade][subject][course]:
                raise RuntimeError("Unknown unit.")
        cards = pick_cards(pools_for(grade, subject, course, unit), count)
        if not cards:
            raise RuntimeError("No cards in the bank for that selection yet (add some to the cards folder).")
        return cards, f"Grade {grade} {subject} flash cards"

    def do_POST(self):
        try:
            cards, title = self._selection()
            if self.path == "/cards":
                self._send(200, "application/json", json.dumps(cards).encode())
            else:
                self._send(200, "application/pdf", make_pdf(cards, title),
                           {"Content-Disposition": 'attachment; filename="flashcards.pdf"',
                            "X-Cards-Made": str(len(cards))})
        except Exception as e:  # shown in the page
            self._send(500, "text/plain; charset=utf-8", str(e).encode())

    def log_message(self, *args):
        pass


def main():
    server = ThreadingHTTPServer((HOST, PORT), Handler)
    url = f"http://{HOST}:{PORT}/"
    print(f"Flash card maker running at {url}  (Ctrl+C to stop)")
    threading.Timer(0.8, lambda: webbrowser.open(url)).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
