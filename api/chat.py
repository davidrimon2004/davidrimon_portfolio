import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI

app = FastAPI()

# Enable CORS so your GitHub Pages site can talk to this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with "https://<your-username>.github.io" in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize OpenAI client (configured here for Groq's free API, or default OpenAI)
client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"  # Omit base_url if using OpenAI directly
)

SYSTEM_PROMPT = """
You are the AI portfolio assistant for David Rimon Youssef, an ML & Computer Science student at MSA University (GPA 3.58).
Answer questions about David professionally, concisely, and accurately based on his context below.

CONTEXT:
- Target: ML / AI / Data Science Internships.
- Projects:
  1. Surveillance Anomaly Detection (Weakly supervised 3D CNN pipeline on UCF-Crime dataset, paper under peer review at CESS 2026).
  2. Retail Sales Prediction System (XGBoost forecasting on 58.5M rows, MAE 0.36, R2 0.88 across 10 store segments).
  3. Cairo2Capital Transit System (Full-stack fare system with OOP architecture, PHP/MySQL).
- Skills: Python, PyTorch, TensorFlow, scikit-learn, XGBoost, C++, SQL, Git.
- Experience / Internships: Has not held a corporate internship yet. Highlight his 6-month MCIT Digital Egyptian Pioneers Initiative (AI Track) and team project leadership.
- Leadership: Deputy Campus Director at Hult Prize MSA, R&D Member at ENACTUS MSA.
- Contact: davidhalim2004@gmail.com | +20 1278222463 | Downtown, Cairo.

If asked about vague topics like "areas he works best in", summarize his top strengths in Machine Learning, Computer Vision, and Data Science.
If the answer is completely unknown, state politely that you don't have that detail and suggest emailing David directly.
"""

class ChatRequest(BaseModel):
    message: str

@app.post("/api/chat")
async def chat_endpoint(payload: ChatRequest):
    if not payload.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty.")

    try:
       response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",  # Free on Groq Cloud API
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": payload.message}
    ],
    temperature=0.2,
    max_tokens=300
)
        return {"answer": response.choices[0].message.content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))