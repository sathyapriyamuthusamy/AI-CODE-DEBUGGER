from __future__ import annotations

import ast
import keyword
from collections import Counter
from typing import Any

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

app = FastAPI(
    title="AI Code Debugger API",
    description="A lightweight static checker for beginner Python snippets.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Development prototype only; restrict in production.
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


class AnalyzeRequest(BaseModel):
    code: str = Field(min_length=1, max_length=20000)


class Finding(BaseModel):
    line: int
    severity: str
    title: str
    message: str
    suggestion: str


class AnalyzeResponse(BaseModel):
    summary: str
    findings: list[Finding]
    syntax_error: str | None = None


def _defined_names(tree: ast.AST) -> set[str]:
    names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            names.add(node.name)
        elif isinstance(node, ast.Name) and isinstance(node.ctx, (ast.Store, ast.Param)):
            names.add(node.id)
        elif isinstance(node, ast.arg):
            names.add(node.arg)
        elif isinstance(node, (ast.Import, ast.ImportFrom)):
            for alias in node.names:
                names.add(alias.asname or alias.name.split(".")[0])
    names.update(dir(__builtins__))
    names.update(keyword.kwlist)
    return names


def analyze_python(code: str) -> AnalyzeResponse:
    findings: list[Finding] = []
    try:
        tree = ast.parse(code)
    except SyntaxError as exc:
        line = exc.lineno or 1
        return AnalyzeResponse(
            summary="Python could not parse this snippet. Fix the syntax issue first.",
            findings=[
                Finding(
                    line=line,
                    severity="error",
                    title="Syntax error",
                    message=exc.msg,
                    suggestion="Check the indicated line for a missing colon, bracket, quote, or incorrect indentation.",
                )
            ],
            syntax_error=f"Line {line}: {exc.msg}",
        )

    defined = _defined_names(tree)
    loads: list[tuple[str, int]] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
            loads.append((node.id, getattr(node, "lineno", 1)))

    # Basic name check; deliberately conservative and not a full scope/type checker.
    for name, line in loads:
        if name not in defined:
            findings.append(Finding(
                line=line,
                severity="warning",
                title=f"Possible undefined name: {name}",
                message=f"'{name}' is used but no matching definition was found in this snippet.",
                suggestion=f"Check the spelling of '{name}' or define it before this line.",
            ))

    for node in ast.walk(tree):
        if isinstance(node, ast.Compare):
            if any(isinstance(op, (ast.Eq, ast.NotEq)) for op in node.ops):
                if any(isinstance(comp, ast.Constant) and comp.value is None for comp in node.comparators):
                    findings.append(Finding(
                        line=getattr(node, "lineno", 1),
                        severity="suggestion",
                        title="Prefer identity check for None",
                        message="Comparing a value to None with == or != is usually discouraged in Python.",
                        suggestion="Use `is None` or `is not None` instead.",
                    ))
        if isinstance(node, ast.ExceptHandler) and node.type is None:
            findings.append(Finding(
                line=getattr(node, "lineno", 1),
                severity="warning",
                title="Bare except clause",
                message="A bare `except:` catches almost every exception, including exceptions you may not intend to handle.",
                suggestion="Catch a specific exception type, such as `except ValueError:`.",
            ))
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and not ast.get_docstring(node):
            findings.append(Finding(
                line=getattr(node, "lineno", 1),
                severity="info",
                title=f"Consider documenting `{node.name}`",
                message="This function has no docstring.",
                suggestion="Add a short docstring describing what the function does and any important inputs or outputs.",
            ))

    # Remove duplicate findings while preserving order.
    unique: list[Finding] = []
    seen: set[tuple[Any, ...]] = set()
    for item in findings:
        key = (item.line, item.severity, item.title, item.message)
        if key not in seen:
            seen.add(key)
            unique.append(item)

    if not unique:
        summary = "No obvious issues found by the basic checks. Run your tests too!"
    else:
        summary = f"Found {len(unique)} potential issue(s). Review the suggestions below."

    return AnalyzeResponse(summary=summary, findings=unique)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "AI Code Debugger API"}


@app.post("/analyze", response_model=AnalyzeResponse)
def analyze(request: AnalyzeRequest) -> AnalyzeResponse:
    return analyze_python(request.code)
