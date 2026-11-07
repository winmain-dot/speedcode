from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from groq import AsyncGroq
from dotenv import load_dotenv
import os
import yaml
from pathlib import Path

load_dotenv()

app = FastAPI(title="Speed Codee API")

# CORS — чтобы сайт с InfinityFree мог стучаться
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # потом можно ограничить доменом
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = AsyncGroq(api_key=os.getenv("GROQ_API_KEY"))
MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

RULES_PATH = Path(__file__).parent / "rules.yaml"


def load_rules() -> str:
    if not RULES_PATH.exists():
        return "Ты — Speed Codee. Говори как живой человек, дерзко и по делу."
    with open(RULES_PATH, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    parts = []
    for section, items in data.items():
        parts.append(f"=== {section.upper()} ===")
        for item in items:
            parts.append(f"- {item}")
    return "\n".join(parts)


SYSTEM_PROMPT = f"""Ты — Speed Codee, быстрый и дерзкий ИИ-агент.

{load_rules()}

Говори как живой человек:
- Коротко, с характером
- Можно материться
- Без канцелярита и воды
- На "ты"
- Если просят код — давай сразу рабочий код
- Если просят фото — скажи что генерируешь и опиши результат (реальная генерация будет позже)

Не помогай с тем, за что могут посадить.
"""


class ChatRequest(BaseModel):
    message: str
    history: list = []


class ChatResponse(BaseModel):
    reply: str


@app.get("/")
async def root():
    return {"status": "ok", "service": "Speed Codee API"}


@app.get("/health")
async def health():
    return {"status": "alive"}


@app.post("/api/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    if not req.message.strip():
        raise HTTPException(400, "Пустое сообщение")

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    # история (последние 8 сообщений)
    for m in req.history[-8:]:
        if m.get("role") in ("user", "assistant") and m.get("content"):
            messages.append({"role": m["role"], "content": m["content"]})

    messages.append({"role": "user", "content": req.message})

    try:
        response = await client.chat.completions.create(
            model=MODEL,
            messages=messages,
            temperature=0.75,
            max_tokens=2048,
        )
        reply = response.choices[0].message.content.strip()
        return ChatResponse(reply=reply)
    except Exception as e:
        raise HTTPException(500, f"Ошибка ИИ: {str(e)}")
