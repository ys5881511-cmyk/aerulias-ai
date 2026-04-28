// ===== STATE =====
let currentResult = null;
let allResults = [];
let charts = {};
let settings = {
  apiTimeout: 30,
  autoRefresh: true,
  showTimestamps: true,
  darkMode: false
};

// ===== DOM ELEMENTS =====
const form = document.querySelector("#runForm");
const queryInput = document.querySelector("#query");
const sourcesInput = document.querySelector("#sources");
const roundsInput = document.querySelector("#rounds");
const targetInput = document.querySelector("#target");
const useMemoryInput = document.querySelector("#useMemory");
const demoModeInput = document.querySelector("#demoMode");
const runButton = document.querySelector("#runButton");
const runStatus = document.querySelector("#runStatus");
const finalAnswer = document.querySelector("#finalAnswer");
const scoreDial = document.querySelector(".score-dial");
const scoreValue = document.querySelector("#scoreValue");
const roundCount = document.querySelector("#roundCount");
const targetValue = document.querySelector("#targetValue");
const memoryCount = document.querySelector("#memoryCount");
const historyCount = document.querySelector("#historyCount");
const roundsList = document.querySelector("#roundsList");
const memoryList = document.querySelector("#memoryList");
const historyList = document.querySelector("#historyList");
const portfolioPanel = document.querySelector("#portfolioPanel");
const progressContainer = document.querySelector("#progressContainer");
const progressFill = document.querySelector("#progressFill");
const progressSteps = document.querySelectorAll(".progress-step");

// ===== INITIALIZATION =====
document.addEventListener("DOMContentLoaded", () => {
  loadSettings();
  setupEventListeners();
  refreshSidebars();
  setScore(null);
  renderPortfolio(null);
});

function setupEventListeners() {
  // Tab Navigation
  document.querySelectorAll(".tab-btn").forEach(btn => {
    btn.addEventListener("click", (e) => {
      const tabName = e.target.dataset.tab;
      switchTab(tabName);
    });
  });

  // Theme Toggle
  document.querySelector("#themeToggle").addEventListener("click", toggleTheme);

  // Export Button
  document.querySelector("#exportBtn").addEventListener("click", () => {
    document.querySelector("#exportModal").style.display = "flex";
  });

  // Settings Button
  document.querySelector("#settingsBtn").addEventListener("click", () => {
    document.querySelector("#settingsModal").style.display = "flex";
  });

  // Modal Close
  document.querySelector("#closeSettings").addEventListener("click", () => {
    document.querySelector("#settingsModal").style.display = "none";
  });

  document.querySelector("#closeExport").addEventListener("click", () => {
    document.querySelector("#exportModal").style.display = "none";
  });

  // Export Options
  document.querySelector("#exportJSON").addEventListener("click", () => exportAsJSON());
  document.querySelector("#exportCSV").addEventListener("click", () => exportAsCSV());
  document.querySelector("#exportHTML").addEventListener("click", () => exportAsHTML());

  // Settings
  document.querySelector("#saveSettings").addEventListener("click", saveSettings);

  // Filters
  document.querySelector("#memoryFilter").addEventListener("input", filterMemory);
  document.querySelector("#historyFilter").addEventListener("input", filterHistory);

  // Search
  document.querySelector("#searchBox").addEventListener("input", handleSearch);

  // Compare
  document.querySelector("#compareBtn").addEventListener("click", compareRuns);

  // Form Submit
  form.addEventListener("submit", handleFormSubmit);

  // Target input
  targetInput.addEventListener("input", () => {
    targetValue.textContent = targetInput.value;
  });

  // Copy buttons
  document.addEventListener("click", async (event) => {
    const button = event.target.closest("[data-copy]");
    if (!button) return;
    await navigator.clipboard.writeText(button.dataset.copy);
    button.textContent = "Copied ✓";
    setTimeout(() => {
      button.textContent = "Copy post";
    }, 1200);
  });

  // Keyboard Shortcuts
  document.addEventListener("keydown", handleKeyboardShortcuts);

  // Close modals on outside click
  document.querySelectorAll(".modal").forEach(modal => {
    modal.addEventListener("click", (e) => {
      if (e.target === modal) modal.style.display = "none";
    });
  });
}

