import React, { useState } from "react";
import ChatBox from "./src/components/Chatbox";
import HistoryPanel from "./src/components/HistoryPanel";
import Insights from "./components/Insights";
import "./App.css"; // optional styling

function App() {
  const [history, setHistory] = useState([]);
  const [insights, setInsights] = useState({});

  // When a new Q&A exchange finishes, append to history
  const addToHistory = (entry) => {
    setHistory((prev) => [...prev, entry]);
  };

  // Optionally refresh insights from backend
  const refreshInsights = async () => {
    try {
      const res = await fetch("http://localhost:8000/insights");
      const data = await res.json();
      setInsights(data);
    } catch (err) {
      console.error("Failed to load insights", err);
    }
  };

  return (
    <div className="app-container">
      <header className="header">
        <h1>🧠 Second Brain AI</h1>
      </header>

      <main className="main-grid">
        <section className="chat-section">
          <ChatBox onNewExchange={addToHistory} />
        </section>

        <aside className="sidebar">
          <HistoryPanel history={history} />
          <Insights insights={insights} onRefresh={refreshInsights} />
        </aside>
      </main>
    </div>
  );
}

export default App;
