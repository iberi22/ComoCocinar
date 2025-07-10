import { pipeline } from '@xenova/transformers';
import fs from 'fs/promises';
import path from 'path';

// Configuración
const MODEL_NAME = 'Xenova/all-MiniLM-L6-v2'; // Modelo equivalente a 'all-MiniLM-L6-v2'
const INPUT_JSON = path.join(__dirname, '../../recipes_metadata.json');
const OUTPUT_JSONL = path.join(__dirname, '../../recipes_vectors.jsonl');

// Campos a vectorizar (ajusta según tu estructura)
const FIELDS_TO_VECTORIZE = [
  'nombre', 'descripcion', 'ingredientes', 'preparacion', 'analisis', 'sabiduria_colectiva', 'fuentes'
];

interface RecipeMetadata {
  [key: string]: any;
}

async function loadMetadata(jsonPath: string): Promise<RecipeMetadata[]> {
  const content = await fs.readFile(jsonPath, 'utf8');
  return JSON.parse(content);
}

function getTextForVectorization(metadata: RecipeMetadata): string {
  const texts: string[] = [];
  for (const field of FIELDS_TO_VECTORIZE) {
    const value = metadata[field];
    if (value) {
      if (Array.isArray(value)) {
        texts.push(value.join('\n'));
      } else {
        texts.push(String(value));
      }
    }
  }
  return texts.join('\n');
}

async function main() {
  try {
    // Verificar si el archivo de entrada existe
    await fs.access(INPUT_JSON);

    // Cargar metadatos
    const data = await loadMetadata(INPUT_JSON);

    // Inicializar el modelo de embeddings
    const extractor = await pipeline('feature-extraction', MODEL_NAME);

    // Abrir el archivo de salida
    const fout = await fs.open(OUTPUT_JSONL, 'w');

    // Procesar cada receta
    for (const recipe of data) {
      const text = getTextForVectorization(recipe);
      // Generar embeddings
      const output = await extractor(text, { pooling: 'mean', normalize: true });
      const embedding = Array.from(output.data);

      // Escribir en el archivo JSONL
      await fout.appendFile(JSON.stringify({
        ...recipe,
        vector: embedding
      }) + '\n');
    }

    await fout.close();
    console.log('Vectorización completada.');
  } catch (err) {
    console.error('Error:', err);
  }
}

main();
