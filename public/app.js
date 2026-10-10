
const form = document.getElementById("chat-form");
const input = document.getElementById("message");
const chat = document.getElementById("chat");
const send = document.getElementById("send");
const errorBox = document.getElementById("error");

const history = [];

function addMessage(role, content) {
  const div = document.createElement("div");
  div.className = `message ${role}`;
  div.textContent = content;
  chat.appendChild(div);
  chat.scrollTop = chat.scrollHeight;
  return div;
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();

  const message = input.value.trim();
  if (!message || send.disabled) return;

  errorBox.textContent = "";
  addMessage("user", message);
  input.value = "";
  send.disabled = true;

  const loading = addMessage("assistant", "Soch raha hoon...");

  try {
    const response = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        message,
        history: history.slice(-10)
      })
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.error || "Request fail ho gayi.");
    }

    loading.textContent = data.reply;

    history.push(
      { role: "user", content: message },
      { role: "assistant", content: data.reply }
    );

    if (history.length > 20) history.splice(0, history.length - 20);
  } catch (error) {
    loading.textContent = "Jawab nahi mil saka.";
    errorBox.textContent = error.message;
  } finally {
    send.disabled = false;
    input.focus();
  }
});
