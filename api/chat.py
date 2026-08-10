import os
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from groq import Groq

app = FastAPI()

# Enable CORS so your GitHub Pages site can talk to this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Groq client using environment variable
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Load David's CV/portfolio context from the repo at startup.
# This file lives at api/portfolio_context.txt — edit that file to update
# what the bot knows, no code changes needed.
CONTEXT_PATH = Path(__file__).parent / "portfolio_context.txt"
try:
    PORTFOLIO_CONTEXT = CONTEXT_PATH.read_text(encoding="utf-8")
except FileNotFoundError:
    PORTFOLIO_CONTEXT = ""

# BASE SYSTEM PROMPT (style + rules). The actual facts about David live in
# portfolio_context.txt and are appended below.
BASE_SYSTEM_PROMPT = """
You are the AI guide embedded in David Rimon Youssef's personal portfolio site. You speak AS David's knowledgeable representative — warm, direct, and specific, never a generic corporate bot.

STYLE:
- Answer in 2-4 sentences by default. Only go longer if the person explicitly asks for a deep technical breakdown.
- Get specific fast: name the actual project, dataset, metric, or tool instead of listing everything every time. If someone asks about ML, talk about the ML projects — not a generic inventory of all projects.
- Sound like a person explaining something they know well, not a summary bot reading bullet points. Vary sentence structure; don't reuse the same opening phrase across answers.
- Light Markdown (bold for key terms/numbers) is fine, but don't over-format short answers with headers or bullet walls.

RULES:
- Only answer using the CONTEXT below. If asked something outside this scope, say so plainly and suggest emailing David — don't stretch an answer to sound complete when it isn't.
- Never invent metrics, dates, or employers not present in the context.
- If asked about internships specifically, be upfront that David hasn't held a formal corporate internship yet, and point to his hands-on project leadership and the Digital Egyptian Pioneers Initiative instead.

CONTEXT (David's CV / portfolio details):
"""

SYSTEM_PROMPT = BASE_SYSTEM_PROMPT + "\n" + PORTFOLIO_CONTEXT


class ChatRequest(BaseModel):
    message: str


@app.post("/api/chat")
async def chat_endpoint(payload: ChatRequest):
    user_message = payload.message.strip()
    if not user_message:
        raise HTTPException(status_code=400, detail="Message cannot be empty.")

    def generate_stream():
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message}
            ],
            temperature=0.65,
            max_completion_tokens=600,
            top_p=1,
            stream=True,
            stop=None
        )

        for chunk in completion:
            token = chunk.choices[0].delta.content or ""
            if token:
                yield token

    return StreamingResponse(generate_stream(), media_type="text/plain")