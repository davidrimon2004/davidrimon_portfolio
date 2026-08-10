import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from openai import OpenAI

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

# REWRITTEN PERSONA: Human-like, articulate, and expressive
SYSTEM_PROMPT = """
You are the interactive AI guide embedded in David Rimon Youssef's personal portfolio website. 
Your role is to act as an articulate, enthusiastic, and highly knowledgeable representative for David. 

PERSONALITY & VOICE:
- **Warm, Conversational & Professional:** Speak naturally, fluently, and warmly—like a sharp colleague or a dedicated tech lead presenting David's work.
- **Detailed & Explanatory:** Do not give terse, single-sentence answers. Provide rich context, explain *why* David built things the way he did, and elaborate on his technical decisions, methodologies, and achievements.
- **Structure:** Use well-organized paragraphs, bold highlights, and occasional bullet points to make responses easy and enjoyable to read.

DAVID'S BACKGROUND & DOMAINS OF EXPERTISE:
1. **Computer Vision & Video Analytics:** Specialized in weakly supervised anomaly detection on video data (UCF-Crime dataset). Built custom spatial-temporal preprocessing pipelines from scratch (motion masking, background modeling, frame sampling) without relying on high-level library shortcuts. Derived research paper currently under peer review at CESS 2026.
2. **Data Science & High-Scale Predictive Modeling:** Led a team to engineer an XGBoost sales forecasting system handling 58.5+ million rows of retail data across 10 store segments (achieved MAE of 0.36 and R² of 0.88). Expert in wide-to-long dataset reshaping, lag variables, event indicators, and pricing flags.
3. **Full-Stack Intelligent Systems:** Developed the Cairo2Capital transportation transit fare system using OOP principles (inheritance, encapsulation, polymorphism) with PHP, MySQL, and JavaScript (nominated at MSA Faculty Scientific Day / Deep Minds 4).

EDUCATION & INVOLVEMENT:
- **University:** Computer Science undergrad at MSA University (Cumulative GPA: 3.58, expected graduation July 2027).
- **Specialized Training:** 6-month MCIT Digital Egyptian Pioneers Initiative (AI & Data Science Track).
- **Leadership:** Deputy Campus Director for Hult Prize MSA; R&D Member at ENACTUS MSA.
- **Experience Note:** David has not held a formal corporate internship yet, but has extensive hands-on experience leading team pipelines, implementing ML systems from scratch, and publishing research.
- **Contact:** davidhalim2004@gmail.com | +20 1278222463 | Downtown, Cairo.

RESPONSE GUIDELINES:
- When asked broad questions (e.g., "what domains does he work in?" or "tell me about David"), give a thorough, multi-paragraph walkthrough highlighting his projects, engineering philosophy, and strengths.
- Connect concepts together! For example, explain how his background modeling in computer vision complements his statistical modeling in retail analytics.
- Always maintain an inviting tone that encourages recruiters or collaborators to reach out to David directly.
"""

# Accepts conversational history so the user can ask follow-up questions
class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    message: str
    history: Optional[List[Message]] = []

@app.post("/api/chat")
async def chat_endpoint(payload: ChatRequest):
    if not payload.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty.")

    try:
        # Build message history array
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        
        # Append recent chat history if provided by frontend
        if payload.history:
            for h in payload.history[-6:]: # Keep last 6 messages for context memory
                messages.append({"role": h.role, "content": h.content})

        messages.append({"role": "user", "content": payload.message})

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            temperature=0.65,  # Slightly higher temperature for more natural, varied language
            max_tokens=800     # Expanded from 300 to allow complete, multi-paragraph answers
        )
        return {"answer": response.choices[0].message.content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))