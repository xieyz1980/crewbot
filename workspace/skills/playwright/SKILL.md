---
name: playwright
emoji: 🎭
description: Browser automation using Playwright - supports Chromium, Firefox, and WebKit. Cross-platform web testing and automation.
requires:
  bins: [npx]
---

# Playwright Browser Automation

## Installation

```bash
npm install -g @playwright/test
npx playwright install chromium
```

## Quick Start

```bash
# Run a simple script
npx playwright open example.com

# Codegen - record your actions
npx playwright codegen example.com

# Run tests
npx playwright test
```

## Features

- Multi-browser support (Chromium, Firefox, WebKit)
- Auto-wait for elements
- Mobile emulation
- Headless or headed mode
- Screenshots and videos
- Network interception
- Parallel execution

## Docs
https://playwright.dev