// ===== TAB MANAGEMENT =====
function switchTab(tabName) {
  document.querySelectorAll(".tab-content").forEach(tab => tab.classList.remove("active"));
  document.querySelectorAll(".tab-btn").forEach(btn => btn.classList.remove("active"));
  document.querySelector(`#${tabName}-tab`).classList.add("active");
  document.querySelector(`[data-tab="${tabName}"]`).classList.add("active");

  if (tabName === "analytics") setTimeout(initializeAnalytics, 100);
  if (tabName === "compare") loadCompareSelects();
}

// ===== THEME MANAGEMENT =====
function toggleTheme() {
  const isDark = document.body.classList.toggle("dark-mode");
  settings.darkMode = isDark;
  localStorage.setItem("aerulias_settings", JSON.stringify(settings));
  document.querySelector("#themeToggle").textContent = isDark ? "☀️" : "🌙";
}

function applyTheme() {
  if (settings.darkMode) {
    document.body.classList.add("dark-mode");
    document.querySelector("#themeToggle").textContent = "☀️";
  } else {
    document.body.classList.remove("dark-mode");
    document.querySelector("#themeToggle").textContent = "🌙";
  }
}

// ===== SETTINGS =====
function loadSettings() {
  const saved = localStorage.getItem("aerulias_settings");
  if (saved) {
    settings = { ...settings, ...JSON.parse(saved) };
    applyTheme();
    document.querySelector("#apiTimeout").value = settings.apiTimeout;
    document.querySelector("#autoRefresh").checked = settings.autoRefresh;
    document.querySelector("#showTimestamps").checked = settings.showTimestamps;
  }
}

function saveSettings() {
  settings.apiTimeout = parseInt(document.querySelector("#apiTimeout").value);
  settings.autoRefresh = document.querySelector("#autoRefresh").checked;
  settings.showTimestamps = document.querySelector("#showTimestamps").checked;
  localStorage.setItem("aerulias_settings", JSON.stringify(settings));
  alert("✓ Settings saved!");
  document.querySelector("#settingsModal").style.display = "none";
}

// ===== SCORE & VISUALIZATION =====
function scoreClass(score) {
  if (score >= 85) return "score-good";
  if (score >= 60) return "score-mid";
  return "score-low";
}

function setScore(score) {
  const value = Number.isFinite(score) ? score : 0;
  scoreValue.textContent = Number.isFinite(score) ? String(score) : "--";
  scoreDial.style.setProperty("--score", `${Math.max(0, Math.min(100, value))}%`);
}

// ===== PROGRESS TRACKING =====
function showProgress() {
  progressContainer.style.display = "block";
  resetProgressSteps();
}

function hideProgress() {
  progressContainer.style.display = "none";
}

function resetProgressSteps() {
  progressSteps.forEach(step => step.classList.remove("active", "completed"));
}

function updateProgressStep(stepIndex) {
  for (let i = 0; i < stepIndex; i++) {
    progressSteps[i].classList.add("completed");
    progressSteps[i].classList.remove("active");
  }
  if (stepIndex < progressSteps.length) {
    progressSteps[stepIndex].classList.add("active");
    progressFill.style.width = ((stepIndex + 1) / progressSteps.length * 100) + "%";
  }
}

function updateFlowSteps(currentStep) {
  document.querySelectorAll(".flow-step").forEach((step, idx) => {
    step.classList.remove("active", "completed");
    if (idx < currentStep) step.classList.add("completed");
    if (idx === currentStep) step.classList.add("active");
  });

  document.querySelectorAll(".flow-line").forEach((line, idx) => {
    line.classList.remove("active");
    if (idx < currentStep) line.classList.add("active");
  });
}

