//
//  ChatInputBar.swift
//  Tree
//
//  Shared input bar used by both main chat and branch panel
//

import SwiftUI

extension ContentView {

    func chatInputBar(
        placeholder: String,
        text: Binding<String>,
        textColor: Color = .white, //default white, override per use
        onSend: @escaping() -> Void //The content of chatInputBar runs only when clicked
    ) -> some View {
        HStack {
            TextField(placeholder, text: text)
                .textFieldStyle(.plain)
                .padding(10)
                .background(Color.gray.opacity(0.1))
                .cornerRadius(8)
                .foregroundColor(textColor)
            
            Button(action: onSend) {
                Image(systemName: "arrow.up.circle.fill")
                    .font(.system(size: 24))
                    .foregroundColor(.blue)
            }
            .buttonStyle(.plain)
        }
        .padding()
    }
}
