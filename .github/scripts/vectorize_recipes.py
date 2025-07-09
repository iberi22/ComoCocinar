import json
import os
from pathlib import Path
from sentence_transformers import SentenceTransformer
import numpy as np

# Configuración
MODEL_NAME = 'all-MiniLM-L6-v2'  # Cambia por otro modelo si lo prefieres
INPUT_JSON = 'recipes_metadata.json'
OUTPUT_JSONL = 'recipes_vectors.jsonl'

# Campos a vectorizar (puedes ajustar según tu estructura)
FIELDS_TO_VECTORIZE = [
    'nombre', 'descripcion', 'ingredientes', 'preparacion', 'analisis', 'sabiduria_colectiva', 'fuentes'
]

def load_metadata(json_path):
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_text_for_vectorization(metadata):
    texts = []
    for field in FIELDS_TO_VECTORIZE:
        value = metadata.get(field)
        if value:
            if isinstance(value, list):
                texts.extend([str(v) for v in value])
            else:
                texts.append(str(value))
    return '\n'.join(texts)

def main():
    if not os.path.exists(INPUT_JSON):
        print(f"No se encontró {INPUT_JSON}. Ejecuta primero el script de extracción de metadatos.")
        return
    data = load_metadata(INPUT_JSON)
    model = SentenceTransformer(MODEL_NAME)
    with open(OUTPUT_JSONL, 'w', encoding='utf-8') as fout:
        for recipe in data:
            text = get_text_for_vectorization(recipe)
            embedding = model.encode(text).tolist()
            out = {
                'id': recipe.get('file', ''),
                'metadata': recipe,
                'embedding': embedding
            }
            fout.write(json.dumps(out, ensure_ascii=False) + '\n')
    print(f"Vectorización completada. Archivo generado: {OUTPUT_JSONL}")

if __name__ == "__main__":
    main()
