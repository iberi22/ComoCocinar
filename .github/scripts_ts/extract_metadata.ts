import fs from 'fs/promises';
import path from 'path';
import frontmatter from 'front-matter';

interface Metadata {
  [key: string]: any;
}

async function extractMetadataFromMd(mdPath: string): Promise<Metadata | null> {
  try {
    const content = await fs.readFile(mdPath, 'utf8');
    const parsed = frontmatter<Metadata>(content);
    return parsed.attributes;
  } catch (err) {
    console.error(`Error parsing ${mdPath}: ${err}`);
    return null;
  }
}

async function main() {
  const recipesDir = path.join(__dirname, '../../dishes/colombian');
  const metadataList: Metadata[] = [];
  const repoRoot = path.join(__dirname, '../../');

  async function walk(dir: string) {
    const entries = await fs.readdir(dir, { withFileTypes: true });
    for (const entry of entries) {
      const fullPath = path.join(dir, entry.name);
      if (entry.isDirectory()) {
        await walk(fullPath);
      } else if (entry.isFile() && entry.name.endsWith('.md')) {
        const metadata = await extractMetadataFromMd(fullPath);
        if (metadata) {
          const relativePath = path.relative(repoRoot, fullPath);
          const githubBaseUrl = 'https://github.com/iberi22/ComoCocinar/blob/main/';
          const githubUrl = githubBaseUrl + relativePath.replace(/\\/g, '/');
          metadataList.push({ ...metadata, file: githubUrl });
        }
      }
    }
  }

  await walk(recipesDir);

  await fs.writeFile(
    path.join(__dirname, '../../recipes_metadata.json'),
    JSON.stringify(metadataList, null, 2),
    'utf8'
  );
}

main().catch(console.error);
