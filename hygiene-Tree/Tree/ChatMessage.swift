//
//  ChatMessage.swift
//  Tree
//
//  Model for a single chat message.
//  isUser: true = user sent (right-aligned, no branch button)
//  isUser: false = AI response (left-aligned, branchable)
//
//  `text` is mutable so streamed tokens can be appended in place while the
//  local model generates, and `isStreaming` drives a live typing indicator.
//

import Foundation

struct ChatMessage: Identifiable, Codable, Equatable {
    var id = UUID()
    var text: String
    let isUser: Bool
    var isStreaming: Bool = false

    /// Convert to the wire format the local Ollama model expects.
    var ollamaMessage: OllamaMessage {
        OllamaMessage(role: isUser ? "user" : "assistant", content: text)
    }
}
