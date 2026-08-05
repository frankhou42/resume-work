//
//  MainChatColumn.swift
//  Tree
//
//  Refactored from ContentView.swift
//

import SwiftUI

extension ContentView {

    var mainChatColumn : some View{
        //make the Stack in it scrollable
        VStack(spacing: 0) {
            mainHeader
            ScrollView {
                VStack(alignment: .leading, spacing: 16) {
                    //loop through each message in the selected chat
                    ForEach(chats[selectedChatIndex].messages) { message in
                        messageRow(msg: message)
                    }
                }
                .padding()
                .frame(maxWidth: .infinity, alignment: .leading)
                //expands to full width of screen and left align
            }

            chatInputBar(
                placeholder: isResponding ? "Responding…" : "Message",
                text: $mainMessage,
                onSend: {
                    let text = mainMessage.trimmingCharacters(in: .whitespacesAndNewlines)
                    guard !text.isEmpty, !isResponding else { return }
                    mainMessage = ""
                    // Stream a real reply from the local model.
                    sendMainMessage(text)
                }
            )
        }
    }

    var mainHeader: some View {
        HStack(spacing: 8) {
            if !showChats{
                showChatsButton
                    .padding(.top, 10)
                    .padding(.leading, 12)
            }
            Image(systemName: "tree")
                .font(.title3)
                .padding(.top, 10)
                .padding(.leading, showChats ? 12 : 4)
            Text("Tree")
                .font(.headline)
                .padding(.top, 10)
            Spacer()
        }
        .padding(.bottom, 8)
    }

    var showChatsButton: some View{
        Button(action: {
            withAnimation{
                if showChats == true{
                    showChats = false
                } else {
                    showChats = true
                }
            }
        }){
            Image(systemName: "line.3.horizontal")
                .foregroundColor(.black)
        }
        .buttonStyle(.bordered)
        .tint(.black)
    }

    func messageRow(msg: ChatMessage) -> some View {
        VStack(alignment: msg.isUser ? .trailing : .leading, spacing: 6) {//tells the alignment of all componetns inside
            HStack {
                //user message: push to the right
                if msg.isUser {
                    Spacer()
                }

                // Empty streaming placeholder shows a typing indicator instead
                // of an empty bubble until the first token arrives.
                Text(msg.text.isEmpty && msg.isStreaming ? "…" : msg.text)
                    .padding(10)
                    .background(msg.isUser ? Color.blue : Color.gray.opacity(0.1))
                    //AI text must be dark on the light-gray bubble to stay readable
                    .foregroundColor(msg.isUser ? .white : .black)
                    .cornerRadius(8)
                    //these are called view modifiers

                //AI message: push to the left
                if !msg.isUser {
                    Spacer()
                }
            }

            //branch button underneath AI messages only (hidden while streaming)
            if !msg.isUser && !msg.isStreaming {
                Button {
                    // Open a branch rooted at THIS AI message so the branch
                    // carries its context into the local model.
                    branchParentMessageID = msg.id
                    branchMessages = []
                    withAnimation {
                        showBranch = true
                    }
                } label : {
                    HStack(spacing: 6) { //spacing determines the space betweenb components in stack
                        Image(systemName: "arrow.branch")
                        Text("Branch")
                    }
                    .font(.subheadline)
                    .padding(.vertical, 6)
                    .padding(.horizontal, 10)
                    .background(Color.blue.opacity(0.15))
                    .foregroundColor(.blue)
                    .cornerRadius(8)
                }
                .buttonStyle(.plain)
                .opacity(showBranch ? 0 : 1)
                .disabled(showBranch)
            }
        }
    }
}
