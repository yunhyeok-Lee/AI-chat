"""Minimal Flask server to expose the chatbot with a simple web frontend."""
from __future__ import annotations

import os
from typing import Any, Dict, Tuple
from uuid import uuid4

from flask import Flask, jsonify, make_response, request, send_from_directory
from dotenv import load_dotenv, find_dotenv
from werkzeug.exceptions import HTTPException

from chat_backend import ChatSession

# .env 파일 로드
load_dotenv(find_dotenv(), override=True)

app = Flask(__name__, static_folder="static", static_url_path="/static")

# ✅ /api/chat 과 /api/chat/ 를 모두 허용하여 리다이렉트(HTML) 방지
app.url_map.strict_slashes = False

# In-memory sessions
_sessions: dict[str, ChatSession] = {}


def _get_or_create_session(session_id: str | None) -> Tuple[str, ChatSession]:
    """Return the chat session for the current browser session."""
    sid = session_id or uuid4().hex
    session = _sessions.get(sid)
    if session is None:
        session = ChatSession()
        _sessions[sid] = session
    return sid, session


# ✅ 전역 에러 핸들러: 항상 JSON으로 응답(HTML 에러 페이지 방지)
@app.errorhandler(HTTPException)
def handle_http_error(e: HTTPException):
    return jsonify({"error": e.name, "status": e.code}), e.code


@app.errorhandler(Exception)
def handle_all_error(e: Exception):
    # debug=True 일 때도 HTML 디버거 페이지로 가지 않도록 JSON 강제
    return jsonify({"error": "internal_server_error"}), 500


@app.route("/", methods=["GET"])
def index() -> Any:
    """Serve the static chat UI."""
    return send_from_directory(app.static_folder, "index.html")


# ✅ GET으로 잘못 호출했을 때도 HTML이 아니라 JSON으로 명확히 알려주기
@app.route("/api/chat", methods=["GET"])
def chat_get_hint() -> Any:
    return jsonify({"error": "Use POST with JSON payload: { \"message\": \"...\" }"}), 405


@app.route("/api/chat", methods=["POST"])
def chat_completion() -> Any:
    """Receive a chat message and respond with the assistant reply."""
    payload: Dict[str, Any] = request.get_json(force=True, silent=True) or {}
    message = (payload.get("message") or "").strip()
    if not message:
        return jsonify({"error": "Message is required."}), 400

    session_id, session = _get_or_create_session(request.cookies.get("chat_session"))
    try:
        assistant_reply = session.send(message)
    except Exception as exc:  # pragma: no cover - network/API errors
        # 롤백: 바로 직전 유저 메시지 제거
        if len(session.messages) > 1:
            session.messages.pop()
        return jsonify({"error": f"OpenAI API request failed: {exc}"}), 502

    response = make_response(
        jsonify(
            {
                "reply": assistant_reply,
                "model": session.model_name,
                "history": session.messages[-4:],  # send a small tail for context
            }
        )
    )
    response.set_cookie(
        "chat_session",
        session_id,
        max_age=60 * 60 * 24,
        httponly=True,
        samesite="Lax",
    )
    return response


# (선택) 간단 헬스체크: 프록시/경로 테스트 용
@app.route("/api/health", methods=["GET"])
def health() -> Any:
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    host = os.getenv("CHATBOT_HOST", "127.0.0.1")
    port = int(os.getenv("CHATBOT_PORT", "8000"))
    debug = os.getenv("CHATBOT_DEBUG") == "1"
    app.run(host=host, port=port, debug=debug)
