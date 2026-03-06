---
name: arxiv-watcher
emoji: 📚
description: Search and summarize papers from arXiv. Monitor new publications, get paper abstracts, and track research topics.
requires:
  bins: [curl, jq]
---

# arXiv Watcher

Search and monitor academic papers from arXiv.org.

## Features

- 🔍 Search arXiv papers by keyword
- 📰 Monitor new publications
- 📝 Get paper abstracts
- 🏷️ Filter by category
- 📊 Track research trends

## Usage

### Search Papers
```bash
# Search by keyword
curl -s "http://export.arxiv.org/api/query?search_query=all:machine+learning&start=0&max_results=10"

# Search by category
curl -s "http://export.arxiv.org/api/query?search_query=cat:cs.AI&start=0&max_results=10"

# Search by author
curl -s "http://export.arxiv.org/api/query?search_query=au:Hinton&start=0&max_results=10"
```

### Get Paper Details
```bash
# Get specific paper by ID
curl -s "http://export.arxiv.org/api/query?id_list=2101.00001"
```

### Categories

| Code | Description |
|------|-------------|
| cs.AI | Artificial Intelligence |
| cs.CL | Computation and Language |
| cs.CV | Computer Vision |
| cs.LG | Machine Learning |
| cs.SE | Software Engineering |
| quant-ph | Quantum Physics |

## Example Output

```xml
<entry>
  <id>http://arxiv.org/abs/2101.00001</id>
  <title>Paper Title</title>
  <summary>Paper abstract...</summary>
  <author><name>Author Name</name></author>
  <published>2021-01-01T00:00:00Z</published>
</entry>
```

## Python Script

```python
import requests
import xml.etree.ElementTree as ET

def search_arxiv(query, max_results=10):
    url = f"http://export.arxiv.org/api/query?search_query=all:{query}&start=0&max_results={max_results}"
    response = requests.get(url)
    root = ET.fromstring(response.content)
    # Parse results...
    return papers
```
