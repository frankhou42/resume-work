//
//  ChatSidebar.swift
//  Tree
//
//  Refactored from ContentView.swift
//

import SwiftUI
import AppKit

extension ContentView {

    var chatSidebar : some View {
        HStack {
            VStack {
                chatHeader
                ScrollView {
                    VStack(alignment: .leading) {
                        //looping through indices in arr
                        ForEach(chats.indices, id: \.self) { index in
                            if renameChatIndex == index { 
                                //rename logic after double tapping renameChatIndex will be set to that index and then we have
                                //state var to re render the state of text newName when we write so we can see cahnges on screen
                                //we also have on commit where when we click enter the changes is thus saved
                                TextField("Chat name", text: $newName, onCommit: {
                                    chats[index].name = newName.isEmpty ? chats[index].name : newName
                                    renameChatIndex = -1
                                })
                                .textFieldStyle(.plain)
                                .padding(.vertical, 8)
                                .padding(.horizontal, 6)
                                .frame(maxWidth: .infinity, alignment: .leading)
                                .foregroundColor(.white)
                            } else {
                                //normal logic for sidebar just render all
                                Button(action: {
                                    selectedChatIndex = index
                                }) {
                                    Text(chats[index].name)
                                        .foregroundColor(.white)
                                        .padding(.vertical, 8)
                                        .padding(.horizontal, 6)
                                        .frame(maxWidth: .infinity, alignment: .leading)
                                        .background(selectedChatIndex == index ? Color.blue.opacity(0.3) : Color.clear)
                                        .cornerRadius(6)
                                }
                                .contentShape(Rectangle())
                                .buttonStyle(.plain)
                                .onTapGesture(count: 2) { //tap twice to rename
                                    renameChatIndex = index
                                    newName = chats[index].name
                                }
                            }
                        }
                    }
                }
                .scrollIndicators(.never) //fully hide scrollbar on sidebar
            }
            .padding() //padding around VStack
            .frame(width: chatSidebarWidth) //width of vstack
            .background(Color.gray.opacity(0.1))

            // drag handle added to the right （HStack）
            Capsule()
                .fill(Color.gray.opacity(0.45))
                .frame(width: 8)
                .overlay(
                    VStack(spacing: 4) {
                        Circle().fill(Color.white.opacity(0.8)).frame(width: 3, height: 3)
                        Circle().fill(Color.white.opacity(0.8)).frame(width: 3, height: 3)
                        Circle().fill(Color.white.opacity(0.8)).frame(width: 3, height: 3)
                    }
                )
                .padding(.vertical, 12)
                .contentShape(Rectangle())
                .onHover { hovering in
                    if hovering {
                        NSCursor.resizeLeftRight.push()
                    } else {
                        NSCursor.pop()
                    }
                }
                .gesture(
                    DragGesture()
                        //when dragging
                        .onChanged { value in
                            let newWidth = chatSidebarWidth + value.translation.width //newWidth created once, nvr reassigned
                            chatSidebarWidth = min(max(newWidth, 180), 360) //160 is minimum width 360 is max width
                        }
                )

        }
    }

    var chatHeader : some View {
        HStack {
            showChatsButton

            Spacer()

            Button(action: {
                let newChat = Chat(name: "New Chat", messages: [])
                chats.append(newChat)
                selectedChatIndex = chats.count - 1 //length of chat arr - 1
            }){
                Image(systemName: "plus")
                    .foregroundColor(.white)
                Text("New Chat")
                    .foregroundColor(.white)
                    .padding(.vertical, 6)
                    .padding(.horizontal, 8)
            }
            .buttonStyle(.bordered)
            .tint(.white)
        }
    }
}
