//
//  OllamaService.swift
//  Tree
//
//  Talks to a locally running Ollama server (default: http://localhost:11434).
//  Streams tokens from the /api/chat endpoint so the UI can render responses
//  as they are generated, fully on-device with no cloud calls.
//

import Foundation

/// One turn in the wire-format conversation sent to Ollama.
struct OllamaMessage: Codable {
    let role: String   // "system" | "user" | "assistant"
    let content: String
}

/// Errors surfaced to the UI when the local model is unreachable or misbehaves.
enum OllamaError: LocalizedError {
    case serverUnreachable
    case badResponse(Int)
    case decoding

    var errorDescription: String? {
        switch self {
        case .serverUnreachable:
            return "Can't reach Ollama at localhost:11434. Run `ollama serve` and `ollama pull llama3.2`."
        case .badResponse(let code):
            return "Ollama returned HTTP \(code)."
        case .decoding:
            return "Couldn't decode the model's streamed response."
        }
    }
}

/// Minimal async client for Ollama's streaming chat API.
actor OllamaService {
    static let shared = OllamaService()

    private let host: URL
    private let model: String

    init(host: URL = URL(string: "http://localhost:11434")!,
         model: String = "llama3.2") {
        self.host = host
        self.model = model
    }

    /// One JSON object per streamed line from /api/chat.
    private struct StreamChunk: Decodable {
        struct Msg: Decodable { let content: String }
        let message: Msg?
        let done: Bool
    }

    private struct ChatRequest: Encodable {
        let model: String
        let messages: [OllamaMessage]
        let stream: Bool
    }

    /// Streams the assistant's reply token-by-token for the given context.
    ///
    /// - Parameter context: full ordered history (system prompt first, then
    ///   alternating user/assistant turns). Passing the branch's context here
    ///   is what makes a branch a real, context-aware continuation.
    /// - Returns: an async stream of incremental text deltas.
    func streamChat(context: [OllamaMessage]) -> AsyncThrowingStream<String, Error> {
        AsyncThrowingStream { continuation in
            Task {
                do {
                    var request = URLRequest(url: host.appendingPathComponent("api/chat"))
                    request.httpMethod = "POST"
                    request.setValue("application/json", forHTTPHeaderField: "Content-Type")
                    request.httpBody = try JSONEncoder().encode(
                        ChatRequest(model: model, messages: context, stream: true)
                    )

                    let (bytes, response) = try await URLSession.shared.bytes(for: request)

                    guard let http = response as? HTTPURLResponse else {
                        continuation.finish(throwing: OllamaError.serverUnreachable)
                        return
                    }
                    guard http.statusCode == 200 else {
                        continuation.finish(throwing: OllamaError.badResponse(http.statusCode))
                        return
                    }

                    // Ollama emits newline-delimited JSON; decode each line.
                    for try await line in bytes.lines {
                        guard let data = line.data(using: .utf8),
                              let chunk = try? JSONDecoder().decode(StreamChunk.self, from: data)
                        else { continue }

                        if let delta = chunk.message?.content, !delta.isEmpty {
                            continuation.yield(delta)
                        }
                        if chunk.done {
                            continuation.finish()
                            return
                        }
                    }
                    continuation.finish()
                } catch {
                    // URLSession throws when the server is down / refuses the socket.
                    continuation.finish(throwing: OllamaError.serverUnreachable)
                }
            }
        }
    }
}
