---
layout: page
title: Tree
description: Native macOS client for local LLMs, with context-carrying conversation branches
img:
importance: 1
category: projects
github: https://github.com/frankhou42/Tree
---

**Tree** is a native macOS app for talking to local large language models. It streams responses from
**Llama&nbsp;3.2** through [Ollama](https://ollama.com) entirely on-device — no cloud, no API keys —
and lets you _branch_ any reply into a focused side conversation that inherits the original message as
context. "Permanent" branches persist across launches.

**Stack:** Swift, SwiftUI, Ollama.

**Highlights**

- Streaming client (`AsyncThrowingStream`) over Ollama's `/api/chat`, rendering tokens live.
- Context-aware branching — a branch is seeded with its parent AI message so the model stays on-topic.
- Codable persistence of chats and saved branches to Application Support.

[View on GitHub →](https://github.com/frankhou42/Tree)
