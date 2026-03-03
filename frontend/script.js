const API_BASE = 'http://localhost:5000/api';

// Check backend health on load
window.addEventListener('load', checkHealth);

async function checkHealth() {
    const statusEl = document.getElementById('backend-status');
    try {
        const response = await fetch(`${API_BASE}/health`);
        if (response.ok) {
            statusEl.textContent = 'Backend: Connected';
            statusEl.className = 'status-indicator status-online';
        } else {
            throw new Error();
        }
    } catch (error) {
        statusEl.textContent = 'Backend: Disconnected';
        statusEl.className = 'status-indicator status-offline';
    }
}

async function evaluateProject() {
    const urlInput = document.getElementById('github-url');
    const githubUrl = urlInput.value.trim();

    if (!githubUrl) {
        alert('Please enter a GitHub URL');
        return;
    }

    // Show loading
    document.getElementById('loading').classList.remove('hidden');
    document.getElementById('results').classList.add('hidden');
    document.getElementById('evaluate-btn').disabled = true;

    // Update progress
    updateProgress(10, 'Cloning repository...');

    try {
        const response = await fetch(`${API_BASE}/evaluate`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ github_url: githubUrl })
        });

        const data = await response.json();

        if (!response.ok) {
            const errorMsg = data.error || `HTTP error! status: ${response.status}`;
            const trace = data.trace ? `\n\nTrace:\n${data.trace}` : '';
            throw new Error(errorMsg + trace);
        }

        if (data.error) {
            throw new Error(data.error);
        }

        // Display results
        displayResults(data);

        updateProgress(100, 'Complete!');

    } catch (error) {
        alert('Error: ' + error.message);
        console.error(error);
    } finally {
        document.getElementById('evaluate-btn').disabled = false;
        setTimeout(() => {
            document.getElementById('loading').classList.add('hidden');
        }, 1000);
    }
}

function updateProgress(percent, status) {
    document.getElementById('progress').style.width = percent + '%';
    document.getElementById('status').textContent = status;
}

function displayResults(data) {
    document.getElementById('project-name').textContent = data.project_name || 'Project';
    document.getElementById('total-score').textContent = data.total_score || 0;
    document.getElementById('max-score').textContent = `/ ${data.max_score || 130}`;

    const criteriaContainer = document.getElementById('criteria-results');
    criteriaContainer.innerHTML = '';

    if (data.criteria_results && data.criteria_results.length > 0) {
        data.criteria_results.forEach(criterion => {
            const card = createCriterionCard(criterion);
            criteriaContainer.appendChild(card);
        });
    }

    document.getElementById('results').classList.remove('hidden');
}

function createCriterionCard(criterion) {
    const card = document.createElement('div');
    card.className = 'criterion-card';

    card.innerHTML = `
        <div class="criterion-header">
            <span class="criterion-name">${criterion.criterion || 'Unknown'}</span>
            <span class="criterion-score">${criterion.score || 0}/10</span>
        </div>
        
        <div class="issues-list">
            <h4>Issues:</h4>
            <ul>
                ${(criterion.issues || ['None identified']).map(issue => `<li>${issue}</li>`).join('')}
            </ul>
        </div>
        
        <div class="suggestions-list">
            <h4>Suggestions:</h4>
            <ul>
                ${(criterion.suggestions || ['None provided']).map(suggestion => `<li>${suggestion}</li>`).join('')}
            </ul>
        </div>
    `;

    return card;
}

async function exportJSON() {
    try {
        const response = await fetch(`${API_BASE}/results/latest_results.json`);
        const data = await response.json();

        const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'evaluation-results.json';
        a.click();
        window.URL.revokeObjectURL(url);
    } catch (error) {
        alert('Error exporting JSON: ' + error.message);
    }
}

function exportPDF() {
    alert('PDF export coming soon!');
    // Implement PDF export using a library like jsPDF
}