# Orbit Workspace

> Kanban project management — a complete Python/Flask portfolio demo with a responsive interface and SQLite data persistence.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue) ![Flask](https://img.shields.io/badge/Flask-3.x-black) ![License](https://img.shields.io/badge/License-MIT-green)

## Overview

**Orbit Workspace** is a lightweight but working full-stack web application designed to demonstrate route design, database operations, authentication and responsive UI.

## Features

- Modern mobile-friendly interface
- SQLite database and Flask backend
- Sign-up / sign-in with securely hashed passwords
- Kanban project management workflow
- Input validation and contextual feedback

## Getting Started

```bash
git clone https://github.com/jahongir-stack/orbit-workspace.git
cd orbit-workspace
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Open **http://127.0.0.1:5000** in your browser.

## Structure

```text
app.py                # Flask routes & SQLite models
templates/            # Jinja pages
static/style.css      # Responsive UI
requirements.txt      # Dependencies
```

## Production Considerations

This is a portfolio demonstration, not a production service. Add CSRF tokens, secret management, tests, HTTPS, rate limiting and production hosting before deployment. Checkout is a simulation, not a payment gateway.

## License

MIT.
