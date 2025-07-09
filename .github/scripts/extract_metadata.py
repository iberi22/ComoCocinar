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
    # Cambia este path si tus recetas están en otra carpeta
    recipes_dir = Path('dishes/colombian')
    metadata_list = []
    for root, _, files in os.walk(recipes_dir):
        for file in files:
            if file.endswith('.md'):
                md_path = Path(root) / file
                metadata = extract_metadata_from_md(md_path)
                if metadata:
                    metadata['file'] = str(md_path)
                    metadata_list.append(metadata)
    # Guarda el JSON en la raíz del repo
    with open('recipes_metadata.json', 'w', encoding='utf-8') as f:
        json.dump(metadata_list, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
