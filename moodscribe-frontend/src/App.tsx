import { useState } from "react";
import { analyzeConversation, type AnalysisResult, type Message } from "./api";

// A small, self-contained demo conversation so the UI is usable without a
// live Instagram session. In production these messages come from /get_messages.
const SAMPLE: Message[] = [
  { text: "hey, been a rough week honestly", sender: "user2", timestamp: "" },
  { text: "oh no, what happened?", sender: "user1", timestamp: "" },
  { text: "just a lot of stress with finals and stuff", sender: "user2", timestamp: "" },
];

export default function App() {
  const [messages, setMessages] = useState<Message[]>(SAMPLE);
  const [draft, setDraft] = useState("");
  const [result, setResult] = useState<AnalysisResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  function addMessage() {
    const text = draft.trim();
    if (!text) return;
    setMessages((m) => [...m, { text, sender: "user2", timestamp: "" }]);
    setDraft("");
    setResult(null);
  }

  async function analyze() {
    setLoading(true);
    setError(null);
    try {
      const r = await analyzeConversation(messages);
      setResult(r);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Something went wrong");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="app">
      <header>
        <h1>MoodScribe</h1>
        <p>Emotion-aware reply suggestions from a fine-tuned local model.</p>
      </header>

      <section className="thread">
        {messages.map((m, i) => (
          <div key={i} className={`bubble ${m.sender === "user1" ? "me" : "them"}`}>
            {m.text}
          </div>
        ))}
      </section>

      <div className="composer">
        <input
          value={draft}
          onChange={(e) => setDraft(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && addMessage()}
          placeholder="Add a message to the conversation…"
        />
        <button onClick={addMessage}>Add</button>
      </div>

      <button className="analyze" onClick={analyze} disabled={loading}>
        {loading ? "Analyzing…" : "Suggest a reply"}
      </button>

      {error && <p className="error">{error}</p>}

      {result && (
        <section className="result">
          <div className="suggested">“{result.suggestedMessage}”</div>
          <div className="signals">
            <span>mood: <b>{result.mood}</b></span>
            <span>suggested tone: <b>{result.suggestedMood}</b></span>
            <span>engagement: <b>{result.engagement}/5</b></span>
          </div>
        </section>
      )}
    </div>
  );
}
