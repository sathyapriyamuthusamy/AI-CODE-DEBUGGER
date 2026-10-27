const API_BASE = "http://127.0.0.1:8000";
const editor = document.getElementById("code-input");
const analyzeButton = document.getElementById("analyze-button");
const results = document.getElementById("results");
const findingCount = document.getElementById("finding-count");
const lineCount = document.getElementById("line-count");
const apiStatus = document.getElementById("api-status");
const statusDot = document.querySelector(".status-dot");

const exampleCode = `name = "Sam"
print(user_name)

def greet(person):
    return "Hello, " + person`;

function updateLineCount() {
  const count = editor.value.split("\n").length;
  lineCount.textContent = `${count} line${count === 1 ? "" : "s"}`;
}
editor.addEventListener("input", updateLineCount);
updateLineCount();

async function checkHealth() {
  try {
    const response = await fetch(`${API_BASE}/health`);
    if (!response.ok) throw new Error("API unavailable");
    const data = await response.json();
    apiStatus.textContent = data.status === "ok" ? "API connected" : "API status unknown";
    statusDot.classList.add("online");
  } catch {
    apiStatus.textContent = "Start backend to connect";
    statusDot.classList.remove("online");
  }
}
checkHealth();

document.getElementById("load-example").addEventListener("click", () => {
  editor.value = exampleCode;
  updateLineCount();
});

function escapeHTML(value) {
  return String(value).replace(/[&<>"']/g, (char) => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;"
  })[char]);
}

function renderFindings(data) {
  findingCount.textContent = `${data.findings.length} finding${data.findings.length === 1 ? "" : "s"}`;
  const cards = data.findings.map((item) => `
    <article class="finding">
      <div class="finding-top">
        <span class="badge ${escapeHTML(item.severity)}">${escapeHTML(item.severity)}</span>
        <span class="finding-line">LINE ${Number(item.line) || 1}</span>
      </div>
      <h3>${escapeHTML(item.title)}</h3>
      <p>${escapeHTML(item.message)}</p>
      <div class="suggestion">↳ ${escapeHTML(item.suggestion)}</div>
    </article>
  `).join("");
  results.innerHTML = `<div class="summary">${escapeHTML(data.summary)}</div>${
    cards || '<div class="empty-state"><div class="empty-icon">✓</div><h2>No obvious issues</h2><p>Basic checks passed. Run your code and tests to confirm it behaves as expected.</p></div>'
  }`;
}

analyzeButton.addEventListener("click", async () => {
  const code = editor.value.trim();
  if (!code) {
    results.innerHTML = '<div class="summary">Paste some Python code first, then run the analysis.</div>';
    findingCount.textContent = "No code";
    return;
  }
  analyzeButton.disabled = true;
  analyzeButton.querySelector("span:first-child").textContent = "Analyzing…";
  try {
    const response = await fetch(`${API_BASE}/analyze`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ code })
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.detail || "Analysis request failed.");
    renderFindings(data);
  } catch (error) {
    findingCount.textContent = "Connection error";
    results.innerHTML = `<div class="summary">Could not reach the API. Start the FastAPI backend and try again.<br><br><code>${escapeHTML(error.message)}</code></div>`;
  } finally {
    analyzeButton.disabled = false;
    analyzeButton.querySelector("span:first-child").textContent = "Analyze code";
  }
});
