# Alberta Flash Cards

Flash cards for Alberta Grade 9-12 Math, Science, Social Studies and ELA (about 12,000 cards, at least 100 per unit).

## On a computer: make printable PDFs or study on screen
- **Windows:** double-click `run.bat`
- **Mac:** run `chmod +x run.command` once, then double-click `run.command`

A page opens where you pick grade, subject, course, unit and number of cards, then click **Create PDF** or **Study on screen**.

## On a phone: offline web app
The `docs/` folder is a phone-friendly web app (installable, works offline) that uses the same cards.

**One-time publish on GitHub Pages**
1. On GitHub, open the repo, then **Settings -> Pages**.
2. Under **Build and deployment**, set **Source** to *Deploy from a branch*.
3. Choose branch **main** and folder **/docs**, then **Save**.
4. After a minute the site is live at `https://<your-github-name>.github.io/FlashCards/`.

**On the Android phone**
1. Open that link in Chrome (internet needed this first time only).
2. Tap the Chrome menu, then **Add to Home screen** (or **Install app**).
3. It now opens like an app and works with no internet. Cards you mark "Got it" are remembered on that phone.

## Adding or editing cards
Cards live in `cards/*.txt`, one per line as `question :: answer`, under a heading like `## Mathematics 20-1 | Trigonometry`.
Use `## English Language Arts * | Poetry` to share cards across every ELA course.

After changing cards, rebuild the phone app and push:
```
python build_web.py
git add -A && git commit -m "Update cards" && git push
```
The phone picks up the update the next time it opens the app with internet.
