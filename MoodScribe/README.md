# MoodScribe

An **emotion-aware messaging assistant** that reads the recent tone of a conversation and suggests a
tone-matched reply, along with a read on the current mood and an engagement score. Built at
**HackTX 2024**.

## What it does

Given the last several messages in a thread, MoodScribe returns:
- a **suggested reply** written to match the emotional context,
- the detected **mood** of the conversation,
- a **suggested tone** for the response, and
- an **engagement score**.

## Stack

- **Model** — a **LoRA** adapter fine-tuned with **Unsloth** + **FlashAttention** on conversational
  data, served for inference through **PyTorch / Transformers**.
- **Backend** — **Flask** API (`POST /analyze`) that assembles conversation context and runs
  inference.
- **Frontend** — **React + TypeScript** (Vite) client: renders the thread, lets you extend the
  conversation, and calls the inference API to surface suggestions.

## Repository layout

```
backend/            Flask app + inference (run_inference, /analyze)
model_training/     Unsloth fine-tuning + inference notebooks
frontend/           React + TypeScript (Vite) client
```

## Running it

**Backend**
```bash
cd backend
pip install -r ../requirements.txt
flask --app flaskApp run           # serves on http://localhost:5000
```

**Frontend**
```bash
cd frontend
npm install
npm run dev                        # http://localhost:5173, proxies /analyze -> :5000
```

## Team & my role

MoodScribe was built collaboratively at HackTX 2024. My work focused on the **model side** — the
Unsloth/LoRA fine-tuning pipeline and inference — and the **React + TypeScript frontend**.
The original hackathon submission was pushed from a teammate's account; this repository is my own
copy with the frontend added and credentials removed.

> Note: earlier hackathon code contained an Instagram integration for pulling live DMs. The public
> version ships with that path disabled and **no credentials or session tokens** committed.
