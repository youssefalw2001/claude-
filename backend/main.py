"""
Ollama Fox Platform - FastAPI Backend
Supports multiple AI providers: Ollama (local), Groq, OpenRouter
"""

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional, List, Dict
import httpx
import json
import os
from fox_persona import FOX_SYSTEM_PROMPT

app = FastAPI(title="Ollama Fox Platform")

# CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_CLOUD_API_KEY = os.getenv("OLLAMA_CLOUD_API_KEY", "")
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")

# Models
class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    message: str
    provider: str = "ollama"  # ollama, ollama-cloud, groq, openrouter
    model: Optional[str] = None
    stream: bool = False
    history: List[ChatMessage] = []
    api_key: Optional[str] = None  # For client-side API keys

class ModelInfo(BaseModel):
    name: str
    provider: str
    size: Optional[str] = None

# Active WebSocket connections
active_connections: List[WebSocket] = []

@app.get("/")
async def read_root():
    """Serve the frontend"""
    return FileResponse("../frontend/index.html")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "fox": "ready to fuck shit up"}

@app.get("/api/models")
async def list_models():
    """List available models from all providers"""
    models = []
    
    # Ollama local models
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=5.0)
            if response.status_code == 200:
                ollama_models = response.json().get("models", [])
                models.extend([
                    ModelInfo(
                        name=m["name"],
                        provider="ollama",
                        size=m.get("size", "unknown")
                    ) for m in ollama_models
                ])
    except Exception as e:
        print(f"Failed to fetch Ollama local models: {e}")
    
    # Ollama Cloud models (always available)
    models.extend([
        ModelInfo(name="llama3.1:70b", provider="ollama-cloud", size="70B"),
        ModelInfo(name="llama3.1:8b", provider="ollama-cloud", size="8B"),
        ModelInfo(name="qwen2.5:72b", provider="ollama-cloud", size="72B"),
        ModelInfo(name="deepseek-v3", provider="ollama-cloud", size="671B"),
        ModelInfo(name="mistral:7b", provider="ollama-cloud", size="7B"),
        ModelInfo(name="gemma2:27b", provider="ollama-cloud", size="27B"),
    ])
    
    # Groq models (if API key provided)
    if GROQ_API_KEY:
        models.extend([
            ModelInfo(name="llama-3.1-70b-versatile", provider="groq"),
            ModelInfo(name="llama-3.1-8b-instant", provider="groq"),
            ModelInfo(name="mixtral-8x7b-32768", provider="groq"),
        ])
    
    # OpenRouter models (if API key provided)
    if OPENROUTER_API_KEY:
        models.extend([
            ModelInfo(name="meta-llama/llama-3.1-70b-instruct", provider="openrouter"),
            ModelInfo(name="meta-llama/llama-3.1-8b-instruct", provider="openrouter"),
            ModelInfo(name="anthropic/claude-3.5-sonnet", provider="openrouter"),
        ])
    
    return {"models": models}

@app.post("/api/chat")
async def chat(request: ChatRequest):
    """Chat endpoint - routes to appropriate provider"""
    
    if request.provider == "ollama":
        return await chat_ollama(request)
    elif request.provider == "ollama-cloud":
        return await chat_ollama_cloud(request)
    elif request.provider == "groq":
        return await chat_groq(request)
    elif request.provider == "openrouter":
        return await chat_openrouter(request)
    else:
        raise HTTPException(status_code=400, detail="Invalid provider")

async def chat_ollama(request: ChatRequest):
    """Chat with Ollama"""
    model = request.model or "llama3.2:3b"
    
    # Build conversation context
    conversation = f"{FOX_SYSTEM_PROMPT}\n\n"
    for msg in request.history:
        role = "Jack" if msg.role == "user" else "Fox"
        conversation += f"{role}: {msg.content}\n"
    conversation += f"Jack: {request.message}\nFox:"
    
    try:
        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(
                f"{OLLAMA_BASE_URL}/api/generate",
                json={
                    "model": model,
                    "prompt": conversation,
                    "stream": False,
                }
            )
            
            if response.status_code == 200:
                result = response.json()
                return {"response": result.get("response", "")}
            else:
                raise HTTPException(status_code=response.status_code, detail="Ollama API error")
    
    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail="Ollama request timed out")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ollama error: {str(e)}")

