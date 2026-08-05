# Tree 🌳

A native macOS client for **local** large language models. Tree streams responses from
**Llama 3.2** through [Ollama](https://ollama.com) entirely on-device — no cloud, no API keys — and
lets you *branch* any reply into a side conversation that carries the original message as context.

Built in **Swift / SwiftUI**.

## Why

Long chat threads get messy when you want to explore a tangent without derailing the main
conversation. Tree treats a chat like a tree: branch off any AI message into a focused side thread
that inherits that message as context, then keep or discard it. Because inference runs locally through
Ollama, experimentation is free and private.

## Features

- **On-device inference** — streams tokens from Llama 3.2 via Ollama's `/api/chat`, rendered live.
- **Context-aware branching** — a branch is seeded with the parent AI message, so the model
  continues the tangent on-topic.
- **Persistent branches** — "Permanent" branches are saved to disk (JSON in Application Support) and
  survive relaunches; "Temporary" branches are discarded on close.
- **Multi-chat sidebar** — rename, switch, and manage multiple conversations.

## Architecture

| File | Responsibility |
|------|----------------|
| `OllamaService.swift` | `actor` streaming client for `localhost:11434/api/chat` (`AsyncThrowingStream`). |
| `BranchStore.swift` | Codable persistence of chats + saved branches. |
| `ContentView.swift` | State, streaming drivers, branch save logic. |
| `MainChatColumn.swift` / `BranchPanel.swift` / `ChatSidebar.swift` | SwiftUI views. |
| `Chat.swift` / `ChatMessage.swift` | Models (Codable). |

## Running it

**Prerequisites:** macOS 14+, Xcode 16+, and [Ollama](https://ollama.com).

```bash
# 1. Start Ollama and pull the model
ollama serve                 # if not already running as a service
ollama pull llama3.2

# 2. Open and run
open Tree.xcodeproj          # then press ⌘R in Xcode
```

If the model isn't reachable, Tree shows a banner explaining how to start Ollama — it never crashes.

## Notes

Model and host are configurable in `OllamaService.init` (defaults: `llama3.2`,
`http://localhost:11434`). The app is sandboxed with the `network.client` entitlement scoped to
localhost.
