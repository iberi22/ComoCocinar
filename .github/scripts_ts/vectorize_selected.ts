import { pipeline } from '@xenova/transformers';
import fs from 'fs/promises';
import path from 'path';

// CLI args
interface Args { [k: string]: string }
function parseArgs(): Args {
  const out: Args = {};
  for (let i = 2; i < process.argv.length; i++) {
    const a = process.argv[i];
    if (a.startsWith('--')) {
      const key = a.slice(2);
      const val = process.argv[i + 1] && !process.argv[i + 1].startsWith('--') ? process.argv[++i] : 'true';
      out[key] = val;
    }
  }
  return out;
}

const args = parseArgs();
const SELECTED_LIST = args.selected || path.join(__dirname, '../../automation/queue/selected_files.txt');
const METADATA_JSON = args.metadata || path.join(__dirname, '../../recipes_metadata.json');
const OUTPUT_JSONL = args.output || path.join(__dirname, '../../recipes_vectors.jsonl');

// Fields to embed (same as existing script)
const FIELDS_TO_VECTORIZE = [
  'nombre', 'descripcion', 'ingredientes', 'preparacion', 'analisis', 'sabiduria_colectiva', 'fuentes'
];

type AnyObj = { [k: string]: any };

function normalizePath(p: string): string {
  return p.replace(/\\/g, '/').trim();
}

async function readSelectedFiles(p: string): Promise<Set<string>> {
  const txt = await fs.readFile(p, 'utf8');
  const set = new Set<string>();
  for (const line of txt.split(/\r?\n/)) {
    const v = normalizePath(line);
    if (v) set.add(v);
  }
  return set;
}

async function readExistingVectorFiles(p: string): Promise<Set<string>> {
  const set = new Set<string>();
  try {
    const fh = await fs.open(p, 'r');
    try {
      for await (const chunk of fh.readLines()) {
        const line = (chunk as unknown as string).trim();
        if (!line) continue;
        try {
          const obj = JSON.parse(line);
          if (obj && obj.file) set.add(normalizePath(String(obj.file)));
        } catch { /* ignore */ }
      }
    } finally {
      await fh.close();
    }
  } catch { /* file may not exist yet */ }
  return set;
}

async function loadMetadata(jsonPath: string): Promise<AnyObj[]> {
  const content = await fs.readFile(jsonPath, 'utf8');
  const data = JSON.parse(content);
  if (!Array.isArray(data)) throw new Error('recipes_metadata.json must be an array');
  return data as AnyObj[];
}

function getTextForVectorization(metadata: AnyObj): string {
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
  // Load selections
  const selected = await readSelectedFiles(SELECTED_LIST);
  if (selected.size === 0) {
    console.log('No selected files to vectorize.');
    return;
  }

  // Load metadata and index by normalized path
  const meta = await loadMetadata(METADATA_JSON);
  const byFile = new Map<string, AnyObj>();
  for (const m of meta) {
    const f = m && m.file ? normalizePath(String(m.file)) : '';
    if (f) byFile.set(f, m);
  }

  // Determine remaining (skip ones already vectorized)
  const already = await readExistingVectorFiles(OUTPUT_JSONL);
  const toProcess: AnyObj[] = [];
  for (const f of selected) {
    if (already.has(f)) continue;
    const m = byFile.get(f);
    if (m) toProcess.push(m);
  }

  if (toProcess.length === 0) {
    console.log('All selected files are already vectorized.');
    return;
  }

  // Initialize model
  const extractor = await pipeline('feature-extraction', 'Xenova/all-MiniLM-L6-v2');

  // Append to JSONL
  const fout = await fs.open(OUTPUT_JSONL, 'a');
  try {
    for (const recipe of toProcess) {
      const text = getTextForVectorization(recipe);
      const output = await extractor(text, { pooling: 'mean', normalize: true });
      const embedding = Array.from(output.data as Float32Array);
      const lineObj = { ...recipe, vector: embedding };
      await fout.appendFile(JSON.stringify(lineObj) + '\n');
    }
  } finally {
    await fout.close();
  }

  console.log(`Vectorized ${toProcess.length} selected items.`);
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