// ===== RENDER FUNCTIONS =====
function renderRounds(rounds) {
  if (!rounds.length) {
    roundsList.innerHTML = "";
    return;
  }

  roundsList.innerHTML = rounds.map((round) => {
    const score = round.evaluation?.score ?? 0;
    const issues = round.evaluation?.issues ?? [];
    const suggestions = round.evaluation?.improvement_suggestions ?? [];
    const refined = round.refinement?.refined_answer ?? "";

    return `
      <article class="round-card">
        <div class="round-top">
          <strong>Round ${round.round}</strong>
          <span class="badge ${scoreClass(score)}">${score}/100</span>
        </div>
        <p>${escapeHtml(refined)}</p>
        <ul>
          ${issues.map((issue) => `<li>${escapeHtml(issue)}</li>`).join("")}
          ${suggestions.map((item) => `<li>${escapeHtml(item)}</li>`).join("")}
        </ul>
      </article>
    `;
  }).join("");
}

function renderMemory(items) {
  memoryCount.textContent = String(items.length);
  if (!items.length) {
    memoryList.innerHTML = `<div class="side-item"><p>No memory yet.</p></div>`;
    return;
  }

  memoryList.innerHTML = items.slice().reverse().slice(0, 5).map((item) => `
    <div class="side-item">
      <strong>${escapeHtml(item.query ?? "Untitled query")}</strong>
      <p>${escapeHtml((item.issues ?? []).join(" • "))}</p>
      <span>Score: ${item.score ?? 0}</span>
    </div>
  `).join("");
}

function renderHistory(items) {
  historyCount.textContent = String(items.length);
  if (!items.length) {
    historyList.innerHTML = `<div class="side-item"><p>No runs yet.</p></div>`;
    return;
  }

  historyList.innerHTML = items.slice().reverse().slice(0, 5).map((item) => `
    <div class="side-item">
      <strong>${escapeHtml(item.query ?? "Untitled query")}</strong>
      <p>${escapeHtml((item.final_answer ?? "").substring(0, 60))}...</p>
      <span>Score: ${item.final_score ?? 0}</span>
    </div>
  `).join("");
}

function renderPortfolio(portfolio) {
  if (!portfolio) {
    portfolioPanel.innerHTML = `
      <article class="portfolio-card">
        <p>Run the pipeline to generate resume bullets and a LinkedIn-ready project summary.</p>
      </article>
    `;
    return;
  }

  const bullets = portfolio.resume_bullets ?? [];
  const linkedIn = portfolio.linkedin_post ?? "";
  const explanation = portfolio.beginner_explanation ?? "";

  portfolioPanel.innerHTML = `
    <article class="portfolio-card">
      <h3>📚 Beginner Explanation</h3>
      <p>${escapeHtml(explanation)}</p>
    </article>
    <article class="portfolio-card">
      <h3>💼 Resume Bullets</h3>
      <ul>${bullets.map((bullet) => `<li>${escapeHtml(bullet)}</li>`).join("")}</ul>
    </article>
    <article class="portfolio-card">
      <h3>🔗 LinkedIn Draft</h3>
      <p>${escapeHtml(linkedIn)}</p>
      <button class="secondary-button" type="button" data-copy="${escapeHtml(linkedIn)}">Copy post</button>
    </article>
  `;
}

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

// ===== REFRESH SIDEBARS =====
async function refreshSidebars() {
  try {
    const [memoryResponse, historyResponse] = await Promise.all([
      fetch("/api/memory").catch(() => fetch("/memory")),
      fetch("/api/history").catch(() => fetch("/history"))
    ]);

    const memoryData = await memoryResponse.json();
    const historyData = await historyResponse.json();

    renderMemory(memoryData.memory ?? []);
    renderHistory(historyData.history ?? []);

    allResults = historyData.history ?? [];
    localStorage.setItem("aerulias_results", JSON.stringify(allResults));
  } catch (error) {
    console.error("Failed to refresh sidebars:", error);
  }
}

