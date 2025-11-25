// Dashboard Tomates (EDA) — versión U6 con estimadores de varianza
// Usa Chart.js + Bootstrap y carga CSV local.

const LS_THEME = "tomates_theme";

// Paleta "tomate" suave para barras / histogramas
const TOMATO_FILL = "rgba(220, 53, 69, 0.45)";
const TOMATO_BORDER = "rgba(220, 53, 69, 0.9)";

// ---- Chart Instances ----
let chTurno, chCalidad, chProv, chDefecto;
let hDiametro, hPeso;
let chScatter;

// ---- Theme ----
function applyTheme(theme) {
  document.documentElement.setAttribute("data-bs-theme", theme);
  const isDark = theme === "dark";
  const gridColor = isDark ? "rgba(255, 255, 255, 0.1)" : "rgba(0, 0, 0, 0.1)";
  const textColor = isDark ? "#dee2e6" : "#212529";
  Chart.defaults.color = textColor;
  Chart.defaults.borderColor = gridColor;
}

const $ = (sel) => document.querySelector(sel);

// ---------- CSV parsing ----------
function parseCSV(text) {
  const lines = text.trim().split(/\r?\n/);
  const headers = lines[0].split(",").map(h => h.trim());
  return lines.slice(1).map(line => {
    const cols = line.split(",").map(c => c.trim());
    const obj = {};
    headers.forEach((h, i) => obj[h] = cols[i]);

    // Casts numéricos
    obj.id_tomate = Number(obj.id_tomate);
    obj.diametro_mm = Number(obj.diametro_mm);
    obj.peso_g = Number(obj.peso_g);
    return obj;
  });
}

// ---------- Helpers ----------
function destroyCharts() {
  [chTurno, chCalidad, chProv, chDefecto, hDiametro, hPeso, chScatter]
    .filter(Boolean).forEach(c => c.destroy());
}

function countBy(rows, key) {
  const m = {};
  for (const r of rows) {
    const k = r[key];
    m[k] = (m[k] ?? 0) + 1;
  }
  return m;
}

function histogram(values, bins = 10) {
  if (!values.length) {
    return { labels: [], counts: [] };
  }
  const min = Math.min(...values);
  const max = Math.max(...values);
  const width = (max - min) / bins || 1;
  const counts = Array(bins).fill(0);
  for (const v of values) {
    let idx = Math.floor((v - min) / width);
    if (idx === bins) idx = bins - 1;
    counts[idx]++;
  }
  const labels = counts.map((_, i) => {
    const a = min + i * width;
    const b = a + width;
    return `${a.toFixed(1)}–${b.toFixed(1)}`;
  });
  return { labels, counts };
}

function linearFit(xs, ys) {
  const n = xs.length;
  const xbar = xs.reduce((a,b)=>a+b,0)/n;
  const ybar = ys.reduce((a,b)=>a+b,0)/n;
  let num=0, den=0;
  for (let i=0;i<n;i++){
    num += (xs[i]-xbar)*(ys[i]-ybar);
    den += (xs[i]-xbar)**2;
  }
  const m = num/den;
  const b = ybar - m*xbar;
  return { m, b };
}

function toCSV(rows) {
  const header = Object.keys(rows[0] || {});
  const lines = [header.join(",")];
  for (const r of rows) {
    lines.push(header.map(h => `"${String(r[h]).replace(/"/g,'""')}"`).join(","));
  }
  return lines.join("\n");
}

function download(name, text) {
  const blob = new Blob([text], { type: "text/csv;charset=utf-8" });
  const a = document.createElement("a");
  a.href = URL.createObjectURL(blob);
  a.download = name;
  a.click();
  URL.revokeObjectURL(a.href);
}

// Media y varianza muestral (divisor n-1)
function meanAndVar(values) {
  const n = values.length;
  if (!n) return { mean: NaN, variance: NaN };
  const mean = values.reduce((a,b)=>a+b,0) / n;
  if (n === 1) return { mean, variance: 0 };
  let sumSq = 0;
  for (const v of values) {
    sumSq += (v - mean) ** 2;
  }
  const variance = sumSq / (n - 1);
  return { mean, variance };
}

