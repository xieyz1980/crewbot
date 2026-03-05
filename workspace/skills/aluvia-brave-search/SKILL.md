---
name: aluvia-brave-search
emoji: 🔍
description: Web search and content extraction via Brave Search API. Privacy-focused search engine with fast results and no tracking.
requires:
  env: [ALUVIA_API_KEY]
  bins: [curl, jq]
---

# Aluvia Brave Search

Privacy-focused web search using Brave Search API.

## Features

- 🔒 Privacy-protected searches
- ⚡ Fast results
- 📄 Content extraction
- 🚫 No tracking

## Setup

1. Get API key from https://api.aluvia.io
2. Set environment variable:
   ```bash
   export ALUVIA_API_KEY=your_key_here
   ```

## Usage

### Search
```bash
curl -s "https://api.aluvia.io/v1/search?q=your+query" \
  -H "Authorization: Bearer $ALUVIA_API_KEY"
```

### Extract Content
```bash
curl -s "https://api.aluvia.io/v1/extract?url=https://example.com" \
  -H "Authorization: Bearer $ALUVIA_API_KEY"
```

## API Endpoints

| Endpoint | Description |
|----------|-------------|
| `/v1/search` | Web search |
| `/v1/extract` | Content extraction |
| `/v1/suggest` | Search suggestions |

## Output Format

```json
{
  "results": [
    {
      "title": "...",
      "url": "...",
      "description": "..."
    }
  ]
}
```
