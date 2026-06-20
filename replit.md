# LexWatch

AI-powered regulatory compliance monitoring system built for UiPath AgentHack 2026. Automatically monitors global regulatory bodies (FCA, SEC, BIS, FATF), classifies updates using LLMs, detects policy gaps, and orchestrates compliance workflows.

## Architecture

- **Language:** Python 3.12
- **Package Manager:** pip (requirements.txt)
- **Entry Point:** `main.py`
- **Type:** CLI application (no web frontend)

## Project Structure

```
agents/
  scraper_agent.py     # Monitors RSS feeds from regulatory bodies
  classifier_agent.py  # LLM-based impact classification (Groq)
  policy_matcher.py    # Cross-references updates against internal policies
  case_manager.py      # Creates and routes compliance cases
data/
  cases.json           # Output: generated compliance cases
  sample_policies/     # Input: internal policy .docx files
config.py              # Centralized configuration via environment variables
main.py                # Orchestrator entry point
```

## Running the App

```bash
python main.py
```

This runs the full pipeline:
1. Scrapes live regulatory RSS feeds
2. Classifies each update by impact level (CRITICAL/HIGH/MEDIUM/LOW)
3. Detects gaps between regulatory updates and internal policies
4. Creates compliance cases routed to the appropriate teams

## Required Environment Variables

Set these in the Secrets panel before running:

| Variable | Description |
|---|---|
| `GROQ_API_KEY` | Groq API key (free at console.groq.com) — used for LLM classification |
| `ANTHROPIC_API_KEY` | Anthropic Claude API key (optional alternative LLM) |
| `GEMINI_API_KEY` | Google Gemini API key (optional alternative LLM) |
| `UIPATH_CLIENT_ID` | UiPath Automation Cloud client ID |
| `UIPATH_CLIENT_SECRET` | UiPath Automation Cloud client secret |
| `UIPATH_TENANT_NAME` | UiPath tenant name |
| `UIPATH_ORG_ID` | UiPath organization ID |

## User Preferences

- Prefer explicit errors over silent fallbacks.
