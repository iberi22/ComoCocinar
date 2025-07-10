# Flujo CI/CD y Protección de Rama

Este proyecto utiliza un flujo CI/CD robusto basado en GitHub Actions para asegurar la calidad, trazabilidad y seguridad de todas las recetas y cambios en el repositorio.

## ¿Cómo funciona?

1. **Workflows principales:**
   - `ci.yml`: Valida el formato y la calidad de los archivos Markdown (lint).
   - `extract-metadata.yml`: Extrae automáticamente los metadatos YAML de todas las recetas y genera/actualiza `recipes_metadata.json`.
2. **Protección de rama main:**
   - No se permite el push directo a `main`.
   - Todo cambio debe pasar por Pull Request y ser validado por los checks automáticos.
   - Solo se puede fusionar un PR si todos los workflows pasan correctamente.
3. **Automerge de metadatos:**
   - Cuando hay cambios en los metadatos, el workflow crea un Pull Request automático y habilita el automerge si los checks pasan.

## Reglas de protección recomendadas

- Activar "Require status checks to pass before merging" para todos los workflows relevantes.
- Activar "Require pull request reviews before merging" si se desea revisión humana.
- Bloquear force-push y borrado de la rama main.

## Enlaces útiles

- [Workflow de CI](../.github/workflows/ci.yml)
- [Workflow de extracción de metadatos](../.github/workflows/extract-metadata.yml)
- [Script de extracción de metadatos](../.github/scripts/extract_metadata.py)

## Diagnóstico de problemas comunes

- Si un PR no se fusiona automáticamente, revisa los checks fallidos en la pestaña "Checks" del PR.
- Si el workflow de metadatos falla, consulta los logs y asegúrate de que el script y los archivos YAML sean válidos.
