# AI Chatbot

A real-time AI chat application built with FastAPI, WebSockets, and Ollama. Features JWT authentication, PostgreSQL database, and a modern dark-themed UI.

![AI Chatbot](https://img.shields.io/badge/FastAPI-009688?style=flat&logo=fastapi&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=flat&logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat&logo=docker&logoColor=white)
![Ollama](https://img.shields.io/badge/Ollama-000000?style=flat&logo=ollama&logoColor=white)

## Features

- 🤖 **AI Chat** - Powered by Ollama (local LLM) with phi3, llama3, or any supported model
- 🔐 **Authentication** - JWT-based auth with secure password hashing (bcrypt)
- 💬 **Real-time** - WebSocket-based messaging with instant AI responses
- 🎨 **Modern UI** - Dark theme with responsive design
- 🐳 **Dockerized** - Full Docker Compose setup for easy deployment
- 🗄️ **Database** - PostgreSQL with SQLAlchemy ORM and Alembic migrations

## Tech Stack

| Component | Technology |
|-----------|------------|
| Backend | FastAPI 0.115 |
| Database | PostgreSQL 16 + SQLAlchemy 2.0 |
| AI/LLM | Ollama (phi3, llama3, etc.) |
| Auth | JWT (python-jose) + bcrypt |
| Real-time | WebSockets |
| Migrations | Alembic |
| Frontend | Vanilla JS + CSS |
| Container | Docker + Docker Compose |

## Quick Start

### Prerequisites

- Docker & Docker Compose
- Git

### 1. Clone and Configure

```bash
git clone https://github.com/yourusername/ai-chatbot.git
cd ai-chatbot

# Create environment file
cat > .env << 'EOF'
DATABASE_URL=postgresql://chatbot:chatbot123@db:5432/ai_chatbot
POSTGRES_USER=chatbot
POSTGRES_PASSWORD=chatbot123
POSTGRES_DB=ai_chatbot
SECRET_KEY=your-secret-key-change-in-production
OLLAMA_MODEL=phi3
EOF
```

### 2. Start the Application

```bash
# Start all services
docker-compose up -d

# Pull the AI model (first time only, ~2GB download)
docker exec ai-chatbot-ollama ollama pull phi3

# Check status
docker-compose ps
```

### 3. Open the App

Visit **http://localhost:8000** in your browser.

1. Click "Create Account" to register
2. Sign in with your credentials
3. Start chatting with the AI!

## Project Structure

```
ai-chatbot/
├── app/
│   ├── crud/              # Database operations
│   │   └── user.py
│   ├── models/            # SQLAlchemy models
│   │   └── user.py
│   ├── routers/           # API routes
│   │   ├── auth.py        # Login, token refresh
│   │   ├── chat.py        # WebSocket chat with AI
│   │   └── user.py        # User CRUD
│   ├── schemas/           # Pydantic schemas
│   │   ├── token.py
│   │   └── user.py
│   ├── services/          # External services
│   │   └── ollama.py      # Ollama LLM client
│   ├── auth.py            # JWT utilities
│   └── database.py        # DB configuration
├── alembic/               # Database migrations
├── static/                # Frontend files
│   └── index.html         # Chat UI
├── scripts/
│   └── setup-ollama.sh    # Model setup script
├── tests/                 # Test files
├── docker-compose.yml     # Docker services
├── Dockerfile
├── requirements.txt
└── main.py                # App entry point
```

## API Endpoints

### Authentication

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| `POST` | `/api/auth/login` | Login, get JWT token | No |
| `GET` | `/api/auth/me` | Get current user | Yes |

### Users

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| `POST` | `/api/users/` | Register new user | No |
| `GET` | `/api/users/{id}` | Get user by ID | Yes |

### Chat

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| `WebSocket` | `/api/chat` | AI chat connection | No |
| `GET` | `/api/chat/status` | Ollama status & models | No |

## Usage Examples

### Register a User

```bash
curl -X POST "http://localhost:8000/api/users/" \
  -H "Content-Type: application/json" \
  -d '{"username": "john", "email": "john@example.com", "password": "secret123"}'
```

### Login

```bash
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=john&password=secret123"
```

### Access Protected Endpoint

```bash
curl -X GET "http://localhost:8000/api/users/1" \
  -H "Authorization: Bearer <your-token>"
```

### WebSocket Chat (Python)

```python
import asyncio
import websockets
import json

async def chat():
    async with websockets.connect("ws://localhost:8000/api/chat") as ws:
        # Receive welcome message
        print(await ws.recv())
        
        # Send a message
        await ws.send(json.dumps({
            "type": "message",
            "text": "Hello! What can you help me with?",
            "username": "user"
        }))
        
        # Receive AI response
        response = await ws.recv()
        print(json.loads(response))

asyncio.run(chat())
```

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | Required |
| `SECRET_KEY` | JWT signing key | Required |
| `OLLAMA_BASE_URL` | Ollama API URL | `http://ollama:11434` |
| `OLLAMA_MODEL` | Default AI model | `phi3` |

### Changing the AI Model

```bash
# List available models
docker exec ai-chatbot-ollama ollama list

# Pull a different model
docker exec ai-chatbot-ollama ollama pull llama3.2
docker exec ai-chatbot-ollama ollama pull mistral
docker exec ai-chatbot-ollama ollama pull codellama

# Update .env
OLLAMA_MODEL=llama3.2

# Restart app
docker-compose restart app
```

## Database Migrations

```bash
# Create a new migration
docker exec ai-chatbot alembic revision --autogenerate -m "description"

# Apply migrations
docker exec ai-chatbot alembic upgrade head

# Rollback
docker exec ai-chatbot alembic downgrade -1
```

## Development

### Local Development (without Docker)

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start Ollama locally
ollama serve &
ollama pull phi3

# Set environment variables
export DATABASE_URL=postgresql://user:pass@localhost:5432/ai_chatbot
export SECRET_KEY=dev-secret-key
export OLLAMA_BASE_URL=http://localhost:11434

# Run the app
uvicorn main:app --reload
```

### Running Tests

```bash
# With Docker
docker exec ai-chatbot pytest -v

# Locally
pytest -v
```

## Deployment

### Docker Compose (Self-Hosted)

The included `docker-compose.yml` runs everything:

```bash
docker-compose up -d
```

**Services:**
- `app` - FastAPI application (port 8000)
- `db` - PostgreSQL database (port 5432)
- `ollama` - Ollama LLM server (port 11434)

### GPU Support (NVIDIA)

For faster AI responses, enable GPU in `docker-compose.yml`:

```yaml
ollama:
  deploy:
    resources:
      reservations:
        devices:
          - driver: nvidia
            count: all
            capabilities: [gpu]
```

### Cloud Deployment

For cloud hosting, consider:

| Platform | Notes |
|----------|-------|
| **Railway** | Easy Docker deployment, free tier available |
| **Render** | Free tier, auto-deploy from GitHub |
| **Fly.io** | Good for Docker apps, free tier |
| **DigitalOcean** | Droplets with Docker, $5-12/month |

**Note:** For cloud deployment, you may want to use a cloud LLM API (OpenAI, Anthropic) instead of Ollama to avoid GPU costs.

## Troubleshooting

### Ollama Connection Error

```
⚠️ Cannot connect to Ollama
```

**Solution:** Ensure Ollama is running:
```bash
docker-compose ps  # Check if ollama container is running
docker exec ai-chatbot-ollama ollama list  # Check if model is pulled
```

### Model Not Found (404)

```
⚠️ Ollama error: 404
```

**Solution:** Pull the model:
```bash
docker exec ai-chatbot-ollama ollama pull phi3
```

### Database Connection Error

**Solution:** Check PostgreSQL is running:
```bash
docker-compose logs db
```

## License

See [LICENSE](LICENSE) file for details.

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request
