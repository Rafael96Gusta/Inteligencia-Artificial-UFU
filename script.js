const API_BASE = "http://127.0.0.1:8000"; // ajuste se necessário
const messagesDiv = document.getElementById("messages");
const userInput = document.getElementById("userInput");
const fileInput = document.getElementById("fileInput");
const sendBtn = document.getElementById("sendBtn");

const historyBtn = document.getElementById("historyBtn");

const chatStatus = document.getElementById("chatStatus");
const apiPill = document.getElementById("apiPill");
const themeSwitcher = document.getElementById("theme-switcher-grid");

const THEME_KEY = "rw_theme_v1";

function setTheme(theme) {
  const t = theme === "light" ? "light" : "dark";
  document.documentElement.setAttribute("data-theme", t);
  localStorage.setItem(THEME_KEY, t);
  if (themeSwitcher) {
    if (t === "dark") {
      themeSwitcher.classList.add("night-theme");
    } else {
      themeSwitcher.classList.remove("night-theme");
    }
  }
}

function loadTheme() {
  const saved = localStorage.getItem(THEME_KEY);
  if (saved === "light" || saved === "dark") return setTheme(saved);
  const prefersLight = window.matchMedia && window.matchMedia("(prefers-color-scheme: light)").matches;
  setTheme(prefersLight ? "light" : "dark");
}

function addMessage(sender, text) {
  const msg = document.createElement("div");
  msg.classList.add("message", sender);
  msg.textContent = text;
  messagesDiv.appendChild(msg);
  messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

function saveToHistory(role, text) {
  const history = JSON.parse(localStorage.getItem("chatHistory") || "[]");
  history.push({ role, text, time: new Date().toLocaleString() });
  localStorage.setItem("chatHistory", JSON.stringify(history));
}

function downloadHistoryPdf() {
  const history = JSON.parse(localStorage.getItem("chatHistory") || "[]");
  if (!history.length) {
    alert("Nenhum histórico para exportar.");
    return;
  }

  if (!window.jspdf || !window.jspdf.jsPDF) {
    alert("Biblioteca de PDF não carregada.");
    return;
  }

  const { jsPDF } = window.jspdf;
  const doc = new jsPDF({ unit: "pt", format: "a4" });
  const marginX = 40;
  let cursorY = 60;

  doc.setFont("helvetica", "bold");
  doc.setFontSize(16);
  doc.text("ReadWise AI — Histórico de resumos", marginX, cursorY);
  cursorY += 24;

  doc.setFontSize(10);
  doc.setFont("helvetica", "normal");

  const width = doc.internal.pageSize.getWidth() - marginX * 2;

  history.forEach((item, index) => {
    const header = `${item.time} — ${item.role.toUpperCase()}`;
    const bodyLines = doc.splitTextToSize(item.text || "", width);

    if (cursorY + bodyLines.length * 12 + 24 > doc.internal.pageSize.getHeight() - 40) {
      doc.addPage();
      cursorY = 60;
    }

    doc.setFont("helvetica", "bold");
    doc.text(header, marginX, cursorY);
    cursorY += 14;

    doc.setFont("helvetica", "normal");
    bodyLines.forEach(line => {
      doc.text(line, marginX, cursorY);
      cursorY += 12;
    });

    cursorY += 10;
    if (index < history.length - 1) {
      doc.setDrawColor(180);
      doc.line(marginX, cursorY, marginX + width, cursorY);
      cursorY += 16;
    }
  });

  const filename = `readwise-historico-${new Date().toISOString().slice(0,10)}.pdf`;
  doc.save(filename);
}

historyBtn.onclick = downloadHistoryPdf;
if (themeSwitcher) {
  themeSwitcher.addEventListener("click", () => {
    const current = document.documentElement.getAttribute("data-theme") || "dark";
    setTheme(current === "light" ? "dark" : "light");
  });
}

sendBtn.onclick = async () => {
  const text = userInput.value.trim();
  const file = fileInput.files[0];

  if (!text && !file) return alert("Envie um texto ou selecione um PDF!");

  if (text) {
    addMessage("user", text);
    saveToHistory("user", text);
    userInput.value = "";

    addMessage("ai", " Processando sua solicitação...");
    const res = await fetch(`${API_BASE}/chat/`, {
      method: "POST",
      body: new URLSearchParams({ query: text }),
    });
    const data = await res.json();

    const answer = data.response || data.results || data.error || "Erro ao buscar.";
    messagesDiv.lastChild.textContent = answer;
    saveToHistory("ai", answer);
  }

  if (file) {
    addMessage("user", `Upload de arquivo: ${file.name}`);
    saveToHistory("user", `Arquivo enviado: ${file.name}`);

    const formData = new FormData();
    formData.append("file", file);

    addMessage("ai", " Analisando PDF...");
    const res = await fetch(`${API_BASE}/upload/`, {
      method: "POST",
      body: formData,
    });
    const data = await res.json();

    messagesDiv.lastChild.textContent = data.analysis || "Erro na análise.";
    saveToHistory("ai", data.analysis);
  }

  fileInput.value = "";
};

apiPill.textContent = API_BASE.replace("http://", "");
loadTheme();
