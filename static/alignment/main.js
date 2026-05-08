// static/alignment/main.js

let lastResult = null;

document.getElementById('align-btn').addEventListener('click', async () => {
  const english = document.getElementById('english-input').value.trim();
  const hindi   = document.getElementById('hindi-input').value.trim();

  if (!english) { alert('Please enter an English sentence.'); return; }

  setLoading(true);

  try {
    const resp = await fetch('/api/align/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json',
                 'X-CSRFToken': getCookie('csrftoken') },
      body: JSON.stringify({ english, hindi })
    });

    if (!resp.ok) {
      const err = await resp.json();
      alert('Error: ' + (err.error || resp.statusText));
      return;
    }

    const data = await resp.json();
    lastResult = data;
    renderResult(data);

  } catch(e) {
    alert('Network error: ' + e.message);
  } finally {
    setLoading(false);
  }
});


function renderResult(data) {
  document.getElementById('result-panel').classList.remove('hidden');

  // Sentences
  document.getElementById('res-english').textContent = data.english;
  document.getElementById('res-hindi').textContent   = data.hindi;
  document.getElementById('res-time').textContent    = data.elapsed_sec;

  // Alignment table
  const tbody = document.getElementById('alignment-body');
  tbody.innerHTML = '';
  data.alignment_rows.forEach((row, idx) => {
    const tr = document.createElement('tr');
    if (row.many_to_many) tr.classList.add('many');
    tr.innerHTML = `
      <td>${idx + 1}</td>
      <td class="en-word">${row.en_word}</td>
      <td class="hi-word">${row.hi_words.join(' + ')}</td>
      <td>${row.many_to_many ? '1→many' : '1→1'}</td>`;
    tbody.appendChild(tr);
  });

  // Unaligned Hindi words
  const unalignedBox = document.getElementById('unaligned-box');
  if (data.unaligned_hindi.length > 0) {
    unalignedBox.classList.remove('hidden');
    document.getElementById('unaligned-words').textContent =
      data.unaligned_hindi.map(w => w.word).join(', ');
  } else {
    unalignedBox.classList.add('hidden');
  }

  // Heatmap
  drawHeatmap(data.sim_matrix, data.src_words, data.tgt_words);
}


function drawHeatmap(matrix, srcWords, tgtWords) {
  const canvas = document.getElementById('heatmap-canvas');
  const ctx    = canvas.getContext('2d');

  const CELL   = 48;
  const MARGIN = 120;

  canvas.width  = MARGIN + tgtWords.length * CELL;
  canvas.height = MARGIN + srcWords.length * CELL;

  ctx.clearRect(0, 0, canvas.width, canvas.height);
  ctx.font = '11px monospace';

  // Draw cells
  matrix.forEach((row, i) => {
    row.forEach((val, j) => {
      const intensity = Math.max(0, Math.min(1, val));
      // Blue-to-red colorscale
      const r = Math.round(255 * intensity);
      const b = Math.round(255 * (1 - intensity));
      ctx.fillStyle = `rgb(${r}, 80, ${b})`;
      ctx.fillRect(MARGIN + j * CELL, MARGIN + i * CELL, CELL - 2, CELL - 2);

      // Value text
      ctx.fillStyle = intensity > 0.5 ? '#fff' : '#222';
      ctx.fillText(val.toFixed(2),
        MARGIN + j * CELL + 4,
        MARGIN + i * CELL + CELL / 2 + 4);
    });
  });

  // Hindi column labels (top)
  ctx.fillStyle = '#333';
  tgtWords.forEach((w, j) => {
    ctx.save();
    ctx.translate(MARGIN + j * CELL + CELL / 2, MARGIN - 8);
    ctx.rotate(-Math.PI / 4);
    ctx.fillText(w, 0, 0);
    ctx.restore();
  });

  // English row labels (left)
  srcWords.forEach((w, i) => {
    ctx.fillStyle = '#333';
    ctx.fillText(w,
      4,
      MARGIN + i * CELL + CELL / 2 + 4);
  });
}


// Download result as JSON
document.getElementById('download-btn').addEventListener('click', () => {
  if (!lastResult) return;
  const blob = new Blob([JSON.stringify(lastResult, null, 2)],
                        { type: 'application/json' });
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = 'alignment_result.json';
  a.click();
});


function setLoading(on) {
  document.getElementById('loading').classList.toggle('hidden', !on);
  document.getElementById('align-btn').disabled = on;
}

function getCookie(name) {
  const val = `; ${document.cookie}`;
  const parts = val.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
}