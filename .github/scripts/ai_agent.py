name: Local Offline AI Code Reviewer

on:
  push:
    branches: [ "main" ]
  workflow_dispatch:

jobs:
  local-ai-patcher:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Code
        uses: actions/checkout@v4
        with:
          token: ${{ secrets.MY_GITHUB_PAT }}
          fetch-depth: 0

      - name: Install Ollama (Local AI Engine)
        run: |
          curl -fsSL https://ollama.com | sh
          # Start the background local AI server
          ollama serve &
          # Wait for server startup
          sleep 5

      - name: Download Lightweight Code Model
        # Downloads Qwen2.5-Coder (1.5B), optimized for code processing on standard hardware
        run: ollama pull qwen2.5-coder:1.5b

      - name: Set Up Python Environment
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Run Local AI Patching Script
        env:
          GITHUB_TOKEN: ${{ secrets.MY_GITHUB_PAT }}
        run: python .github/scripts/local_ai_agent.py
