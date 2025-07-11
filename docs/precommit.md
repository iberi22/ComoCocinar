# Sistema de Pre-commit: Husky + lint-staged

Para asegurar la calidad y consistencia de los archivos Markdown antes de cada commit, el proyecto utiliza un sistema de hooks de pre-commit basado en Husky y lint-staged.

## ¿Cómo funciona?

1. **Husky** instala y gestiona los hooks de Git. Cada vez que ejecutas `git commit`, Husky intercepta la acción.
2. **lint-staged** ejecuta `markdownlint --fix` automáticamente sobre todos los archivos `.md` que están en el staging area.
3. Si hay errores de formato, se corrigen automáticamente antes de completar el commit.

## Instalación y uso

1. Instala las dependencias:

   ```bash
   npm install
   ```

2. Los hooks se configuran automáticamente al instalar las dependencias.
3. Haz tus cambios, añade archivos con `git add` y luego ejecuta `git commit` normalmente. El sistema se encargará del resto.

## Configuración relevante

- [package.json](../package.json) → Sección `lint-staged` y scripts
- [.husky/pre-commit](../.husky/pre-commit)

## Diagnóstico

- Si el commit no avanza, revisa si hay errores de lint en el Markdown.
- Puedes forzar el commit (no recomendado) con `git commit --no-verify`.