async def chat_ollama_cloud(request: ChatRequest):
    """Chat with Ollama Cloud"""
    # Get API key from request or environment
    api_key = request.api_key or OLLAMA_CLOUD_API_KEY
    
    if not api_key:
        raise HTTPException(status_code=400, detail="Ollama Cloud API key not configured")
    
    model = request.model or "llama3.1:8b"
    
    # Build messages in OpenAI format (Ollama Cloud uses this)
    messages = [{"role": "system", "content": FOX_SYSTEM_PROMPT}]
    messages.extend([{"role": msg.role, "content": msg.content} for msg in request.history])
    messages.append({"role": "user", "content": request.message})
    
    try:
        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(
                "https://api.ollama.com/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": model,
                    "messages": messages,
                    "temperature": 0.7,
                    "max_tokens": 4096
                }
            )
            
            if response.status_code == 200:
                result = response.json()
                return {"response": result["choices"][0]["message"]["content"]}
            else:
                error_detail = response.text
                raise HTTPException(
                    status_code=response.status_code, 
                    detail=f"Ollama Cloud API error: {error_detail}"
                )
    
    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail="Ollama Cloud request timed out")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ollama Cloud error: {str(e)}")

async def chat_groq(request: ChatRequest):
    """Chat with Groq"""
    if not GROQ_API_KEY:
        raise HTTPException(status_code=400, detail="Groq API key not configured")
    
    model = request.model or "llama-3.1-70b-versatile"
    
    messages = [{"role": "system", "content": FOX_SYSTEM_PROMPT}]
    messages.extend([{"role": msg.role, "content": msg.content} for msg in request.history])
    messages.append({"role": "user", "content": request.message})
    
    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {GROQ_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": model,
                    "messages": messages,
                    "temperature": 0.7,
                    "max_tokens": 4096
                }
            )
            
            if response.status_code == 200:
                result = response.json()
                return {"response": result["choices"][0]["message"]["content"]}
            else:
                raise HTTPException(status_code=response.status_code, detail=f"Groq API error: {response.text}")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Groq error: {str(e)}")

async def chat_openrouter(request: ChatRequest):
    """Chat with OpenRouter"""
    if not OPENROUTER_API_KEY:
        raise HTTPException(status_code=400, detail="OpenRouter API key not configured")
    
    model = request.model or "meta-llama/llama-3.1-70b-instruct"
    
    messages = [{"role": "system", "content": FOX_SYSTEM_PROMPT}]
    messages.extend([{"role": msg.role, "content": msg.content} for msg in request.history])
    messages.append({"role": "user", "content": request.message})
    
    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                    "Content-Type": "application/json",
                    "HTTP-Referer": "https://github.com/youssefalw2001/claude-",
                    "X-Title": "Ollama Fox Platform"
                },
                json={
                    "model": model,
                    "messages": messages,
                    "temperature": 0.7,
                }
            )
            
            if response.status_code == 200:
                result = response.json()
                return {"response": result["choices"][0]["message"]["content"]}
            else:
                raise HTTPException(status_code=response.status_code, detail=f"OpenRouter API error: {response.text}")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OpenRouter error: {str(e)}")

@app.websocket("/ws/chat")
async def websocket_chat(websocket: WebSocket):
    """WebSocket for streaming chat"""
    await websocket.accept()
    active_connections.append(websocket)
    
    try:
        while True:
            data = await websocket.receive_text()
            request_data = json.loads(data)
            
            # Handle streaming response
            if request_data.get("provider") == "ollama":
                model = request_data.get("model", "llama3.2:3b")
                message = request_data.get("message", "")
                
                conversation = f"{FOX_SYSTEM_PROMPT}\n\nJack: {message}\nFox:"
                
                async with httpx.AsyncClient(timeout=120.0) as client:
                    async with client.stream(
                        "POST",
                        f"{OLLAMA_BASE_URL}/api/generate",
                        json={"model": model, "prompt": conversation, "stream": True}
                    ) as response:
                        async for line in response.aiter_lines():
                            if line:
                                chunk = json.loads(line)
                                if "response" in chunk:
                                    await websocket.send_json({"type": "chunk", "content": chunk["response"]})
                                if chunk.get("done", False):
                                    await websocket.send_json({"type": "done"})
            
    except WebSocketDisconnect:
        active_connections.remove(websocket)
    except Exception as e:
        print(f"WebSocket error: {e}")
        if websocket in active_connections:
            active_connections.remove(websocket)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
