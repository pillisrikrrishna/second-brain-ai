import React from "react";

/**
 * HistoryPanel
 * ------------
 * Displays the running conversation history between
 * the user and their Second Brain.
 *
 * Props:
 *  - history : Array of { question: string, answer: string }
 */
function HistoryPanel({ history }) {
  return (
    <div className="history-panel">
      <h2 className="history-title">Conversation History</h2>

      {history.length === 0 ? (
        <p className="history-empty">No chats yet. Ask your first question!</p>
      ) : (
        <ul className="history-list">
          {history.map((entry, index) => (
            <li key={index} className="history-item">
              <p className="history-question">
                <strong>You:</strong> {entry.question}
              </p>
              <p className="history-answer">
                <strong>Second Brain:</strong> {entry.answer}
              </p>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default HistoryPanel;
