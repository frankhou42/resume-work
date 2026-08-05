// Typed client for the MoodScribe Flask inference API.
//
// The backend exposes POST /analyze which takes the recent conversation and
// returns a tone-matched reply suggestion plus mood/engagement signals from
// the fine-tuned (Unsloth LoRA) model.

export interface Message {
  text: string;
  sender: "user1" | "user2";
  timestamp: string;
}

export interface AnalysisResult {
  suggestedMessage: string;
  mood: string;
  suggestedMood: string;
  engagement: number;
}

/** Ask the backend model to analyze a conversation and suggest a reply. */
export async function analyzeConversation(
  messages: Message[]
): Promise<AnalysisResult> {
  const res = await fetch("/analyze", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ messages }),
  });

  if (!res.ok) {
    throw new Error(`Analyze request failed: HTTP ${res.status}`);
  }

  const data = (await res.json()) as Partial<AnalysisResult> & {
    success?: boolean;
    error?: string;
  };

  if (data.error) throw new Error(data.error);
  if (typeof data.suggestedMessage !== "string") {
    throw new Error("Malformed response from inference API");
  }

  return {
    suggestedMessage: data.suggestedMessage,
    mood: data.mood ?? "neutral",
    suggestedMood: data.suggestedMood ?? "neutral",
    engagement: data.engagement ?? 0,
  };
}
