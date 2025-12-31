import os
from typing import AsyncGenerator, Optional

import httpx
from dotenv import load_dotenv

load_dotenv()

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://ollama:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "phi3")


class OllamaService:
    def __init__(self, base_url: str = OLLAMA_BASE_URL, model: str = OLLAMA_MODEL):
        self.base_url = base_url
        self.model = model
        self.client = httpx.AsyncClient(timeout=60.0)

    async def chat(
        self,
        message: str,
        system_prompt: Optional[str] = None,
        conversation_history: Optional[list] = None,
    ) -> str:
        """Send a message to Ollama and get a response."""
        messages = []

        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})

        if conversation_history:
            messages.extend(conversation_history)

        messages.append({"role": "user", "content": message})

        try:
            response = await self.client.post(
                f"{self.base_url}/api/chat",
                json={
                    "model": self.model,
                    "messages": messages,
                    "stream": False,
                },
            )
            response.raise_for_status()
            data = response.json()
            return data.get("message", {}).get("content", "I couldn't generate a response.")
        except httpx.ConnectError:
            return "⚠️ Cannot connect to Ollama. Make sure Ollama is running (`ollama serve`)."
        except httpx.HTTPStatusError as e:
            return f"⚠️ Ollama error: {e.response.status_code}"
        except Exception as e:
            return f"⚠️ Error: {str(e)}"

    async def chat_stream(
        self,
        message: str,
        system_prompt: Optional[str] = None,
        conversation_history: Optional[list] = None,
    ) -> AsyncGenerator[str, None]:
        """Stream a response from Ollama."""
        messages = []

        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})

        if conversation_history:
            messages.extend(conversation_history)

        messages.append({"role": "user", "content": message})

        try:
            async with self.client.stream(
                "POST",
                f"{self.base_url}/api/chat",
                json={
                    "model": self.model,
                    "messages": messages,
                    "stream": True,
                },
            ) as response:
                response.raise_for_status()
                async for line in response.aiter_lines():
                    if line:
                        import json
                        data = json.loads(line)
                        content = data.get("message", {}).get("content", "")
                        if content:
                            yield content
        except httpx.ConnectError:
            yield "⚠️ Cannot connect to Ollama. Make sure Ollama is running (`ollama serve`)."
        except Exception as e:
            yield f"⚠️ Error: {str(e)}"

    async def is_available(self) -> bool:
        """Check if Ollama is available."""
        try:
            response = await self.client.get(f"{self.base_url}/api/tags")
            return response.status_code == 200
        except Exception:
            return False

    async def list_models(self) -> list:
        """List available models."""
        try:
            response = await self.client.get(f"{self.base_url}/api/tags")
            response.raise_for_status()
            data = response.json()
            return [model["name"] for model in data.get("models", [])]
        except Exception:
            return []

    async def close(self):
        """Close the HTTP client."""
        await self.client.aclose()


# Singleton instance
ollama_service = OllamaService()

