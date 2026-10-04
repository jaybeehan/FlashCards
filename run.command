#!/bin/bash
# macOS launcher. First time only: chmod +x run.command   (then double-click it)
cd "$(dirname "$0")"
if ! command -v python3 >/dev/null; then
    echo "Python 3 is not installed. Get it from https://www.python.org/downloads/"
    exit 1
fi
if [ ! -d .venv ]; then
    python3 -m venv .venv
    .venv/bin/python -m pip install -q -r requirements.txt
fi
.venv/bin/python flashcards.py
