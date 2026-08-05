//
//  Chat.swift
//  Tree
//
//  A single conversation. Each chat owns its own message history and any
//  saved ("Permanent") branches spun off from its AI responses.
//

import Foundation //frame work that has basic types and utilities

struct Chat: Identifiable, Codable, Equatable {
    //Provides an ID for any Chat instance
    var id = UUID()
    //name of the chat
    var name: String
    //messages stored in chat
    var messages: [ChatMessage]
    //saved branches spun off this chat, keyed by the parent message id
    var savedBranches: [SavedBranch] = []
}

/// A permanent branch: a side conversation rooted at a specific AI message,
/// carrying that message as context so the model continues on-topic.
struct SavedBranch: Identifiable, Codable, Equatable {
    var id = UUID()
    //id of the AI message this branch was spun off from
    var parentMessageID: UUID
    //short label so the user can reopen it
    var title: String
    //messages in this branch
    var messages: [ChatMessage]
}
