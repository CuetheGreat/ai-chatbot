import json
from typing import Dict, List

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.services.ollama import ollama_service

router = APIRouter()

# Store connected clients and their conversation history
connected_clients: Dict[WebSocket, List[dict]] = {}

SYSTEM_PROMPT = """You are a helpful, friendly AI assistant. Keep your responses concise and conversational. 
If you don't know something, say so honestly. Be helpful but don't be overly verbose."""


@router.websocket("/chat")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_clients[websocket] = []

    # Send welcome message
    welcome = {
        "type": "system",
        "text": "Connected to AI Chat! Send a message to start chatting.",
    }
    await websocket.send_text(json.dumps(welcome))

    try:
        while True:
            data = await websocket.receive_text()

            # Parse the incoming message
            try:
                message_data = json.loads(data)
                user_message = message_data.get("text", data)
                username = message_data.get("username", "User")
            except json.JSONDecodeError:
                user_message = data
                username = "User"

            # Skip empty messages or join messages
            if not user_message or message_data.get("type") == "join":
                continue

            # Add user message to history
            connected_clients[websocket].append(
                {"role": "user", "content": user_message}
            )

            # Keep only last 10 messages for context
            if len(connected_clients[websocket]) > 20:
                connected_clients[websocket] = connected_clients[websocket][-20:]

            # Get AI response
            ai_response = await ollama_service.chat(
                message=user_message,
                system_prompt=SYSTEM_PROMPT,
                conversation_history=connected_clients[websocket][:-1],  # Exclude current message
            )

            # Add AI response to history
            connected_clients[websocket].append(
                {"role": "assistant", "content": ai_response}
            )

            # Send AI response back to the user
            response = {
                "type": "message",
                "text": ai_response,
                "username": "AI Assistant",
                "isAI": True,
            }
            await websocket.send_text(json.dumps(response))

    except WebSocketDisconnect:
        connected_clients.pop(websocket, None)


@router.get("/chat/status")
async def chat_status():
    """Check if Ollama is available and list models."""
    available = await ollama_service.is_available()
    models = await ollama_service.list_models() if available else []
    return {
        "ollama_available": available,
        "current_model": ollama_service.model,
        "available_models": models,
        "connected_clients": len(connected_clients),
    }
