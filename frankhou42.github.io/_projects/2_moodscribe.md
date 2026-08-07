---
layout: page
title: MoodScribe
description: Emotion-aware messaging assistant with a fine-tuned local model
img:
importance: 2
category: projects
github: https://github.com/frankhou42/MoodScribe
---

**MoodScribe** reads the recent tone of a conversation and suggests a tone-matched reply, along with a
read on the current mood and an engagement score. Built at **HackTX**.

**Stack:** PyTorch, Unsloth (LoRA), Flask, React, TypeScript.

**Highlights**

- LoRA adapter fine-tuned with Unsloth / FlashAttention for tone-aware reply generation.
- Flask inference API (`/analyze`) assembling conversation context and running the model.
- React + TypeScript client rendering the thread and surfacing suggestions.

[View on GitHub →](https://github.com/frankhou42/MoodScribe)
