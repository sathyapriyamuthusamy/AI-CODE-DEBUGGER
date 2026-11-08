# 🛠️ AI Code Debugger

### A Beginner-Friendly Python Code Analysis Tool

An interactive web-based tool that analyzes Python code snippets, identifies common programming mistakes, and provides actionable suggestions to help developers improve code quality.

## 📌 Overview

AI Code Debugger is a lightweight code analysis application designed to help developers identify common Python coding mistakes without requiring an external AI API.

The application uses static code analysis techniques to inspect Python snippets and highlight potential issues with line numbers and suggested corrections.

It provides a simple interface where users can write or paste code, analyze it, and understand potential errors.

## ✨ Features

- **Code Analysis:** Analyze Python code snippets directly through the web interface.
- **Undefined Name Detection:** Identify potentially undefined variables and names.
- **Unused Import Detection:** Highlight imports that are not being used.
- **Syntax Pattern Checks:** Detect suspicious coding patterns such as `== None`.
- **Missing Colon Detection:** Identify missing colons in simple control statements.
- **Line Number Reporting:** Display findings with their corresponding line numbers.
- **Suggested Fixes:** Provide recommendations for identified issues.
- **Example Snippets:** Test the analyzer using sample Python programs.
- **Responsive Interface:** Clean, dark-themed developer interface.
- **FastAPI Backend:** Lightweight API for code analysis and health monitoring.

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Backend development and code analysis |
| FastAPI | REST API development |
| Uvicorn | ASGI server |
| HTML5 | Frontend structure |
| CSS3 | Interface styling |
| JavaScript | Frontend functionality |

## 🏗️ Project Architecture

```text
AI-Code-Debugger/
│
├── backend/
│   ├── main.py
│   └── requirements.txt
│
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── app.js
│
├── .gitignore
└── README.md
```

## ⚙️ Installation and Setup

### Prerequisites

- Python 3.9 or above
- pip
- A modern web browser

### Step 1: Clone the Repository

```bash
git clone https://github.com/sathyapriyamuthusamy/AI-CODE-DEBUGGER.git
```

### Step 2: Navigate to the Project

```bash
cd AI-CODE-DEBUGGER
```

### Step 3: Set Up the Backend

```bash
cd backend
python -m venv .venv
```

Activate the virtual environment.

**Windows PowerShell:**

```powershell
.venv\Scripts\Activate.ps1
```

**macOS/Linux:**

```bash
source .venv/bin/activate
```

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 5: Start the Backend Server

```bash
uvicorn main:app --reload
```

The backend will be available at:

`http://127.0.0.1:8000`

Interactive API documentation:

`http://127.0.0.1:8000/docs`

### Step 6: Launch the Frontend

Open `frontend/index.html` in your browser.

If local API requests are blocked, start a local frontend server:

```bash
python -m http.server 5500
```

Run this command from the frontend directory.

Open:

`http://127.0.0.1:5500`

## 🔌 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Checks backend availability |
| POST | `/analyze` | Analyzes submitted Python code |

### Example API Request

```json
{
  "code": "name = \"Sam\"\nprint(user_name)"
}
```

The analyzer can identify that `user_name` may be undefined.

## 🎯 Learning Outcomes

This project demonstrates practical experience in:

- Python programming.
- Static code analysis concepts.
- REST API development.
- FastAPI backend implementation.
- Frontend and backend integration.
- JavaScript-based application development.
- Debugging and problem-solving.

## 🚀 Future Enhancements

- Advanced Python AST-based analysis.
- Support for additional programming languages.
- AI-powered explanations and debugging assistance.
- Automated code correction suggestions.
- Analysis history and saved results.
- Enhanced code quality recommendations.

## ⚠️ Limitations

This project is a learning prototype based on static checks.

It is not a replacement for a Python compiler, professional static analysis tools, type checkers, or security auditing tools. Analysis results may include false positives or miss certain issues.

## 👩‍💻 Developer

**Sathyapriya M**

B.Tech – Computer Science and Business Systems

Interested in Artificial Intelligence, Software Development, and Building Practical Technology Solutions.

## 📄 License

This project is available for educational and portfolio purposes.
 
---

**Building smarter developer tools, one line of code at a time.** 🚀
