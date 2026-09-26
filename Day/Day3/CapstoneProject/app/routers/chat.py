# app/routers/chat.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from groq import Groq

from app.config import settings


router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)


# --------------------------------------------------
# Groq Client
# --------------------------------------------------

client = Groq(
    api_key=settings.GROQ_API_KEY
)

model = settings.GROQ_MODEL


# --------------------------------------------------
# System Prompt
# --------------------------------------------------

SYSTEM_PROMPT = """
You are a technical assistant for a web application.

You are ONLY allowed to answer questions related to:

1. React
2. FastAPI
3. MongoDB

You may also answer questions where these technologies
are used together, such as React with FastAPI,
FastAPI with MongoDB, CRUD applications,
authentication and JWT, REST APIs,
frontend/backend integration, and Docker deployment
of React, FastAPI and MongoDB.

If the question is unrelated to these technologies,
respond exactly with:

"I can answer only questions related to React, FastAPI and MongoDB."

Keep answers clear and suitable for a beginner.
"""


# --------------------------------------------------
# Pydantic Models
# --------------------------------------------------

class PromptRequest(BaseModel):
    prompt: str


class PromptResponse(BaseModel):
    response: str
    model: str


# --------------------------------------------------
# POST /chat
# --------------------------------------------------

@router.post("", response_model=PromptResponse)
def chat(request: PromptRequest):

    try:

        completion = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT,
                },
                {
                    "role": "user",
                    "content": request.prompt,
                },
            ],
        )

        return PromptResponse(
            response=completion.choices[0].message.content,
            model=model,
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Groq API error: {str(e)}",
        )
