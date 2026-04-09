// app.js — MusicVision 前端主逻辑

const canvas = document.getElementById('viz-canvas');
const ctx = canvas.getContext('2d');
let jobId = null, currentStyle = 'spectrum';
let frames = [], maxEnergy = 0.1;
let audioInfo = {};
let animationId = null;

// HTML5 Audio 元素，用于播放原始音频
const audio = new Audio();
audio.controls = false;

// 自适应 canvas 尺寸
function resizeCanvas() {
  const area = document.getElementById('canvas-area');
  const transport = document.getElementById('transport');
  canvas.width = area.clientWidth;
  canvas.height = Math.max(100, area.clientHeight - transport.offsetHeight);
}
window.addEventListener('resize', () => { resizeCanvas(); });
resizeCanvas();

// 风格切换
document.querySelectorAll('.style-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('.style-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    currentStyle = btn.dataset.style;
  });
});

// 文件上传
const dropZone = document.getElementById('drop-zone');
const fileInput = document.getElementById('file-input');
dropZone.addEventListener('click', () => fileInput.click());
dropZone.addEventListener('dragover', e => { e.preventDefault(); dropZone.classList.add('dragover'); });
dropZone.addEventListener('dragleave', () => dropZone.classList.remove('dragover'));
dropZone.addEventListener('drop', e => {
  e.preventDefault();
  dropZone.classList.remove('dragover');
  if (e.dataTransfer.files[0]) uploadFile(e.dataTransfer.files[0]);
});
fileInput.addEventListener('change', () => { if (fileInput.files[0]) uploadFile(fileInput.files[0]); });

async function uploadFile(file) {
  // 停止旧播放
  audio.pause();
  audio.src = '';
  cancelAnimationFrame(animationId);
  frames = [];
  maxEnergy = 0.1;

  // 将文件绑定到 Audio 元素（本地 ObjectURL，无需服务端，直接播放）
  audio.src = URL.createObjectURL(file);

  setStatus('正在分析音频...');
  const form = new FormData();
  form.append('file', file);

  try {
    const res = await fetch('/analyze', { method: 'POST', body: form });
    if (!res.ok) throw new Error(`分析失败: ${res.status}`);
    const data = await res.json();
    jobId = data.job_id;
    audioInfo = data;

    document.getElementById('info-bpm').textContent = data.bpm;
    document.getElementById('info-key').textContent = data.key;
    document.getElementById('info-dur').textContent = formatTime(data.duration);
    document.getElementById('info-section').style.display = 'block';
    document.getElementById('btn-export-mp4').disabled = false;
    document.getElementById('btn-export-gif').disabled = false;

    setStatus('正在加载帧数据...');
    await loadFrames(jobId);
    setStatus('就绪 ▶');
    startPlayback();
  } catch (e) {
    setStatus(`错误: ${e.message}`);
  }
}

async function loadFrames(jId) {
  frames = [];
  maxEnergy = 0.1;

  return new Promise((resolve) => {
    const evtSource = new EventSource(`/stream/${jId}`);
    evtSource.onmessage = (e) => {
      const d = JSON.parse(e.data);
      if (d.done || d.error) {
        evtSource.close();
        resolve();
        return;
      }
      frames.push(d);
      maxEnergy = Math.max(maxEnergy, d.energy);
    };
    evtSource.onerror = () => { evtSource.close(); resolve(); };
  });
}

function startPlayback() {
  document.getElementById('btn-play').textContent = '⏸';
  audio.currentTime = 0;
  audio.play().catch(() => {});  // 部分浏览器需要用户手势，play() 失败时静默
  renderLoop();
}

// 以音频时间轴驱动动画（音画同步）
function renderLoop() {
  if (frames.length === 0) return;

  resizeCanvas();

  // 根据音频当前时间计算对应帧索引
  const t = audio.currentTime || 0;
  const duration = audioInfo.duration || 1;
  const frameIdx = Math.min(
    Math.floor((t / duration) * frames.length),
    frames.length - 1
  );

  const frameData = {
    ...frames[frameIdx],
    maxEnergy,
    duration,
  };

  if (Renderers[currentStyle]) {
    Renderers[currentStyle](ctx, canvas.width, canvas.height, frameData);
  }

  // 更新能量条
  const eNorm = Math.min(frameData.energy / maxEnergy, 1);
  document.getElementById('energy-fill').style.width = (eNorm * 100) + '%';

  // 更新进度条和时间显示
  const progress = duration > 0 ? t / duration : 0;
  document.getElementById('progress-fill').style.width = (Math.min(progress, 1) * 100) + '%';
  document.getElementById('time-display').textContent =
    `${formatTime(t)} / ${formatTime(duration)}`;

  animationId = requestAnimationFrame(renderLoop);
}

// 播放 / 暂停
document.getElementById('btn-play').addEventListener('click', () => {
  if (frames.length === 0) return;
  if (audio.paused) {
    audio.play().catch(() => {});
    document.getElementById('btn-play').textContent = '⏸';
    renderLoop();
  } else {
    audio.pause();
    cancelAnimationFrame(animationId);
    document.getElementById('btn-play').textContent = '▶';
  }
});

// 跳到开头
document.getElementById('btn-prev').addEventListener('click', () => {
  audio.currentTime = 0;
});

// 跳到结尾
document.getElementById('btn-next').addEventListener('click', () => {
  if (audioInfo.duration) audio.currentTime = audioInfo.duration;
});

// 点击进度条跳转
document.getElementById('progress-bar').addEventListener('click', (e) => {
  if (!audioInfo.duration) return;
  const rect = e.currentTarget.getBoundingClientRect();
  const t = (e.clientX - rect.left) / rect.width;
  audio.currentTime = t * audioInfo.duration;
});

// 音频播放结束时重置按钮
audio.addEventListener('ended', () => {
  document.getElementById('btn-play').textContent = '▶';
  cancelAnimationFrame(animationId);
});

// 导出
async function doExport(format) {
  if (!jobId) return;
  setStatus(`导出 ${format.toUpperCase()} 中，请稍候...`);
  document.getElementById('btn-export-mp4').disabled = true;
  document.getElementById('btn-export-gif').disabled = true;

  try {
    const res = await fetch(`/export/${jobId}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ format, style: currentStyle, fps: 30, width: 1920, height: 1080 }),
    });
    const data = await res.json();
    if (data.download_url) {
      const a = document.createElement('a');
      a.href = data.download_url;
      a.download = `musicvision.${format}`;
      a.click();
      setStatus('导出完成！');
    }
  } catch (e) {
    setStatus(`导出失败: ${e.message}`);
  } finally {
    document.getElementById('btn-export-mp4').disabled = false;
    document.getElementById('btn-export-gif').disabled = false;
  }
}

document.getElementById('btn-export-mp4').addEventListener('click', () => doExport('mp4'));
document.getElementById('btn-export-gif').addEventListener('click', () => doExport('gif'));

function formatTime(sec) {
  if (!sec || isNaN(sec)) return '0:00';
  const m = Math.floor(sec / 60);
  const s = Math.floor(sec % 60);
  return `${m}:${s.toString().padStart(2, '0')}`;
}

function setStatus(msg) {
  document.getElementById('status').textContent = msg;
}
