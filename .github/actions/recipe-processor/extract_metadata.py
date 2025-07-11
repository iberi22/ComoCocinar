import os
import json
import frontmatter
from pathlib import Path

def extract_metadata_from_md(md_path):
    try:
        post = frontmatter.load(md_path)
        return post.metadata if post.metadata else None
    except Exception as e:
        print(f"Error parsing {md_path}: {e}")
        return None

def main():
    # This script runs inside the container, so we look for the code in the workspace
    recipes_dir = Path('/github/workspace/dishes/colombian')
    metadata_list = []
    for root, _, files in os.walk(recipes_dir):
        for file in files:
            if file.endswith('.md'):
                md_path = Path(root) / file
                metadata = extract_metadata_from_md(md_path)
                if metadata:
                    # Make file path relative to the repo root for consistency
                    relative_path = md_path.relative_to('/github/workspace')
                    metadata['file'] = str(relative_path)
                    metadata_list.append(metadata)
    
    # Save the JSON file in the workspace root
    output_path = Path('/github/workspace/recipes_metadata.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(metadata_list, f, ensure_ascii=False, indent=2)
    print(f"Metadata saved to {output_path}")

if __name__ == "__main__":
    main()