// ===== FORM SUBMISSION =====
async function handleFormSubmit(event) {
  event.preventDefault();

  const query = queryInput.value.trim();
  if (!query) return;

  runButton.disabled = true;
  runStatus.textContent = "Running";
  runStatus.className = "status-badge";
  finalAnswer.textContent = "Working through the agent loop...";
  roundsList.innerHTML = "";
  renderPortfolio(null);
  setScore(null);
  showProgress();
  updateProgressStep(0);
  updateFlowSteps(0);

  try {
    const payload = {
      query,
      rounds: Number(roundsInput.value),
      target: Number(targetInput.value),
      use_memory: useMemoryInput.checked,
      source_paths: sourcesInput.value,
      demo_mode: demoModeInput.checked
    };

    const response = await fetch("/api/run", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.error || "Pipeline failed");
    }

    currentResult = data.result;
    finalAnswer.textContent = currentResult.final_answer;
    setScore(currentResult.final_score);
    roundCount.textContent = String(currentResult.rounds.length);
    targetValue.textContent = String(currentResult.target_score);
    renderRounds(currentResult.rounds);
    renderPortfolio(currentResult.portfolio);

    runStatus.textContent = "✓ Complete";
    updateProgressStep(progressSteps.length - 1);
    updateFlowSteps(3);

    await refreshSidebars();
  } catch (error) {
    runStatus.textContent = "✕ Error";
    finalAnswer.textContent = error.message;
  } finally {
    runButton.disabled = false;
    hideProgress();
  }
}

// ===== FILTERING =====
function filterMemory(e) {
  const query = e.target.value.toLowerCase();
  document.querySelectorAll("#memoryList .side-item").forEach(item => {
    const text = item.textContent.toLowerCase();
    item.style.display = text.includes(query) ? "block" : "none";
  });
}

function filterHistory(e) {
  const query = e.target.value.toLowerCase();
  document.querySelectorAll("#historyList .side-item").forEach(item => {
    const text = item.textContent.toLowerCase();
    item.style.display = text.includes(query) ? "block" : "none";
  });
}

function handleSearch(e) {
  const query = e.target.value.toLowerCase();
  if (!query) return;
  console.log("Searching for:", query);
}

// ===== EXPORT FUNCTIONS =====
function exportAsJSON() {
  const data = {
    timestamp: new Date().toISOString(),
    currentResult: currentResult,
    allResults: allResults
  };

  const json = JSON.stringify(data, null, 2);
  downloadFile(json, "aerulias-export.json", "application/json");
  document.querySelector("#exportModal").style.display = "none";
  alert("✓ Exported as JSON");
}

function exportAsCSV() {
  let csv = "Query,Initial Score,Final Score,Improvement,Rounds Used\n";

  allResults.forEach(result => {
    const initialScore = result.rounds[0]?.evaluation?.score ?? 0;
    const finalScore = result.final_score ?? 0;
    const improvement = finalScore - initialScore;
    const roundsUsed = result.rounds.length;

    csv += `"${result.query}",${initialScore},${finalScore},${improvement},${roundsUsed}\n`;
  });

  downloadFile(csv, "aerulias-export.csv", "text/csv");
  document.querySelector("#exportModal").style.display = "none";
  alert("✓ Exported as CSV");
}

function exportAsHTML() {
  let html = `<!DOCTYPE html>
<html>
<head>
  <title>Aerulias Export</title>
  <style>
    body { font-family: Arial; margin: 20px; }
    .result { border: 1px solid #ccc; padding: 15px; margin: 10px 0; border-radius: 5px; }
    .query { font-weight: bold; color: #24745b; }
    .score { color: #1e7f86; font-weight: bold; }
  </style>
</head>
<body>
  <h1>Aerulias Results Export</h1>
  <p>Generated: ${new Date().toLocaleString()}</p>
`;

  allResults.forEach(result => {
    html += `
    <div class="result">
      <div class="query">Query: ${escapeHtml(result.query)}</div>
      <div class="score">Final Score: ${result.final_score}/100</div>
      <div>Answer: ${escapeHtml((result.final_answer || "").substring(0, 200))}...</div>
      <div>Rounds: ${result.rounds.length}</div>
    </div>`;
  });

  html += `</body></html>`;

  downloadFile(html, "aerulias-export.html", "text/html");
  document.querySelector("#exportModal").style.display = "none";
  alert("✓ Exported as HTML");
}

function downloadFile(content, filename, type) {
  const blob = new Blob([content], { type });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
}

// ===== ANALYTICS =====
function initializeAnalytics() {
  if (allResults.length === 0) loadStoredResults();
  if (allResults.length === 0) {
    document.querySelector(".analytics-grid").innerHTML = "<p>No results yet. Run the pipeline to see analytics.</p>";
    return;
  }

  updateAnalyticsMetrics();
  drawCharts();
}

