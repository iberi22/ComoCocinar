from sentence_transformers import SentenceTransformer
import json
from pathlib import Path

# This script runs inside the container, so we use absolute paths within the workspace
workspace = Path('/github/workspace')
metadata_path = workspace / 'recipes_metadata.json'
output_path = workspace / 'recipes_with_embeddings.json'

# Load metadata
print(f"Loading metadata from {metadata_path}...")
with open(metadata_path, 'r', encoding='utf-8') as f:
    metadata = json.load(f)

# Initialize model
print("Initializing SentenceTransformer model...")
model = SentenceTransformer('all-MiniLM-L6-v2')

# Generate embeddings
print("Generating embeddings for each recipe...")
for recipe in metadata:
    # Create a rich text string for embedding
    tags = recipe.get('tags', [])
    description = recipe.get('description', '')
    title = recipe.get('title', '')
    text_to_embed = f"{title}. {description}. Tags: {', '.join(tags)}"
    
    # Generate and add the embedding
    embedding = model.encode(text_to_embed, show_progress_bar=False).tolist()
    recipe['embedding'] = embedding

# Save enhanced metadata
print(f"Saving enhanced metadata with embeddings to {output_path}...")
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(metadata, f, ensure_ascii=False, indent=2)

print("Embeddings generated and saved successfully.")
