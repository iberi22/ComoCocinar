# AGENTS.md

This repository is automated by two agents:

- Gemini CLI (via GitHub Actions): edits recipes in small batches following `GEMINI.md`.
- Jules (GitHub App): picks up issues labeled `jules` and opens PRs autonomously.

## Gemini CLI
- Workflow: `.github/workflows/gemini-recipes.yml`
- Inputs: batch size, whether to run embeddings.
- Obeys: `GEMINI.md` style, licensing and sources.
- Only edit files listed by the batch selector output.

Recommended settings:
```json
{"model":"gemini-1.5-flash","temperature":0.2}
```

Project variables/secrets:
- `vars.GCP_PROJECT_ID`, `vars.GCP_LOCATION`
- `secrets.GEMINI_API_KEY` (if not using Vertex AI auth)

## Jules
- Install the Jules GitHub App and grant access to this repo.
- Create an issue using "Jules Task" template or add the `jules` label to any issue.
- Jules will plan, run, and open a PR. Keep tasks small and clear.

Include context for Jules:
- Goal, acceptance criteria, constraints (languages, licenses), file paths.
- Link to prior PRs or examples.

## Batch selection
- Script: `automation/queue/select_batch.py`
- Reads `recipes_metadata.json` and supports filters.
- Excludes already-processed files (e.g., `recipes_vectors.jsonl`).

Example:
```bash
python automation/queue/select_batch.py \
  --metadata recipes_metadata.json \
  --processed recipes_vectors.jsonl \
  --count 10 \
  --output-files output/selected_files.txt
```

## Embeddings
- Default vectorization uses local Transformers in `.github/scripts_ts/vectorize_recipes.ts`.
- You can switch to Vertex AI (text-embedding-004) later using a Python script and WIF auth.

## Conventions
- Branch protection: changes go via PR. Actions and agents create PRs.
- Keep prompts short. Limit batches to avoid rate limits.
- Favor idempotent scripts and append-only JSONL artifacts.
