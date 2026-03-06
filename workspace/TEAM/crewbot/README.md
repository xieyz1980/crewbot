# CrewBot - Multi-Agent Collaboration Platform

## Installation

```bash
pip install -r requirements.txt
```

## Environment Variables

```bash
# OpenAI
export OPENAI_API_KEY="your-openai-api-key"
export OPENAI_DEFAULT_MODEL="gpt-4o"

# Anthropic
export ANTHROPIC_API_KEY="your-anthropic-api-key"
export ANTHROPIC_DEFAULT_MODEL="claude-3-5-sonnet-20241022"
```

## Quick Start

```python
import asyncio
from crewbot.providers import create_openai_client, create_anthropic_client

async def main():
    # OpenAI
    openai_client = create_openai_client()
    response = await openai_client.simple_chat("Hello!")
    print(f"OpenAI: {response}")
    
    # Claude
    claude_client = create_anthropic_client()
    response = await claude_client.simple_chat("Hello!")
    print(f"Claude: {response}")

asyncio.run(main())
```
