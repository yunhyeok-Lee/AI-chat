"""Shared chat utilities for CLI and web frontends."""
from __future__ import annotations

import os
from typing import Sequence, List, Dict

from openai import OpenAI
from dotenv import load_dotenv, find_dotenv

# .env 파일 로드
load_dotenv(find_dotenv(), override=True)

# Commands that terminate the chat loop when entered by the user.
EXIT_COMMANDS = {"exit", "quit", "q", "bye"}


def _ensure_api_key() -> None:
    """Validate that an API key is configured before performing requests."""
    if not os.getenv("OPENAI_API_KEY"):
        raise ValueError("OpenAI API 키가 설정되지 않았습니다. .env 파일에 OPENAI_API_KEY를 설정해주세요.")


def _coerce_to_text(parts: Sequence) -> str:
    """Convert the response content into a printable string."""
    if isinstance(parts, str):
        return parts
    chunks: List[str] = []
    for part in parts or ():
        text = getattr(part, "text", None)
        if text is None and isinstance(part, dict):
            text = part.get("text")
        if text is None:
            text = str(part)
        chunks.append(text)
    return "".join(chunks)


class ChatSession:
    """Wrap OpenAI chat completion calls with simple conversational memory."""

    def __init__(self, model: str | None = None) -> None:
        _ensure_api_key()
        self._client = OpenAI()
        default_model = "gpt-4o-mini"
        self.model_name = os.getenv("OPENAI_MODEL", model or default_model)
        self.messages: List[Dict[str, str]] = [
            {
                "role": "system",
                "content": "당신은 친근하고 도움이 되는 한국어 AI 어시스턴트입니다. 자연스럽고 따뜻한 톤으로 대화하며, 질문에 대해 정확하고 유용한 답변을 제공합니다.",
            }
        ]

    def send(self, user_message: str) -> str:
        """Submit a user message, persist assistant reply, and return the text."""
        self.messages.append({"role": "user", "content": user_message})
        completion = self._client.chat.completions.create(
            model=self.model_name,
            messages=self.messages,
            temperature=0.7,
        )
        assistant_message = completion.choices[0].message
        assistant_text = _coerce_to_text(getattr(assistant_message, "content", ""))
        self.messages.append({"role": "assistant", "content": assistant_text})
        return assistant_text
