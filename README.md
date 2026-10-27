# AI Code Debugger 🛠️

A beginner-friendly code analysis tool that checks Python snippets for common mistakes and gives clear suggestions. This version uses static checks and does **not** require an API key.

## Features
- Paste Python code into the editor
- Detect common issues such as likely undefined names, unused imports, suspicious `== None`, and missing colons on simple control statements
- See findings with line numbers and suggested fixes
- Example snippets to test the analyzer
- Responsive interface with a clean dark developer UI
- FastAPI backend with a simple health endpoint

> This is a learning prototype, not a replacement for Python's compiler, type checker, or a security review. Static analysis can produce false positives and may miss issues.

## Tech stack
- Frontend: HTML, CSS, JavaScript
- Backend: Python, FastAPI, Uvicorn

## Project structure
```text
AI_Code_Debugger/
├── backend/
│   ├── main.py
│   └── requirements.txt
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── app.js
├── .gitignore
└── README.md
```

## Run locally

### 1. Start the backend
Open a terminal in the project folder:

```bash
cd backend
python -m venv .venv
```

Activate the environment:

**Windows PowerShell**
```powershell
.venv\\Scripts\\Activate.ps1
```

**macOS/Linux**
```bash
source .venv/bin/activate
```

Install dependencies and start the API:
```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

The API runs at `http://127.0.0.1:8000`. Interactive API docs are available at `http://127.0.0.1:8000/docs`.

### 2. Open the frontend
Open `frontend/index.html` in your browser. It calls the backend at `http://127.0.0.1:8000`.

If your browser blocks local API requests when opening the HTML directly, run a simple local web server from the `frontend` folder in a second terminal:
```bash
python -m http.server 5500
```
Then visit `http://127.0.0.1:5500`.

## API
- `GET /health` — confirms the API is running
- `POST /analyze` — accepts JSON `{ "code": "print(hello)" }` and returns findings

## Example
Input:
```python
name = "Sam"
print(user_name)
```
Possible finding: `user_name` may be undefined.

## Future improvements
- Add Python AST-based checks and tests
- Add support for more languages
- Add optional AI explanations through a securely configured server-side API key
- Save analysis history locally

## Developer
Created as a portfolio project to practise Python, API development, frontend integration, and developer tooling.
