// canvas-renderer.js — Canvas 2D 渲染四种可视化风格

function hexToRgb(hex) {
  const h = hex.replace('#', '');
  return [parseInt(h.slice(0,2),16), parseInt(h.slice(2,4),16), parseInt(h.slice(4,6),16)];
}

const Renderers = {
  spectrum(ctx, w, h, frameData) {
    const { spectrum, energy, palette } = frameData;
    ctx.fillStyle = palette.background;
    ctx.fillRect(0, 0, w, h);

    const n = Math.min(spectrum.length, 64);
    const barW = w / n;
    const maxSpec = Math.max(...spectrum.slice(0, n)) + 1e-8;
    const maxE = frameData.maxEnergy || 0.1;
    const energyNorm = Math.min(energy / maxE, 1);

    const r1 = hexToRgb(palette.primary), r2 = hexToRgb(palette.accent);
    for (let i = 0; i < n; i++) {
      const mag = spectrum[i] / maxSpec;
      const barH = mag * h * 0.85;
      if (barH < 1) continue;
      const t = i / n;
      const r = Math.round(r1[0]*(1-t) + r2[0]*t);
      const g = Math.round(r1[1]*(1-t) + r2[1]*t);
      const b = Math.round(r1[2]*(1-t) + r2[2]*t);
      // 主体
      ctx.fillStyle = `rgb(${r},${g},${b})`;
      ctx.fillRect(i*barW + 1, h - barH, barW - 2, barH);
      // 顶部发光
      const br = 0.6 + 0.4 * energyNorm;
      ctx.fillStyle = `rgba(${Math.min(255,r*1.5|0)},${Math.min(255,g*1.5|0)},${Math.min(255,b*1.5|0)},${br})`;
      ctx.fillRect(i*barW + 1, h - barH, barW - 2, 3);
    }
  },

  waveform(ctx, w, h, frameData) {
    const { spectrum, energy, palette } = frameData;
    ctx.fillStyle = palette.background;
    ctx.fillRect(0, 0, w, h);

    const maxSpec = Math.max(...spectrum) + 1e-8;
    const maxE = frameData.maxEnergy || 0.1;
    const energyNorm = Math.min(energy / maxE, 1);
    const cy = h / 2;

    ctx.lineWidth = 2 + energyNorm * 4;
    ctx.lineJoin = 'round';

    const grad = ctx.createLinearGradient(0, 0, w, 0);
    grad.addColorStop(0, palette.primary);
    grad.addColorStop(1, palette.secondary);

    // 上半波形
    ctx.beginPath();
    for (let x = 0; x < w; x++) {
      const idx = Math.floor(x / w * spectrum.length);
      const mag = spectrum[idx] / maxSpec;
      const y = cy - mag * cy * 0.8;
      if (x === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
    }
    ctx.strokeStyle = grad;
    ctx.stroke();

    // 下半镜像（半透明）
    ctx.globalAlpha = 0.3;
    ctx.beginPath();
    for (let x = 0; x < w; x++) {
      const idx = Math.floor(x / w * spectrum.length);
      const mag = spectrum[idx] / maxSpec;
      const y = cy + mag * cy * 0.8;
      if (x === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
    }
    ctx.stroke();
    ctx.globalAlpha = 1;
  },

  particle(ctx, w, h, frameData) {
    const { spectrum, energy, palette, frame, bpm, beat_times, total } = frameData;
    ctx.fillStyle = palette.background;
    ctx.fillRect(0, 0, w, h);

    const maxE = frameData.maxEnergy || 0.1;
    const energyNorm = Math.min(energy / maxE, 1);
    const fps = frameData.duration > 0 ? total / frameData.duration : 30;
    const isBeat = beat_times.some(t => Math.abs(t * fps - frame) < 2);

    const cx = w/2, cy = h/2;
    const nParticles = Math.floor(200 + energyNorm * 600 + (isBeat ? 400 : 0));
    const colors = [palette.primary, palette.secondary, palette.accent].map(hexToRgb);

    const rng = mulberry32(frame * 1234567);
    for (let i = 0; i < nParticles; i++) {
      const angle = rng() * Math.PI * 2;
      const maxR = (isBeat ? 0.6 : 0.35) * Math.min(w, h);
      const radius = rng() * maxR * (0.3 + 0.7 * energyNorm);
      const px = cx + radius * Math.cos(angle);
      const py = cy + radius * Math.sin(angle);
      const color = colors[Math.floor(rng() * colors.length)];
      const size = 1 + rng() * (isBeat ? 4 : 2);
      const bright = 0.4 + 0.6 * energyNorm;
      ctx.fillStyle = `rgba(${color[0]*bright|0},${color[1]*bright|0},${color[2]*bright|0},0.9)`;
      ctx.beginPath();
      ctx.arc(px, py, Math.max(0.5, size), 0, Math.PI * 2);
      ctx.fill();
    }

    // 中心发光核心
    const gR = 20 + energyNorm * 40 + (isBeat ? 30 : 0);
    const c = hexToRgb(palette.primary);
    const grd = ctx.createRadialGradient(cx, cy, 0, cx, cy, gR);
    grd.addColorStop(0, '#ffffff');
    grd.addColorStop(0.4, `rgb(${c[0]},${c[1]},${c[2]})`);
    grd.addColorStop(1, 'transparent');
    ctx.fillStyle = grd;
    ctx.beginPath();
    ctx.arc(cx, cy, gR, 0, Math.PI * 2);
    ctx.fill();
  },

  circular(ctx, w, h, frameData) {
    const { spectrum, energy, palette, frame, total, bpm } = frameData;
    ctx.fillStyle = palette.background;
    ctx.fillRect(0, 0, w, h);

    const maxSpec = Math.max(...spectrum) + 1e-8;
    const maxE = frameData.maxEnergy || 0.1;
    const energyNorm = Math.min(energy / maxE, 1);
    const cx = w/2, cy = h/2;
    const baseR = Math.min(w, h) * 0.15;
    const maxBar = Math.min(w, h) * 0.35;
    const rotation = (frame / (total || 1)) * (bpm / 60) * Math.PI * 2;

    const n = Math.min(spectrum.length, 64);
    const r1 = hexToRgb(palette.primary), r2 = hexToRgb(palette.secondary);
    ctx.lineWidth = Math.max(1, 2 + energyNorm * 3);

    for (let i = 0; i < n; i++) {
      const mag = spectrum[i] / maxSpec;
      const barLen = mag * maxBar;
      if (barLen < 2) continue;
      const angle = rotation + (2 * Math.PI * i / n);
      const x1 = cx + baseR * Math.cos(angle);
      const y1 = cy + baseR * Math.sin(angle);
      const x2 = cx + (baseR + barLen) * Math.cos(angle);
      const y2 = cy + (baseR + barLen) * Math.sin(angle);
      const t = i / n;
      const r = Math.round(r1[0]*(1-t) + r2[0]*t);
      const g = Math.round(r1[1]*(1-t) + r2[1]*t);
      const b = Math.round(r1[2]*(1-t) + r2[2]*t);
      ctx.strokeStyle = `rgb(${r},${g},${b})`;
      ctx.beginPath();
      ctx.moveTo(x1, y1);
      ctx.lineTo(x2, y2);
      ctx.stroke();
    }

    // 内圆
    const ac = hexToRgb(palette.accent);
    ctx.strokeStyle = `rgb(${ac[0]},${ac[1]},${ac[2]})`;
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.arc(cx, cy, baseR, 0, Math.PI * 2);
    ctx.stroke();
    ctx.fillStyle = `rgba(${ac[0]},${ac[1]},${ac[2]},0.8)`;
    ctx.beginPath();
    ctx.arc(cx, cy, baseR * 0.4, 0, Math.PI * 2);
    ctx.fill();
  }
};

// mulberry32 固定种子随机数生成器
function mulberry32(a) {
  return function() {
    a |= 0; a = a + 0x6D2B79F5 | 0;
    let t = Math.imul(a ^ a >>> 15, 1 | a);
    t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t;
    return ((t ^ t >>> 14) >>> 0) / 4294967296;
  };
}