// ---------- Builders ----------
function buildBar(canvasId, map, title) {
  const labels = Object.keys(map);
  const data = labels.map(k => map[k]);
  const ctx = $(canvasId);
  return new Chart(ctx, {
    type: "bar",
    data: {
      labels,
      datasets: [{
        label: title,
        data,
        borderWidth: 1,
        backgroundColor: TOMATO_FILL,
        borderColor: TOMATO_BORDER
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      animation: false,
      plugins: { legend: { display: false } },
      scales: { y: { beginAtZero: true } }
    }
  });
}

function buildPie(canvasId, map) {
  const labels = Object.keys(map);
  const data = labels.map(k => map[k]);
  return new Chart($(canvasId), {
    type: "pie",
    data: { labels, datasets: [{ data }] },
    options: { responsive: true, maintainAspectRatio: false, animation: false }
  });
}

function buildHist(canvasId, values, title) {
	const { labels, counts } = histogram(values, 10);
	return new Chart($(canvasId), {
		type: "bar",
		data: {
			labels,
			datasets: [
				{
					label: title,
					data: counts,
					borderWidth: 1,
					backgroundColor: TOMATO_FILL,
					borderColor: TOMATO_BORDER,

					// 👉 Hace que las barras queden pegadas entre sí
					categoryPercentage: 1.0,
					barPercentage: 1.0,
				},
			],
		},
		options: {
			responsive: true,
			maintainAspectRatio: false,
			animation: false,
			scales: {
				y: { beginAtZero: true },
				x: {
					// opcional, por si querés asegurarte de que ocupe todo el ancho
					stacked: false,
				},
			},
			plugins: { legend: { display: false } },
		},
	});
}


function buildScatter(canvasId, xs, ys) {
  const pts = xs.map((x,i)=>({x, y: ys[i]}));
  const { m, b } = linearFit(xs, ys);
  const xmin = Math.min(...xs), xmax = Math.max(...xs);
  const linePts = [{x:xmin, y:m*xmin+b},{x:xmax, y:m*xmax+b}];
  return new Chart($(canvasId), {
    type: "scatter",
    data: {
      datasets: [
        { label:"Datos", data: pts, showLine:false, pointRadius:3 },
        { label:"Recta ajustada", data: linePts, type:"line", tension:0, pointRadius:0 }
      ]
    },
    options: {
      responsive:true, maintainAspectRatio:false, animation:false,
      scales: {
        x: { title:{display:true, text:"Diámetro (mm)"} },
        y: { title:{display:true, text:"Peso (g)"} }
      }
    }
  });
}

// ---------- Render ----------
let allRows = [];

function getFilteredRows() {
  const t = $("#fTurno").value;
  const p = $("#fProv").value;
  const c = $("#fCal").value;
  const d = $("#fDef").value;

  return allRows.filter(r =>
    (t==="all" || r.turno===t) &&
    (p==="all" || r.lote_proveedor===p) &&
    (c==="all" || r.categoria_calidad===c) &&
    (d==="all" || r.defecto===d)
  );
}

function fillTable(rows) {
  const tbody = $("#tblData tbody");
  tbody.innerHTML = "";
  for (const r of rows) {
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td>${r.id_tomate}</td>
      <td>${r.fecha}</td>
      <td>${r.turno}</td>
      <td>${r.lote_proveedor}</td>
      <td>${r.categoria_calidad}</td>
      <td>${r.defecto}</td>
      <td class="text-end">${r.diametro_mm.toFixed(1)}</td>
      <td class="text-end">${r.peso_g.toFixed(1)}</td>
    `;
    tbody.appendChild(tr);
  }
}

function updateSummary(rows) {
  const n = rows.length;
  $("#cardN").textContent = n;
  const def = rows.filter(r=>r.defecto==="Sí").length;
  $("#cardDefPct").textContent = n ? ((def/n)*100).toFixed(1)+"%" : "–";

  const pesos = rows.map(r=>r.peso_g);
  const dias  = rows.map(r=>r.diametro_mm);

  const { mean: meanPeso, variance: varPeso } = meanAndVar(pesos);
  const { mean: meanDia,  variance: varDia }  = meanAndVar(dias);

  $("#cardPesoMean").textContent = n ? meanPeso.toFixed(2) : "–";
  $("#cardPesoVar").textContent  = n ? varPeso.toFixed(2)  : "–";
  $("#cardDiaMean").textContent  = n ? meanDia.toFixed(2)  : "–";
  $("#cardDiaVar").textContent   = n ? varDia.toFixed(2)   : "–";
}

function render() {
  const rows = getFilteredRows();
  destroyCharts();

  if (!rows.length) {
    updateSummary([]);
    fillTable([]);
    return;
  }

  updateSummary(rows);

  chTurno   = buildBar("#chartTurno", countBy(rows,"turno"), "Turno");
  chProv    = buildBar("#chartProv", countBy(rows,"lote_proveedor"), "Proveedor");
  chDefecto = buildBar("#chartDefecto", countBy(rows,"defecto"), "Defecto");
  chCalidad = buildPie("#chartCalidad", countBy(rows,"categoria_calidad"));

  hDiametro = buildHist("#histDiametro", rows.map(r=>r.diametro_mm), "Diámetro");
  hPeso     = buildHist("#histPeso", rows.map(r=>r.peso_g), "Peso");

  chScatter = buildScatter("#scatterPesoDiam",
    rows.map(r=>r.diametro_mm),
    rows.map(r=>r.peso_g)
  );

  fillTable(rows);

  $("#btnExport").onclick = () => download("tomates_filtrado.csv", toCSV(rows));
}

// ---------- UI wiring ----------
document.addEventListener("DOMContentLoaded", () => {
  // tema inicial
  const stored = localStorage.getItem(LS_THEME);
  const prefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches;
  const initialTheme = stored || (prefersDark ? "dark" : "light");
  $("#themeSwitch").checked = initialTheme==="dark";
  applyTheme(initialTheme);

  $("#themeSwitch").addEventListener("change", () => {
    const th = $("#themeSwitch").checked ? "dark" : "light";
    localStorage.setItem(LS_THEME, th);
    applyTheme(th);
    render();
  });

  // filtros
  ["#fTurno","#fProv","#fCal","#fDef"].forEach(id=>{
    $(id).addEventListener("change", render);
  });

  // recargar
  $("#btnReload").addEventListener("click", render);

  // carga de archivo local
  $("#fileInput").addEventListener("change", async (e) => {
    const file = e.target.files?.[0];
    if (!file) return;
    const text = await file.text();
    allRows = parseCSV(text);
    render();
  });
});
