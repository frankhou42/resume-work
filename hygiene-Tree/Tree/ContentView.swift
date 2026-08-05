//
//  ContentView.swift
//  Tree
//
//  Created by Frank Hou on 1/5/26.
//

import SwiftUI
import AppKit
// view == component
//ContentView -> screen component
//extends View rules, View type provides the entire UI
struct ContentView: View {
    //each Chat holds its own messages, so switching chats swaps the message list.
    //Loaded from disk on launch; falls back to a single empty chat on first run.
    @State var chats: [Chat] = BranchStore.shared.load() ?? [
        Chat(name: "New Chat", messages: [])
    ]

    //index of the chat that is being selected in the sidebar
    @State var selectedChatIndex: Int = 0

    //live messages shown in the branch panel (rooted at a specific AI message)
    @State var branchMessages: [ChatMessage] = []

    //the AI message the current branch was spun off from (carries context)
    @State var branchParentMessageID: UUID? = nil

    //whenever @State var's val is changed the UI re-renders automatically
    @State var showBranch = false

    //Tracks the type of branch the user chooses, determine UI behavior
    @State var selectedBranchType: String = "Temporary"

    //user input in branch panel, each time user types the state re-renders
    @State var branchMessage: String = ""

    //show the chats log
    @State var showChats = true

    //user can pick which chat to rename
    @State var renameChatIndex: Int = -1

    //new chat's name after renaming
    @State var newName: String = ""

    //adjust width of chat side bar
    @State var chatSidebarWidth: CGFloat = 220

    //main messsage input bar
    @State var mainMessage: String = ""

    //set when the local model can't be reached, surfaced as a banner
    @State var errorText: String? = nil

    //true while a response is streaming, disables send to avoid overlap
    @State var isResponding = false

    // System prompt prepended to every request so the local model behaves
    // like a concise assistant. Kept in one place for reuse across branches.
    let systemPrompt = "You are Tree, a concise, helpful assistant running locally."

    //specific view type provide only a type of view
    var body: some View {
        VStack(spacing: 0) {
            if let errorText {
                errorBanner(errorText)
            }
            HStack {
                if showChats {
                    chatSidebar
                    .transition(.move(edge: .leading)) //View property
                }
                mainChatColumn
                if showBranch {
                    branchPanel
                    .transition(.move(edge: .trailing))
                }
            }
        }
    }

    func errorBanner(_ text: String) -> some View {
        HStack(spacing: 8) {
            Image(systemName: "exclamationmark.triangle.fill")
                .foregroundColor(.orange)
            Text(text)
                .font(.caption)
                .foregroundColor(.black)
            Spacer()
            Button("Dismiss") { errorText = nil }
                .buttonStyle(.plain)
                .font(.caption)
                .foregroundColor(.blue)
        }
        .padding(8)
        .background(Color.orange.opacity(0.12))
    }

    // MARK: - Streaming

    /// Build the ordered context for a request: system prompt + prior turns.
    private func context(from messages: [ChatMessage]) -> [OllamaMessage] {
        var ctx = [OllamaMessage(role: "system", content: systemPrompt)]
        ctx.append(contentsOf: messages.map(\.ollamaMessage))
        return ctx
    }

    /// Send `text` in the MAIN chat: append the user turn, then stream the
    /// assistant reply token-by-token into a placeholder message.
    func sendMainMessage(_ text: String) {
        guard !isResponding else { return }
        let idx = selectedChatIndex
        chats[idx].messages.append(ChatMessage(text: text, isUser: true))
        // Context is everything so far (the user turn we just added included).
        let history = chats[idx].messages
        let placeholderID = UUID()
        chats[idx].messages.append(
            ChatMessage(id: placeholderID, text: "", isUser: false, isStreaming: true)
        )
        persist()

        streamReply(context: context(from: history)) { delta in
            guard let mIdx = chats[idx].messages.firstIndex(where: { $0.id == placeholderID })
            else { return }
            chats[idx].messages[mIdx].text += delta
        } onFinish: {
            if let mIdx = chats[idx].messages.firstIndex(where: { $0.id == placeholderID }) {
                chats[idx].messages[mIdx].isStreaming = false
            }
            persist()
        }
    }

    /// Send `text` in the BRANCH panel. The branch context includes the parent
    /// AI message, so the model continues the tangent on-topic.
    func sendBranchMessage(_ text: String) {
        guard !isResponding else { return }
        branchMessages.append(ChatMessage(text: text, isUser: true))
        let history = branchMessages
        let placeholderID = UUID()
        branchMessages.append(
            ChatMessage(id: placeholderID, text: "", isUser: false, isStreaming: true)
        )

        // Seed context with the parent AI message if this branch has one.
        var seed: [ChatMessage] = []
        if let pid = branchParentMessageID,
           let parent = chats[selectedChatIndex].messages.first(where: { $0.id == pid }) {
            seed = [parent]
        }
        let full = seed + history

        streamReply(context: context(from: full)) { delta in
            guard let mIdx = branchMessages.firstIndex(where: { $0.id == placeholderID })
            else { return }
            branchMessages[mIdx].text += delta
        } onFinish: {
            if let mIdx = branchMessages.firstIndex(where: { $0.id == placeholderID }) {
                branchMessages[mIdx].isStreaming = false
            }
            // Persist permanent branches back onto the parent chat.
            if selectedBranchType == "Permanent", let pid = branchParentMessageID {
                saveBranch(parentID: pid)
            }
        }
    }

    /// Shared streaming driver: pulls deltas off the OllamaService stream and
    /// applies them on the main actor. Surfaces a banner if the model is down.
    private func streamReply(context: [OllamaMessage],
                             onDelta: @escaping (String) -> Void,
                             onFinish: @escaping () -> Void) {
        isResponding = true
        errorText = nil
        Task {
            do {
                let stream = await OllamaService.shared.streamChat(context: context)
                for try await delta in stream {
                    await MainActor.run { onDelta(delta) }
                }
                await MainActor.run {
                    isResponding = false
                    onFinish()
                }
            } catch {
                await MainActor.run {
                    isResponding = false
                    errorText = (error as? OllamaError)?.errorDescription
                        ?? error.localizedDescription
                    onFinish()
                }
            }
        }
    }

    // MARK: - Persistence

    func persist() { BranchStore.shared.save(chats) }

    /// Save the current branch conversation onto its parent chat.
    private func saveBranch(parentID: UUID) {
        let title = branchMessages.first(where: { $0.isUser })?.text ?? "Branch"
        let branch = SavedBranch(
            parentMessageID: parentID,
            title: String(title.prefix(40)),
            messages: branchMessages
        )
        if let existing = chats[selectedChatIndex].savedBranches
            .firstIndex(where: { $0.parentMessageID == parentID }) {
            chats[selectedChatIndex].savedBranches[existing] = branch
        } else {
            chats[selectedChatIndex].savedBranches.append(branch)
        }
        persist()
    }
}

// tells xcode to show a live demo
#Preview {
    ContentView()
    .frame(width: 1000, height: 700)
}
