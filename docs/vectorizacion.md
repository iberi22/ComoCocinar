# Vectorización de Recetas e Integración con IA

El proyecto permite preparar los datos de recetas para sistemas de búsqueda semántica y agentes de IA (RAG, ChromaDB, Qdrant, etc.).

## ¿Cómo funciona?

1. Tras cada actualización de recetas y metadatos, ejecuta el script de vectorización:

   ```bash
   python .github/scripts/vectorize_recipes.py
   ```

2. El script toma `recipes_metadata.json` y genera `recipes_vectors.jsonl`, listo para importar en ChromaDB, Qdrant u otros motores.
3. Puedes adaptar los campos a vectorizar modificando el script según tus necesidades.

## Enlaces clave

- [Script de vectorización](../.github/scripts/vectorize_recipes.py)
- [Archivo de metadatos generado](../recipes_metadata.json)
- [Ejemplo de receta enriquecida](../dishes/colombian/otras_preparaciones/arequipe.md)

## Recursos

- [ChromaDB](https://docs.trychroma.com/)
- [Qdrant](https://qdrant.tech/documentation/)

## Notas

- Asegúrate de que los metadatos estén actualizados antes de vectorizar.
- Consulta la documentación de tu motor de vectores para importar el archivo generado.
