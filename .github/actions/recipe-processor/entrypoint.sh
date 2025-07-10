#!/bin/sh -l

# Exit immediately if a command exits with a non-zero status.
set -e

# --- Debugging: List all files in the workspace ---
echo "--- Listing all files from the root of the workspace ---"
ls -lR
echo "--- End of file listing ---"

# Run the metadata extraction script
echo "--- Running metadata extraction ---"
python /extract_metadata.py

# Run the embedding generation script
echo "--- Running embedding generation ---"
python /generate_embeddings.py

echo "--- Pipeline finished successfully ---"

# Check for changes and set the output for the main workflow
echo "--- Checking for file changes ---"
CHANGED_FILES=$(git status --porcelain | grep -E 'recipes_metadata.json|recipes_with_embeddings.json' || true)
if [ -n "$CHANGED_FILES" ]; then
  echo "File changes detected:"
  echo "$CHANGED_FILES"
  echo "changed=true" >> $GITHUB_OUTPUT
else
  echo "No changes detected in output files."
  echo "changed=false" >> $GITHUB_OUTPUT
fi
