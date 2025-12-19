from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, Request, Header, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Dict, Optional
import uvicorn
import json

app = FastAPI(title="Interview.CV Python Backend", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "Interview.CV Python Backend", "version": "1.0.0"}

@app.get("/")
async def root():
    return {
        "name": "Interview.CV Python Backend",
        "version": "1.0.0",
        "features": [
            "Agora Conversational AI Integration",
            "Custom LLM Service (OpenAI-Compatible)",
            "Live Transcript Streaming",
            "Context-Aware Processing",
            "Audio Output with Word Timestamps",
            "Payment Processing (Razorpay, Stripe)",
            "Cloudflare R2 Storage",
            "PostgreSQL Database"
        ],
        "docs": "/docs",
        "github": "https://github.com/karthikeyanveeran/interview-cv-python-backend"
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
