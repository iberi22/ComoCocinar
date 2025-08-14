#!/usr/bin/env python3
"""
Batch selection tool for recipe processing workflows.

Reads a metadata file (JSON array or JSONL) such as `recipes_metadata.json` and selects a batch
of recipes based on filters: count, offset, categories, regions, difficulty, processed set, and
optional embeddings presence. Outputs can be JSONL of full entries and/or a list of file paths.

Usage examples:
  - Select 20 items starting at offset 0 and print summary only:
      python automation/queue/select_batch.py --count 20 --offset 0

  - Select 10 Peruvian Amazon region recipes with no prior processing and write outputs:
      python automation/queue/select_batch.py \
        --region "Amazonía" \
        --count 10 \
        --processed output/processed.jsonl \
        --output-jsonl output/selected.jsonl \
        --output-files output/selected_files.txt

Notes:
- The metadata entries should have at least a `file` field. Optional fields used for filtering:
  `categories` (list[str] or str), `region` (str), `difficulty` (str), and `embedding` (list[float]).
- Multiple --processed inputs are supported and can be .jsonl, .json, or .txt (newline-separated paths).
- If GITHUB_OUTPUT env var is present, this script writes a few outputs: selected_count and files_csv.
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import random
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, List, Set


def eprint(*args: Any, **kwargs: Any) -> None:
    print(*args, file=sys.stderr, **kwargs)


def load_metadata(path: Path) -> List[Dict[str, Any]]:
    if not path.exists():
        raise FileNotFoundError(f"Metadata file not found: {path}")

    entries: List[Dict[str, Any]] = []
    if path.suffix.lower() == ".jsonl":
        with path.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    obj = json.loads(line)
                except json.JSONDecodeError as ex:
                    raise ValueError(f"Invalid JSONL at {path}: {ex}")
                if isinstance(obj, dict):
                    entries.append(obj)
                else:
                    raise ValueError("Each JSONL line must be a JSON object")
    else:
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, list):
            if not all(isinstance(x, dict) for x in data):
                raise ValueError("JSON array must contain objects")
            entries = data  # type: ignore[assignment]
        elif isinstance(data, dict):
            # Try common container key
            for key in ("recipes", "items", "data"):
                if key in data and isinstance(data[key], list):
                    entries = data[key]  # type: ignore[assignment]
                    break
            if not entries:
                raise ValueError("JSON object did not contain a recognized array (recipes/items/data)")
        else:
            raise ValueError("Unsupported JSON structure; expected array or object with array field")

    # Normalize minimal expected fields
    for i, e in enumerate(entries):
        if not isinstance(e, dict):
            raise ValueError(f"Entry {i} is not an object")
        if "file" not in e:
            # Best-effort: some datasets may use different key names
            for alt in ("filepath", "path", "source_file"):
                if alt in e:
                    e["file"] = e[alt]
                    break
        if "file" not in e:
            raise ValueError(f"Entry {i} missing required 'file' field")
    return entries


def load_processed_set(paths: Iterable[Path]) -> Set[str]:
    processed: Set[str] = set()

    def norm(p: str) -> str:
        # Normalize slashes and strip whitespace for consistent matching
        return p.replace("\\", "/").strip()

    for p in paths:
        if not p.exists():
            eprint(f"[warn] Processed file not found, skipping: {p}")
            continue
        if p.suffix.lower() == ".jsonl":
            with p.open("r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        obj = json.loads(line)
                    except json.JSONDecodeError:
                        continue
                    if isinstance(obj, dict) and "file" in obj:
                        processed.add(norm(str(obj["file"])) )
        elif p.suffix.lower() == ".json":
            try:
                with p.open("r", encoding="utf-8") as f:
                    data = json.load(f)
                if isinstance(data, list):
                    for item in data:
                        if isinstance(item, dict) and "file" in item:
                            processed.add(norm(str(item["file"])) )
                        elif isinstance(item, str):
                            processed.add(norm(item))
                elif isinstance(data, dict):
                    # Try to collect from any nested arrays
                    for v in data.values():
                        if isinstance(v, list):
                            for item in v:
                                if isinstance(item, dict) and "file" in item:
                                    processed.add(norm(str(item["file"])) )
                                elif isinstance(item, str):
                                    processed.add(norm(item))
            except Exception as ex:
                eprint(f"[warn] Failed to parse processed JSON {p}: {ex}")
        else:
            # Assume text file: newline-separated paths
            try:
                with p.open("r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if line:
                            processed.add(norm(line))
            except Exception as ex:
                eprint(f"[warn] Failed to read processed text {p}: {ex}")
    return processed


def get_field(entry: Dict[str, Any], key: str, default: Any = None) -> Any:
    # Safe getter that supports a few alternate keys for convenience
    if key in entry:
        return entry[key]
    alt_keys = {
        "categories": ["category", "tags"],
        "region": ["area", "zona", "country_region"],
        "difficulty": ["level", "nivel"],
        "embedding": ["vector", "embedding_vector", "embeddings"],
    }
    for alt in alt_keys.get(key, []):
        if alt in entry:
            return entry[alt]
    return default


def match_filters(
    entry: Dict[str, Any],
    categories: List[str] | None,
    regions: List[str] | None,
    difficulties: List[str] | None,
    has_embeddings: bool | None,
) -> bool:
    # categories can be list or string in entry
    if categories:
        entry_cats = get_field(entry, "categories")
        if isinstance(entry_cats, str):
            entry_cats_set = {entry_cats.strip().lower()}
        elif isinstance(entry_cats, list):
            entry_cats_set = {str(x).strip().lower() for x in entry_cats}
        else:
            entry_cats_set = set()
        want = {c.strip().lower() for c in categories}
        if entry_cats_set.isdisjoint(want):
            return False

    if regions:
        entry_region = get_field(entry, "region")
        entry_region_norm = str(entry_region).strip().lower() if entry_region is not None else ""
        want_regions = {r.strip().lower() for r in regions}
        if not entry_region_norm or entry_region_norm not in want_regions:
            return False

    if difficulties:
        entry_diff = get_field(entry, "difficulty")
        entry_diff_norm = str(entry_diff).strip().lower() if entry_diff is not None else ""
        want_diffs = {d.strip().lower() for d in difficulties}
        if not entry_diff_norm or entry_diff_norm not in want_diffs:
            return False

    if has_embeddings is not None:
        emb = get_field(entry, "embedding")
        present = emb is not None and (isinstance(emb, list) and len(emb) > 0)
        if has_embeddings and not present:
            return False
        if (has_embeddings is False) and present:
            return False

    return True


def select_batch(
    entries: List[Dict[str, Any]],
    count: int,
    offset: int,
    categories: List[str] | None,
    regions: List[str] | None,
    difficulties: List[str] | None,
    has_embeddings: bool | None,
    processed_files: Set[str],
    unique_by: List[str],
    shuffle: bool,
    seed: int | None,
) -> List[Dict[str, Any]]:
    # Filter out processed
    def norm_path(p: str) -> str:
        return p.replace("\\", "/").strip()

    filtered: List[Dict[str, Any]] = []
    seen_uniques: Set[str] = set()

    if shuffle:
        rnd = random.Random(seed)
        entries = entries.copy()
        rnd.shuffle(entries)

    for e in entries:
        file_path = str(e.get("file", ""))
        if norm_path(file_path) in processed_files:
            continue
        if not match_filters(e, categories, regions, difficulties, has_embeddings):
            continue
        # unique_by uniqueness check
        uniq_key = "|".join(str(e.get(k, "")).strip().lower() for k in unique_by)
        if uniq_key in seen_uniques:
            continue
        seen_uniques.add(uniq_key)
        filtered.append(e)

    # Apply offset and count
    if offset > 0:
        filtered = filtered[offset:]
    if count >= 0:
        filtered = filtered[:count]
    return filtered


def write_jsonl(entries: List[Dict[str, Any]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for e in entries:
            f.write(json.dumps(e, ensure_ascii=False) + "\n")


def write_files_list(entries: List[Dict[str, Any]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        for e in entries:
            fp = str(e.get("file", "")).replace("\\", "/").strip()
            if fp:
                f.write(fp + "\n")


def write_github_output(entries: List[Dict[str, Any]]) -> None:
    gh_out = os.environ.get("GITHUB_OUTPUT")
    if not gh_out:
        return
    try:
        path = Path(gh_out)
        path.parent.mkdir(parents=True, exist_ok=True)
        files = [str(e.get("file", "")).replace("\\", "/").strip() for e in entries if e.get("file")]
        files_csv = ",".join(files)
        with path.open("a", encoding="utf-8") as f:
            f.write(f"selected_count={len(entries)}\n")
            f.write(f"files_csv={files_csv}\n")
    except Exception as ex:
        eprint(f"[warn] Failed to write GITHUB_OUTPUT: {ex}")


def parse_args(argv: List[str]) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Select a batch of recipes from metadata")
    p.add_argument("--metadata", type=Path, default=Path("recipes_metadata.json"), help="Path to metadata .json or .jsonl (default: recipes_metadata.json)")
    p.add_argument("--processed", type=Path, nargs="*", default=[], help="Paths to processed files list (.jsonl/.json/.txt). Multiple allowed.")
    p.add_argument("--count", type=int, default=20, help="Number of items to select (default: 20). Use -1 for all after offset.")
    p.add_argument("--offset", type=int, default=0, help="Offset into filtered list before selecting (default: 0)")
    p.add_argument("--category", action="append", help="Category filter; can be specified multiple times")
    p.add_argument("--region", action="append", help="Region filter; can be specified multiple times")
    p.add_argument("--difficulty", action="append", help="Difficulty filter; can be specified multiple times")
    p.add_argument("--has-embeddings", dest="has_embeddings", choices=["true", "false"], help="Filter by presence of 'embedding' field")
    p.add_argument("--unique-by", action="append", default=["file"], help="Fields to ensure uniqueness by (default: file)")
    p.add_argument("--shuffle", action="store_true", help="Shuffle before selection (default: false)")
    p.add_argument("--seed", type=int, help="Random seed when shuffling")
    p.add_argument("--output-jsonl", type=Path, help="Write selected entries as JSONL to this path")
    p.add_argument("--output-files", type=Path, help="Write selected file paths (newline-separated) to this path")
    return p.parse_args(argv)


def main(argv: List[str]) -> int:
    args = parse_args(argv)

    try:
        entries = load_metadata(args.metadata)
    except Exception as ex:
        eprint(f"[error] Failed to load metadata: {ex}")
        return 2

    processed_set = load_processed_set(args.processed)

    has_embeddings: bool | None
    if args.has_embeddings is None:
        has_embeddings = None
    else:
        has_embeddings = args.has_embeddings.lower() == "true"

    selected = select_batch(
        entries=entries,
        count=args.count,
        offset=args.offset,
        categories=args.category,
        regions=args.region,
        difficulties=args.difficulty,
        has_embeddings=has_embeddings,
        processed_files=processed_set,
        unique_by=args.unique_by,
        shuffle=args.shuffle,
        seed=args.seed,
    )

    # Outputs
    if args.output_jsonl:
        try:
            write_jsonl(selected, args.output_jsonl)
        except Exception as ex:
            eprint(f"[warn] Failed to write JSONL: {ex}")
    if args.output_files:
        try:
            write_files_list(selected, args.output_files)
        except Exception as ex:
            eprint(f"[warn] Failed to write files list: {ex}")

    # GitHub outputs (if running in Actions)
    write_github_output(selected)

    # Human-friendly summary to stderr
    eprint("=== Batch Selection Summary ===")
    eprint(f"Metadata: {args.metadata}")
    eprint(f"Processed inputs: {len(args.processed)} files -> {len(processed_set)} unique paths")
    eprint(f"Filters: count={args.count}, offset={args.offset}, categories={args.category}, regions={args.region}, difficulties={args.difficulty}, has_embeddings={has_embeddings}")
    eprint(f"Selected: {len(selected)} items")
    if selected:
        sample = [str(selected[i].get('file', '')) for i in range(min(5, len(selected)))]
        eprint("Sample:")
        for s in sample:
            eprint(f" - {s}")

    # Also print the selected file paths to STDOUT for easy piping if no outputs specified
    if not args.output_jsonl and not args.output_files:
        for e in selected:
            fp = str(e.get("file", "")).replace("\\", "/").strip()
            if fp:
                print(fp)

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