function loadStoredResults() {
  const stored = localStorage.getItem("aerulias_results");
  if (stored) allResults = JSON.parse(stored);
}

function updateAnalyticsMetrics() {
  const initialScores = allResults.map(r => r.rounds[0]?.evaluation?.score ?? 0);
  const finalScores = allResults.map(r => r.final_score ?? 0);
  const improvements = finalScores.map((f, i) => f - initialScores[i]);

  const avgInitial = (initialScores.reduce((a, b) => a + b, 0) / initialScores.length).toFixed(1);
  const avgFinal = (finalScores.reduce((a, b) => a + b, 0) / finalScores.length).toFixed(1);
  const avgImprovement = (improvements.reduce((a, b) => a + b, 0) / improvements.length).toFixed(1);

  document.querySelector("#avgInitial").textContent = avgInitial;
  document.querySelector("#avgFinal").textContent = avgFinal;
  document.querySelector("#avgImprovement").textContent = avgImprovement;
  document.querySelector("#totalRuns").textContent = allResults.length;
}

function drawCharts() {
  const initialScores = allResults.map(r => r.rounds[0]?.evaluation?.score ?? 0);
  const finalScores = allResults.map(r => r.final_score ?? 0);
  const roundsUsed = allResults.map(r => r.rounds.length);

  drawScoreChart(initialScores, finalScores);
  drawTrendChart(allResults);
  drawRoundsChart(roundsUsed);
}

function drawScoreChart(initial, final) {
  const ctx = document.querySelector("#scoreChart");
  if (charts.score) charts.score.destroy();

  charts.score = new Chart(ctx, {
    type: "bar",
    data: {
      labels: allResults.map((_, i) => `Run ${i + 1}`),
      datasets: [
        { label: "Initial", data: initial, backgroundColor: "rgba(30, 127, 134, 0.5)", borderColor: "#1e7f86", borderWidth: 1 },
        { label: "Final", data: final, backgroundColor: "rgba(36, 116, 91, 0.7)", borderColor: "#24745b", borderWidth: 1 }
      ]
    },
    options: { responsive: true, plugins: { legend: { position: "top" } }, scales: { y: { beginAtZero: true, max: 100 } } }
  });
}

function drawTrendChart(results) {
  const ctx = document.querySelector("#trendChart");
  if (charts.trend) charts.trend.destroy();

  const improvements = results.map((r, i) => {
    const initial = r.rounds[0]?.evaluation?.score ?? 0;
    const final = r.final_score ?? 0;
    return final - initial;
  });

  charts.trend = new Chart(ctx, {
    type: "line",
    data: {
      labels: results.map((_, i) => `Run ${i + 1}`),
      datasets: [{ label: "Improvement", data: improvements, borderColor: "#24745b", backgroundColor: "rgba(36, 116, 91, 0.1)", tension: 0.4, fill: true }]
    },
    options: { responsive: true, plugins: { legend: { position: "top" } } }
  });
}

function drawRoundsChart(rounds) {
  const ctx = document.querySelector("#roundsChart");
  if (charts.rounds) charts.rounds.destroy();

  charts.rounds = new Chart(ctx, {
    type: "doughnut",
    data: {
      labels: ["1 Round", "2 Rounds", "3+ Rounds"],
      datasets: [{ data: [rounds.filter(r => r === 1).length, rounds.filter(r => r === 2).length, rounds.filter(r => r > 2).length], backgroundColor: ["#24745b", "#1e7f86", "#b97818"] }]
    },
    options: { responsive: true, plugins: { legend: { position: "top" } } }
  });
}

// ===== COMPARE =====
function loadCompareSelects() {
  const select1 = document.querySelector("#compare1");
  const select2 = document.querySelector("#compare2");

  select1.innerHTML = '<option value="">Select a run...</option>';
  select2.innerHTML = '<option value="">Select a run...</option>';

  allResults.forEach((result, idx) => {
    const option1 = document.createElement("option");
    option1.value = idx;
    option1.textContent = `${idx + 1}. ${(result.query || "").substring(0, 40)}...`;
    select1.appendChild(option1);

    const option2 = document.createElement("option");
    option2.value = idx;
    option2.textContent = `${idx + 1}. ${(result.query || "").substring(0, 40)}...`;
    select2.appendChild(option2);
  });
}

