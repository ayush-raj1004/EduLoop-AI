# EduLoop AI – Self-Evaluating Agentic Lesson Generator

EduLoop AI generates beginner lessons, evaluates them against a strict
10-check PASS/FAIL rubric, regenerates failed drafts with feedback, and stores
run history and recurring failure patterns in SQLite.

## Requirements

- Windows/macOS/Linux
- Python 3.11
- Groq API key

## Setup (Windows PowerShell)

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
```

Open `.env` and add your Groq API key. Never commit `.env`.

## Run from command line

```powershell
python run.py --topic "Introduction to RAG"
```

## Run the Streamlit interface

```powershell
streamlit run streamlit_app.py
```

## Run tests

```powershell
pytest -q
```

## Workflow

Input → Generator → Evaluator → PASS/FAIL decision → retry with rejection
feedback (up to two retries) → save lesson and report.

## Evaluation

See `docs/evaluation_rubric.md` for the ten binary criteria. A lesson passes
only if every criterion passes. Deterministic checks can turn an LLM PASS into
a FAIL, but cannot override an LLM FAIL.

## Persistent memory

SQLite stores completed runs, rejection logs and counts of recurring failed
rubric checks. The most common historical failures are added to future
generation guidance. Memory does not modify the fixed rubric.

## Important limitation

The LLM evaluator is a model-based judge, not a guarantee of factual truth.
The grounding criterion is a conservative content review; this starter
version does not use an external reference corpus or fact-checking service.
For a production system, add trusted source retrieval and evidence-linked
claim verification.

## Project structure

- `app/agents`: generator and evaluator
- `app/graph`: LangGraph state, nodes and workflow
- `app/memory`: SQLite persistence and failure-pattern memory
- `app/prompts`: system prompts
- `app/schemas`: structured evaluation schema
- `app/utils`: deterministic checks
- `tests`: automated tests
- `docs`: architecture and rubric
- `outputs`: generated lesson and JSON report
