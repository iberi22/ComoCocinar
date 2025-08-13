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
- `vars.GCP_PROJECT_ID`, `vars.GCP_LOCATION` (only needed when using Vertex AI auth)
- `secrets.GEMINI_API_KEY` (for Gemini API from AI Studio)

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
  --output-files automation/queue/selected_files.txt
```

## Embeddings
- Default batch vectorization script: `.github/scripts_ts/vectorize_selected.ts` (embeds only selected files).
- You can switch to Vertex AI (text-embedding-004) later using a Python script and WIF auth.

## Conventions
- Branch protection: changes go via PR. Actions and agents create PRs.
- Keep prompts short. Limit batches to avoid rate limits.
- Favor idempotent scripts and append-only JSONL artifacts.

## Auto-approve & Auto-merge
- PRs labeled `automation` are auto-approved by a bot and auto-merge is enabled (squash).
- Self-approval by the author is blocked by GitHub; the bot handles approval when the label is present.
- Auto-merge only completes when all required checks are green, respecting branch protection.
- Workflows: `/.github/workflows/auto-merge.yml` and PR-side helper if needed.