function compareRuns() {
  const idx1 = parseInt(document.querySelector("#compare1").value);
  const idx2 = parseInt(document.querySelector("#compare2").value);

  if (isNaN(idx1) || isNaN(idx2)) {
    alert("Please select two runs to compare");
    return;
  }

  const result1 = allResults[idx1];
  const result2 = allResults[idx2];

  const html = `
    <div class="comparison-item">
      <div>
        <h4>Run 1: ${result1.query.substring(0, 50)}</h4>
        <p><strong>Final Score:</strong> ${result1.final_score}/100</p>
        <p><strong>Rounds:</strong> ${result1.rounds.length}</p>
        <p><strong>Memory Used:</strong> ${result1.memory_used?.length || 0}</p>
        <p><strong>Answer:</strong> ${(result1.final_answer || "").substring(0, 100)}...</p>
      </div>
      <div>
        <h4>Run 2: ${result2.query.substring(0, 50)}</h4>
        <p><strong>Final Score:</strong> ${result2.final_score}/100</p>
        <p><strong>Rounds:</strong> ${result2.rounds.length}</p>
        <p><strong>Memory Used:</strong> ${result2.memory_used?.length || 0}</p>
        <p><strong>Answer:</strong> ${(result2.final_answer || "").substring(0, 100)}...</p>
      </div>
    </div>
  `;

  document.querySelector("#compareResults").innerHTML = html;
}

// ===== KEYBOARD SHORTCUTS =====
function handleKeyboardShortcuts(e) {
  if (e.ctrlKey || e.metaKey) {
    switch (e.key.toLowerCase()) {
      case "e":
        e.preventDefault();
        queryInput.focus();
        break;
      case "enter":
        e.preventDefault();
        if (!runButton.disabled) form.dispatchEvent(new Event("submit"));
        break;
      case "d":
        e.preventDefault();
        document.querySelector("#themeToggle").click();
        break;
      case "s":
        e.preventDefault();
        document.querySelector("#settingsBtn").click();
        break;
    }
  }
}

// ===== INITIALIZATION =====
setScore(null);
renderPortfolio(null);
refreshSidebars().catch(() => {});
loadStoredResults();

function scoreClass(score) {
  if (score >= 85) return "score-good";
  if (score >= 60) return "score-mid";
  return "score-low";
}

function setScore(score) {
  const value = Number.isFinite(score) ? score : 0;
  scoreValue.textContent = Number.isFinite(score) ? String(score) : "--";
  scoreDial.style.setProperty("--score", `${Math.max(0, Math.min(100, value))}%`);
}

function renderRounds(rounds) {
  if (!rounds.length) {
    roundsList.innerHTML = "";
    return;
  }

  roundsList.innerHTML = rounds.map((round) => {
    const score = round.evaluation?.score ?? 0;
    const issues = round.evaluation?.issues ?? [];
    const suggestions = round.evaluation?.improvement_suggestions ?? [];
    const refined = round.refinement?.refined_answer ?? "";

    return `
      <article class="round-card">
        <div class="round-top">
          <strong>Round ${round.round}</strong>
          <span class="badge ${scoreClass(score)}">${score}/100</span>
        </div>
        <p>${escapeHtml(refined)}</p>
        <ul>
          ${issues.map((issue) => `<li>${escapeHtml(issue)}</li>`).join("")}
          ${suggestions.map((item) => `<li>${escapeHtml(item)}</li>`).join("")}
        </ul>
      </article>
    `;
  }).join("");
}

function renderMemory(items) {
  memoryCount.textContent = String(items.length);
  memoryList.innerHTML = items.slice().reverse().slice(0, 5).map((item) => `
    <div class="side-item">
      <strong>${escapeHtml(item.query ?? "Untitled query")}</strong>
      <p>${escapeHtml((item.issues ?? []).join(" "))}</p>
      <span>score ${item.score ?? 0}</span>
    </div>
  `).join("") || `<div class="side-item"><p>No memory yet.</p></div>`;
}

