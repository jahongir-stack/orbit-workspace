# PyCert Academy — PCEP & PCAP Practice Website

A responsive Python/Flask learning website for entry-level and associate-level Python certification preparation.

## Features
- PCEP, PCAP, and mixed practice modes
- 12 original multiple-choice exercises
- Server-side answer checking with explanations
- Progress bar, score summary, and restart button
- Responsive dark theme and mobile layout
- No login or database required

## Run locally

```bash
cd pcep-pcap-academy
python -m pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:5000 in your browser.

## API
- `GET /api/questions?level=PCEP|PCAP|ALL`
- `POST /api/check` with JSON `{"id": 1, "choice": 0}`

## Notes
Practice questions are illustrative and not taken from official exams. This project is independent and not affiliated with Python Institute or OpenEDG. A quiz result does not guarantee certification success.

## Development ideas
Add more questions, category-specific drills, user accounts, spaced repetition, accessibility tests, and a deployment configuration.
