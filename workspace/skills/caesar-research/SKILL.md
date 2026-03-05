---
name: caesar-research
emoji: 🧠
description: Deep research using the Caesar API. Run queries, follow up with chat, brainstorm ideas, and manage research collections.
requires:
  env: [CAESAR_API_KEY]
  bins: [curl, jq]
---

# Caesar Research

AI-powered deep research assistant using the Caesar API.

## Features

- 🔬 Deep research queries
- 💬 Interactive follow-up chat
- 💡 Brainstorming sessions
- 📁 Research collections management
- 📊 Structured reports

## Setup

1. Sign up at https://caesar.io
2. Get API key from dashboard
3. Set environment variable:
   ```bash
   export CAESAR_API_KEY=your_key_here
   ```

## Usage

### Run Research Query
```bash
curl -s -X POST "https://api.caesar.io/v1/research" \
  -H "Authorization: Bearer $CAESAR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Latest developments in quantum computing",
    "depth": "comprehensive"
  }'
```

### Chat Follow-up
```bash
curl -s -X POST "https://api.caesar.io/v1/chat" \
  -H "Authorization: Bearer $CAESAR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "session_123",
    "message": "Tell me more about quantum supremacy"
  }'
```

### Brainstorm
```bash
curl -s -X POST "https://api.caesar.io/v1/brainstorm" \
  -H "Authorization: Bearer $CAESAR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "Renewable energy innovations",
    "angles": ["technical", "economic", "environmental"]
  }'
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/v1/research` | POST | Run research query |
| `/v1/chat` | POST | Interactive chat |
| `/v1/brainstorm` | POST | Brainstorm ideas |
| `/v1/collections` | GET/POST | Manage collections |

## Output Format

```json
{
  "research_id": "res_123",
  "summary": "...",
  "findings": [
    {
      "title": "...",
      "content": "...",
      "sources": [...]
    }
  ],
  "suggested_followups": [...]
}
```

## Research Depth Levels

| Level | Description |
|-------|-------------|
| `quick` | Fast overview |
| `standard` | Balanced depth |
| `comprehensive` | In-depth analysis |
| `exhaustive` | Maximum coverage |
