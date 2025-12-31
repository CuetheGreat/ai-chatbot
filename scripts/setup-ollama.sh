#!/bin/bash
# Script to pull the default model into Ollama

MODEL=${OLLAMA_MODEL:-phi3}
OLLAMA_HOST=${OLLAMA_BASE_URL:-http://ollama:11434}

echo "Waiting for Ollama to be ready..."
until curl -s "$OLLAMA_HOST/api/tags" > /dev/null 2>&1; do
    sleep 2
done

echo "Ollama is ready. Checking for model: $MODEL"

# Check if model exists
if curl -s "$OLLAMA_HOST/api/tags" | grep -q "\"name\":\"$MODEL"; then
    echo "Model $MODEL already exists."
else
    echo "Pulling model $MODEL... (this may take a few minutes)"
    curl -X POST "$OLLAMA_HOST/api/pull" -d "{\"name\": \"$MODEL\"}"
    echo "Model $MODEL pulled successfully!"
fi

