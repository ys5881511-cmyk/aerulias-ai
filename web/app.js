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
