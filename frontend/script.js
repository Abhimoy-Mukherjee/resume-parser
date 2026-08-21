const API = '';

async function analyzeResume() {
  const fileInput = document.getElementById('resume-file');
  const jdText = document.getElementById('jd-text').value.trim();
  const btn = document.getElementById('analyze-btn');
  const loading = document.getElementById('loading');
  const resultContainer = document.getElementById('result-container');

  // Basic validation before sending anything
  if (!fileInput.files.length) {
    showError('Please upload a resume file.');
    return;
  }
  if (!jdText) {
    showError('Please paste a job description.');
    return;
  }

  // Build the multipart form data — this is how you send a FILE + TEXT together
  const formData = new FormData();
  formData.append('resume_file', fileInput.files[0]);
  formData.append('job_description', jdText);

  // UI: show loading state, disable button so they can't double-submit
  btn.disabled = true;
  loading.style.display = 'block';
  resultContainer.innerHTML = '';

  try {
    const res = await fetch(`${API}/analyze`, {
      method: 'POST',
      body: formData
      // Note: no 'Content-Type' header set manually — the browser sets the correct
      // multipart boundary automatically when you pass a FormData object as the body.
    });

    const data = await res.json();

    if (!res.ok) {
      throw new Error(data.detail || 'Something went wrong');
    }

    renderResult(data);

  } catch (e) {
    showError(e.message);
  } finally {
    btn.disabled = false;
    loading.style.display = 'none';
  }
}

function renderResult(data) {
  const container = document.getElementById('result-container');
  const d = data.details;

  container.innerHTML = `
    <div class="result-card">
      <div class="result-score">${data.score}%</div>
      <div class="result-name">Candidate: ${data.name || 'Unknown'}</div>

      <div class="detail-block">
        <div class="detail-label">Final Verdict</div>
        <div class="detail-value">${d.final_verdict || '—'}</div>
      </div>

      <div class="detail-block">
        <div class="detail-label">Matching Skills</div>
        <div class="detail-value">${(d.matching_skills || []).join(', ') || 'None found'}</div>
      </div>

      <div class="detail-block">
        <div class="detail-label">Missing Skills</div>
        <div class="detail-value">${(d.missing_important_skills || []).join(', ') || 'None'}</div>
      </div>

      <div class="detail-block">
        <div class="detail-label">Experience Requirement</div>
        <div class="detail-value">${d.experience_requirement_met || '—'}</div>
      </div>

      <div class="detail-block">
        <div class="detail-label">How to Improve</div>
        <div class="detail-value">${d.improvement_suggestions || '—'}</div>
      </div>
    </div>
  `;
}

function showError(message) {
  document.getElementById('result-container').innerHTML = `
    <div class="error-card">⚠ ${message}</div>
  `;
}