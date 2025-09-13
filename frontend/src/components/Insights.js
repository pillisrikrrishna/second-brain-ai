import React from "react";

/**
 * Insights
 * --------
 * Shows user analytics/habit trends provided by the backend.
 *
 * Props:
 *  - insights : Object   -> key/value pairs of insights
 *  - onRefresh : Function -> callback to refetch insights from backend
 */
function Insights({ insights, onRefresh }) {
  return (
    <div className="insights-panel">
      <div className="insights-header">
        <h2>User Insights</h2>
        <button onClick={onRefresh} className="insights-refresh">
          Refresh
        </button>
      </div>

      {(!insights || Object.keys(insights).length === 0) ? (
        <p className="insights-empty">
          No insights available yet. Add memories or refresh.
        </p>
      ) : (
        <ul className="insights-list">
          {Object.entries(insights).map(([key, value]) => (
            <li key={key} className="insights-item">
              <strong>{key}:</strong> {String(value)}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default Insights;
