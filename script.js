const API_BASE = "http://127.0.0.1:8000"; 
const messagesDiv = document.getElementById("messages");
const userInput = document.getElementById("userInput");
const fileInput = document.getElementById("fileInput");
const sendBtn = document.getElementById("sendBtn");

const historyModal = document.getElementById("historyModal");
const historyBtn = document.getElementById("historyBtn");
const closeHistory = document.getElementById("closeHistory");
const clearHistory = document.getElementById("clearHistory");
const historyList = document.getElementById("historyList");

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

function showHistory() {
  const history = JSON.parse(localStorage.getItem("chatHistory") || "[]");
  historyList.innerHTML = history.length
    ? history
        .map(h => `<p><b>${h.role.toUpperCase()}:</b> ${h.text}<br><small>${h.time}</small></p>`)
        .join("<hr>")
    : "<p>Sem histórico salvo.</p>";
  historyModal.style.display = "flex";
}

closeHistory.onclick = () => (historyModal.style.display = "none");
clearHistory.onclick = () => {
  localStorage.removeItem("chatHistory");
  showHistory();
};
historyBtn.onclick = showHistory;

sendBtn.onclick = async () => {
  const text = userInput.value.trim();
  const file = fileInput.files[0];

  if (!text && !file) return alert("Envie um texto ou selecione um PDF!");

  if (text) {
    addMessage("user", text);
    saveToHistory("user", text);
    userInput.value = "";

    addMessage("ai", " Processando sua solicitação...");
    const res = await fetch(`${API_BASE}/search/`, {
      method: "POST",
      body: new URLSearchParams({ query: text }),
    });
    const data = await res.json();

    messagesDiv.lastChild.textContent = data.results || "Erro ao buscar.";
    saveToHistory("ai", data.results);
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
