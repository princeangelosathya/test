import { useState } from "react";

export default function App() {
  const [messages, setMessages] = useState([
    { role: "bot", text: "Ask me anything about the store's data." },
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  async function send() {
    if (!input.trim() || loading) return;
    const q = input;
    setInput("");
    setLoading(true);
    setMessages((m) => [...m, { role: "user", text: q }]);
    try {
      const res = await fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: q }),
      });
      const data = res.json();
      setMessages((m) => [...m, { role: "bot", text: data.answer }]);
    } catch (e) {
      setMessages((m) => [...m, { role: "bot", text: "Error: " + e.message }]);
    }
    setLoading(false);
  }

  return (
    <div className="app">
      <h1>Store Chat</h1>
      <div className="log">
        {messages.map((m, i) => (
          <div key={i} className={"msg " + m.role}>{m.text}</div>
        ))}
        {loading && <div className="msg bot">Thinking...</div>}
      </div>
      <div className="row">
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && send()}
          placeholder="e.g. Which are the top 5 selling products?"
        />
        <button onClick={send}>Send</button>
      </div>
    </div>
  );
}
