import React, { useState, useRef, useEffect } from "react";
import axios from "axios";

const API_URL = import.meta.env.VITE_AGENT1_API_URL;

export default function AgentChat() {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([]);
  const chatEndRef = useRef(null);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const sendMessage = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;
    setMessages([...messages, { from: "user", text: input }]);
    setInput("");
    try {
      const res = await axios.post(API_URL, { message: input });
      setMessages((msgs) => [
        ...msgs,
        { from: "agent", text: res.data.response },
      ]);
    } catch (err) {
      setMessages((msgs) => [
        ...msgs,
        { from: "agent", text: "Error: " + err.message },
      ]);
    }
  };

  return (
    <div
      style={{
        minHeight: "100vh",
        background: "#f7f8fa",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
      }}
    >
      <div
        style={{
          width: 420,      // Fixed width
          height: 520,     // Fixed height
          background: "#fff",
          borderRadius: 12,
          boxShadow: "0 2px 8px rgba(0,0,0,0.06)",
          padding: "28px 18px 12px 18px",
          display: "flex",
          flexDirection: "column",
        }}
      >
        <div
          style={{
            fontWeight: 600,
            fontSize: 20,
            color: "#222",
            textAlign: "center",
            marginBottom: 18,
            letterSpacing: "0.01em",
          }}
        >
          Agent1 Support
        </div>
        <div
          style={{
            flex: 1,
            overflowY: "auto",
            background: "#f3f4f6",
            borderRadius: 8,
            padding: 12,
            marginBottom: 12,
            border: "1px solid #e5e7eb",
          }}
        >
          {messages.length === 0 && (
            <div style={{ color: "#aaa", textAlign: "center", fontSize: 15 }}>
              Start the conversation
            </div>
          )}
          {messages.map((m, i) => (
            <div
              key={i}
              style={{
                textAlign: m.from === "user" ? "right" : "left",
                margin: "10px 0",
                display: "flex",
                flexDirection: m.from === "user" ? "row-reverse" : "row",
              }}
            >
              <div
                style={{
                  background: m.from === "user" ? "#e0e7ef" : "#e5e7eb",
                  color: "#222",
                  borderRadius: 10,
                  padding: "8px 13px",
                  maxWidth: "75%",
                  wordBreak: "break-word",
                  fontSize: 15,
                  fontWeight: 400,
                }}
              >
                <span style={{ color: "#6b7280", fontWeight: 500 }}>
                  {m.from === "user" ? "You" : "Agent"}:
                </span>{" "}
                {m.text}
              </div>
            </div>
          ))}
          <div ref={chatEndRef} />
        </div>
        <form
          onSubmit={sendMessage}
          style={{ display: "flex", gap: 6, marginTop: 6 }}
        >
          <input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            style={{
              flex: 1,
              padding: "10px 12px",
              fontSize: 15,
              borderRadius: 7,
              color: "#222",
              border: "1px solid #d1d5db",
              background: "#fafbfc",
              outline: "none",
              fontWeight: 400,
            }}
            placeholder="Type your message…"
            autoFocus
            autoComplete="off"
          />
          <button
            type="submit"
            style={{
              padding: "0 16px",
              borderRadius: 7,
              border: "none",
              background: "#2563eb",
              color: "#fff",
              fontWeight: 500,
              fontSize: 15,
              cursor: "pointer",
              transition: "background 0.2s",
            }}
          >
            Send
          </button>
        </form>
      </div>
      <div style={{
  position: "fixed",
  right: 12,
  bottom: 10,
  fontSize: 13,
  color: "#888",
  background: "rgba(255,255,255,0.85)",
  padding: "6px 12px",
  borderRadius: 8,
  zIndex: 100,
  boxShadow: "0 1px 4px rgba(0,0,0,0.06)"
}}>
  Agent2 (analytics) not implemented due to time constraints.
</div>
    </div>
  );
}
