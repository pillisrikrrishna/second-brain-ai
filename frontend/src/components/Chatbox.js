import React, { useState } from "react";

/**
 * ChatBox
 * -------
 * Handles user input, sends questions to the backend,
 * and displays the most recent AI response.
 *
 * Props:
 *  - onNewExchange({question, answer}) : callback to add Q&A to history
 */
function ChatBox({ onNewExchange }) {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleAsk = async (e) => {
    e.preventDefault();
    if (!question.trim()) return;

    setLoading(true);
    setError(null);

    try {
      // Adjust backend URL if different
      const res = await fetch("http://localhost:8000/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question }),
      });

      if (!res.ok) throw new Error(`Server error: ${res.status}`);
      const data = await res.json();

      const aiAnswer = data.answer || "No answer received.";
      setAnswer(aiAnswer);
      onNewExchange({ question, answer: aiAnswer });

    } catch (err) {
      console.error(err);
      setError("Something went wrong. Please try again.");
    } finally {
      setLoading(false);
      setQuestion("");
    }
  };

  return (
    <div className="chatbox">
      <form onSubmit={handleAsk} className="chatbox-form">
        <input
          type="text"
          placeholder="Ask your Second Brain..."
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          className="chatbox-input"
        />
        <button type="submit" disabled={loading} className="chatbox-button">
          {loading ? "Thinking..." : "Ask"}
        </button>
      </form>

      {error && <p className="chatbox-error">{error}</p>}

      {answer && (
        <div className="chatbox-answer">
          <strong>Second Brain:</strong> {answer}
        </div>
      )}
    </div>
  );
}

export default ChatBox;