function renderHistory(items) {
  historyCount.textContent = String(items.length);
  historyList.innerHTML = items.slice().reverse().slice(0, 5).map((item) => `
    <div class="side-item">
      <strong>${escapeHtml(item.query ?? "Untitled query")}</strong>
      <p>${escapeHtml(item.final_answer ?? "")}</p>
      <span>final score ${item.final_score ?? 0}</span>
    </div>
  `).join("") || `<div class="side-item"><p>No runs yet.</p></div>`;
}

function renderPortfolio(portfolio) {
  if (!portfolio) {
    portfolioPanel.innerHTML = `
      <article class="portfolio-card">
        <p>Run the pipeline to generate resume bullets and a LinkedIn-ready project summary.</p>
      </article>
    `;
    return;
  }

  const bullets = portfolio.resume_bullets ?? [];
  const linkedIn = portfolio.linkedin_post ?? "";
  const explanation = portfolio.beginner_explanation ?? "";

  portfolioPanel.innerHTML = `
    <article class="portfolio-card">
      <h3>Beginner Explanation</h3>
      <p>${escapeHtml(explanation)}</p>
    </article>
    <article class="portfolio-card">
      <h3>Resume Bullets</h3>
      <ul>${bullets.map((bullet) => `<li>${escapeHtml(bullet)}</li>`).join("")}</ul>
    </article>
    <article class="portfolio-card">
      <h3>LinkedIn Draft</h3>
      <p>${escapeHtml(linkedIn)}</p>
      <button class="secondary-button" type="button" data-copy="${escapeHtml(linkedIn)}">Copy post</button>
    </article>
  `;
}

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

async function refreshSidebars() {
  const memoryUrl = window.location.pathname === "/" ? "/memory" : "/api/memory";
  const historyUrl = window.location.pathname === "/" ? "/history" : "/api/history";
  const [memoryResponse, historyResponse] = await Promise.all([
    fetch(memoryUrl).catch(() => fetch("/api/memory")),
    fetch(historyUrl).catch(() => fetch("/api/history"))
  ]);
  const memoryData = await memoryResponse.json();
  const historyData = await historyResponse.json();
  renderMemory(memoryData.memory ?? []);
  renderHistory(historyData.history ?? []);
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();

  const query = queryInput.value.trim();
  if (!query) return;

  runButton.disabled = true;
  runStatus.textContent = "Running";
  finalAnswer.textContent = "Working through the agent loop...";
  roundsList.innerHTML = "";
  renderPortfolio(null);
  setScore(null);

  try {
    const payload = {
      query,
      rounds: Number(roundsInput.value),
      target: Number(targetInput.value),
      use_memory: useMemoryInput.checked,
      source_paths: sourcesInput.value,
      demo_mode: demoModeInput.checked
    };
    const endpoint = window.location.pathname === "/" ? "/pipeline/run" : "/api/run";
    let response = await fetch(endpoint, {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify(payload)
    });

    if (response.status === 404) {
      response = await fetch("/api/run", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(payload)
      });
    }

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.error || "Pipeline failed.");
    }

    const result = data.result;
    finalAnswer.textContent = result.final_answer;
    setScore(result.final_score);
    roundCount.textContent = String(result.rounds.length);
    targetValue.textContent = String(result.target_score);
    renderRounds(result.rounds);
    renderPortfolio(result.portfolio);
    runStatus.textContent = "Complete";
    await refreshSidebars();
  } catch (error) {
    runStatus.textContent = "Error";
    finalAnswer.textContent = error.message;
  } finally {
    runButton.disabled = false;
  }
});

document.addEventListener("click", async (event) => {
  const button = event.target.closest("[data-copy]");

  if (!button) return;

  await navigator.clipboard.writeText(button.dataset.copy);
  button.textContent = "Copied";
  setTimeout(() => {
    button.textContent = "Copy post";
  }, 1200);
});

targetInput.addEventListener("input", () => {
  targetValue.textContent = targetInput.value;
});

setScore(null);
renderPortfolio(null);
refreshSidebars().catch(() => {});
