import uuid
import json
from flask import Blueprint, request, jsonify
from ai.llm_engine import LLMEngine
from ai.rag_engine import RAGEngine
from ai.prompts import SYSTEM_PROMPT
from database.models import db, ChatHistory

chat_bp = Blueprint("chat", __name__)
llm = LLMEngine()
rag = RAGEngine()


@chat_bp.route("/api/stadiums", methods=["GET"])
def list_stadiums():
    return jsonify({"stadiums": rag.get_stadium_list()})


@chat_bp.route("/api/stadium/select", methods=["POST"])
def select_stadium():
    data = request.get_json()
    if not data or not data.get("stadium_id"):
        return jsonify({"error": "stadium_id required"}), 400
    rag.set_stadium(data["stadium_id"])
    ctx = rag.get_stadium_context()
    return jsonify({"status": "ok", "stadium": ctx})


@chat_bp.route("/api/stadium/context", methods=["GET"])
def stadium_context():
    return jsonify({"stadium": rag.get_stadium_context()})


@chat_bp.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body required"}), 400

    message = data.get("message", "").strip()
    session_id = data.get("session_id", str(uuid.uuid4()))
    language = data.get("language", "auto")
    stadium_id = data.get("stadium_id", rag.stadium_id)

    if not message:
        return jsonify({"error": "Message is required"}), 400

    if len(message) > 2000:
        return jsonify({"error": "Message too long (max 2000 characters)"}), 400

    if stadium_id != rag.stadium_id:
        rag.set_stadium(stadium_id)

    if language == "auto":
        language = llm.detect_language(message)

    intent = llm.classify_intent(message)

    context = rag.retrieve_context(message)

    stadium_info = rag.get_stadium_context()
    context_str = (
        f"Stadium: {stadium_info['name']} ({stadium_info['location']})\n"
        f"Capacity: {stadium_info['capacity']}\n"
        f"User Intent: {intent}\n"
    )
    if context["relevant_zones"]:
        context_str += f"Relevant Context: {json.dumps(context['relevant_zones'][:3])}\n"
    context_str += f"Crowd Summary:\n{rag.get_crowd_summary()}\n"

    user_prompt = f"User Language: {language}\nUser Message: {message}\n\nStadium Context:\n{context_str}"

    response = llm.generate(SYSTEM_PROMPT, user_prompt, language)

    chat_record = ChatHistory(
        session_id=session_id,
        role="user",
        message=message,
        language=language,
    )
    db.session.add(chat_record)

    chat_record = ChatHistory(
        session_id=session_id,
        role="assistant",
        message=response,
        language=language,
    )
    db.session.add(chat_record)
    db.session.commit()

    return jsonify({
        "response": response,
        "session_id": session_id,
        "intent": intent,
        "language": language,
        "stadium": stadium_info["name"],
    })


@chat_bp.route("/api/chat/history", methods=["GET"])
def chat_history():
    session_id = request.args.get("session_id")
    if not session_id:
        return jsonify({"error": "session_id required"}), 400
    history = ChatHistory.query.filter_by(session_id=session_id)\
        .order_by(ChatHistory.timestamp.asc()).limit(50).all()
    return jsonify([h.to_dict() for h in history])


@chat_bp.route("/api/intent", methods=["POST"])
def detect_intent():
    data = request.get_json()
    if not data or not data.get("message"):
        return jsonify({"error": "Message required"}), 400
    intent = llm.classify_intent(data["message"])
    language = llm.detect_language(data["message"])
    return jsonify({"intent": intent, "language": language})
