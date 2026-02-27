let generatedQuestions = [];

async function generateQuestions() {
    const role = document.getElementById("role").value;
    const questionType = document.getElementById("questionType").value;
    const difficulty = document.getElementById("difficulty").value;
    const numQuestions = document.getElementById("numQuestions").value;
    const customTopicsRaw = document.getElementById("customTopics").value;

    const customTopics = customTopicsRaw
        ? customTopicsRaw.split(",").map(t => t.trim()).filter(Boolean)
        : null;

    const btn = document.getElementById("generateBtn");
    const loading = document.getElementById("loading");
    const results = document.getElementById("results");

    btn.disabled = true;
    loading.classList.remove("hidden");
    results.classList.add("hidden");

    try {
        const response = await fetch("/api/generate", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                role,
                question_type: questionType,
                difficulty,
                num_questions: parseInt(numQuestions),
                custom_topics: customTopics,
            }),
        });

        const data = await response.json();

        if (data.success) {
            generatedQuestions = data.questions;
            renderQuestions(data.questions);
            results.classList.remove("hidden");
        } else {
            alert("Error: " + (data.error || "Failed to generate questions"));
        }
    } catch (err) {
        alert("Error: " + err.message);
    } finally {
        btn.disabled = false;
        loading.classList.add("hidden");
    }
}

function renderQuestions(questions) {
    const container = document.getElementById("questionsList");
    container.innerHTML = questions.map((q, i) => `
        <div class="question-card">
            <div class="q-number">Question ${i + 1}</div>
            <div class="q-text">${q.question}</div>
            <div class="q-meta">
                <span class="tag tag-category">${q.category}</span>
                <span class="tag tag-difficulty">${q.difficulty}</span>
                <span class="tag tag-type">${q.type.replace('_', ' ')}</span>
            </div>
            ${q.expected_skills ? `<div class="q-meta">${q.expected_skills.map(s => `<span class="tag">${s}</span>`).join('')}</div>` : ''}
            <details class="q-hints">
                <summary>Interviewer Notes</summary>
                <p>${q.hints || ''}</p>
                ${q.sample_answer_points ? `<ul>${q.sample_answer_points.map(p => `<li>${p}</li>`).join('')}</ul>` : ''}
            </details>
        </div>
    `).join('');
}

function exportQuestions() {
    if (!generatedQuestions.length) return;
    const blob = new Blob([JSON.stringify(generatedQuestions, null, 2)], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "interview_questions.json";
    a.click();
    URL.revokeObjectURL(url);
}
