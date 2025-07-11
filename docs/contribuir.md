# Cómo contribuir y replicar el entorno local

## Requisitos previos

- Node.js >= 16.x
- Git

## Pasos para clonar y preparar el entorno

1. Clona el repositorio:

   ```bash
   git clone https://github.com/iberi22/ComoCocinar.git
   cd ComoCocinar/HowToCook
   ```

2. Instala las dependencias:

   ```bash
   npm install
   ```

3. Haz tus cambios en una rama nueva:

   ```bash
   git checkout -b mi-feature
   ```

4. Añade tus archivos:

   ```bash
   git add .
   ```

5. Haz commit (el hook de pre-commit corregirá el formato):

   ```bash
   git commit -m "feat: mi cambio"
   ```

6. Sube tu rama y abre un Pull Request:

   ```bash
   git push origin mi-feature
   ```

## Reglas básicas

- Sigue la estructura y el formato de las recetas existentes.
- Incluye YAML Front Matter completo en cada receta.
- No edites directamente la rama main.
- Consulta los archivos de docs y ejemplos para referencias.

## Recursos clave

- [Guía de CI/CD](./CI_CD.md)
- [Sistema de pre-commit](./precommit.md)
- [Ejemplo de receta enriquecida](../dishes/colombian/otras_preparaciones/arequipe.md)
- [Plan de enriquecimiento y metodología](../COLOMBIAN_RECIPES_PLAN.md)
