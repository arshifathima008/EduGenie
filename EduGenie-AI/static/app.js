// ==================================================
// Helper: Safe API call with proper error handling
// ==================================================
async function callApi(url, body) {
    const res = await fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body)
    });

    const rawText = await res.text();

    let data;
    try {
        data = JSON.parse(rawText);
    } catch (e) {
        // Backend returned HTML error page (500 Internal Server Error)
        if (res.status === 500) {
            throw new Error(
                "Server error — likely Gemini API quota exhausted. " +
                "Wait ~24 hours (resets 1:30 PM IST) or use a new API key."
            );
        }
        throw new Error("Server returned an invalid response.");
    }

    if (!res.ok) {
        const msg = data.detail || data.message || "Request failed";
        throw new Error(msg);
    }

    return data;
}


// ==================================================
// Q&A
// ==================================================
document.getElementById("qaBtn").addEventListener("click", async () => {
    const question = document.getElementById("question").value.trim();
    if (!question) return showOutput("qaResult", "Please enter a question.");
    showOutput("qaResult", '<span class="loading">EduGenie is thinking...</span>');
    try {
        const data = await callApi("/qa", { question });
        showOutput("qaResult", "<h3>Answer:</h3>" + formatText(data.answer));
    } catch (e) {
        showOutput("qaResult", "❌ " + e.message);
    }
});


// ==================================================
// Explanation
// ==================================================
document.getElementById("explainBtn").addEventListener("click", async () => {
    const topic = document.getElementById("topic").value.trim();
    if (!topic) return showOutput("explanationResult", "Please enter a topic.");
    showOutput("explanationResult", '<span class="loading">Explaining...</span>');
    try {
        const data = await callApi("/explain", { topic });
        showOutput("explanationResult", "<h3>Explanation:</h3>" + formatText(data.explanation));
    } catch (e) {
        showOutput("explanationResult", "❌ " + e.message);
    }
});


// ==================================================
// Summarize
// ==================================================
document.getElementById("summaryBtn").addEventListener("click", async () => {
    const text = document.getElementById("summaryText").value.trim();
    if (!text) return showOutput("summaryResult", "Please enter text to summarize.");
    showOutput("summaryResult", '<span class="loading">Summarizing...</span>');
    try {
        const data = await callApi("/summarize", { text });
        showOutput("summaryResult", "<h3>Summary:</h3>" + formatText(data.summary));
    } catch (e) {
        showOutput("summaryResult", "❌ " + e.message);
    }
});


// ==================================================
// Quiz
// ==================================================
document.getElementById("quizBtn").addEventListener("click", async () => {
    const text = document.getElementById("quizText").value.trim();
    if (!text) return showOutput("quizResult", "Please enter a topic or passage.");
    showOutput("quizResult", '<span class="loading">Generating quiz...</span>');
    try {
        const data = await callApi("/quiz", { text });
        renderQuiz(data.questions);
    } catch (e) {
        showOutput("quizResult", "❌ " + e.message);
    }
});

function renderQuiz(questions) {
    const container = document.getElementById("quizResult");
    container.innerHTML = "<h3>Quiz:</h3>" + questions.map((q, i) => `
        <div class="quiz-question" data-index="${i}">
            <strong>Q${i + 1}: ${escapeHtml(q.question)}</strong>
            ${q.options.map(opt => `
                <button class="quiz-option" data-answer="${escapeHtml(opt)}">
                    ${escapeHtml(opt)}
                </button>
            `).join("")}
            <div class="feedback"></div>
        </div>
    `).join("");
    container.classList.add("show");

    container.querySelectorAll(".quiz-question").forEach((block, i) => {
        const q = questions[i];
        const feedback = block.querySelector(".feedback");
        block.querySelectorAll(".quiz-option").forEach(btn => {
            btn.addEventListener("click", () => {
                const selected = btn.dataset.answer;
                block.querySelectorAll(".quiz-option").forEach(opt => {
                    opt.disabled = true;
                    if (opt.dataset.answer === q.correct_answer) {
                        opt.classList.add("correct");
                    }
                });
                if (selected === q.correct_answer) {
                    feedback.textContent = "Correct! " + (q.explanation || "");
                    feedback.className = "feedback correct";
                } else {
                    btn.classList.add("wrong");
                    feedback.textContent = 'Incorrect. Correct answer: "' + q.correct_answer + '". ' + (q.explanation || "");
                    feedback.className = "feedback wrong";
                }
            });
        });
    });
}


// ==================================================
// Learning Recommendations
// ==================================================
document.getElementById("learnBtn").addEventListener("click", async () => {
    const topic = document.getElementById("learnTopic").value.trim();
    if (!topic) return showOutput("learnResult", "Please enter a topic.");
    showOutput("learnResult", '<span class="loading">Creating your learning path...</span>');
    try {
        const data = await callApi("/learn/recommendations", {
            topic, level: "beginner", weeks: 6
        });
        renderLearningPath(data);
    } catch (e) {
        showOutput("learnResult", "❌ " + e.message);
    }
});

function renderLearningPath(data) {
    let html = "<h3>Learning Recommendations</h3>";
    html += "<p>" + escapeHtml(data.overview) + "</p>";
    data.weeks.forEach(w => {
        html += `<div class="quiz-question">
            <strong>Week ${w.week}: ${escapeHtml(w.focus)}</strong>
            <p><b>Topics:</b> ${w.topics.map(escapeHtml).join(", ")}</p>
            <p><b>Practice:</b> ${escapeHtml(w.practice)}</p>
            <p><b>Resources:</b> ${w.resources.map(escapeHtml).join(", ")}</p>
        </div>`;
    });
    html += "<p><b>Final Assessment:</b> " + escapeHtml(data.final_assessment) + "</p>";
    html += "<p><b>Tips:</b></p><ul>" + data.tips.map(t => "<li>" + escapeHtml(t) + "</li>").join("") + "</ul>";
    showOutput("learnResult", html);
}


// ==================================================
// Helpers
// ==================================================
function showOutput(id, html) {
    const el = document.getElementById(id);
    el.innerHTML = html;
    el.classList.add("show");
}

function formatText(text) {
    return escapeHtml(text).replace(/\n/g, "<br>");
}

function escapeHtml(v) {
    return String(v).replace(/[&<>"']/g, c => ({
        "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#039;"
    }[c]));
}