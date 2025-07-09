# ComoCocinar/HowToCook

<!-- Cambio de prueba para disparar workflow CI/CD: 2025-07-09 -->
A modern, open-source recipe repository inspired by HowToCook.
This project aims to create a comprehensive, structured, and accessible collection of global recipes—enriched with metadata, automation, and AI-ready features.
Includes CI/CD workflows, community-driven contributions, and support for advanced search and AI applications.

Recetario automatizado y enriquecido, con flujos CI/CD, integración para IA y comunidad bilingüe.

Inspirado en [HowToCook](https://github.com/Anduin2017/HowToCook).

## 📑 Estado del Proyecto

- Todas las recetas principales estandarizadas y enriquecidas (YAML, sensorial, nutricional, imágenes, fuentes, licencia)
- En proceso de revisión y enriquecimiento de recetas secundarias y nuevas adiciones
- Sincronización de índices, enlaces y documentación
- Preparación para integración con agentes de IA, búsqueda semántica y vectorización

## 🚀 Integración final y automatización

Este repositorio integra:

- Recetas colombianas estandarizadas con YAML Front Matter, imágenes libres, fuentes y licencia open source.
- Automatización CI/CD: generación automática de metadatos (`recipes_metadata.json`) tras cada push a main.
- Scripts y workflows para vectorización de recetas, listos para IA/RAG (ChromaDB, Qdrant, etc).
- Documentos de comunidad en español e inglés.
- Rama `main` protegida con checks automáticos.

## 📦 Flujos CI/CD (Automatización)

### Workflows principales

- **Lint y Build:** Valida y compila la documentación y recetas (`ci.yml`, `build.yml`).
- **Extracción de metadatos:** Genera automáticamente `recipes_metadata.json` con los metadatos de todas las recetas (`metadata.yml`).
- **Vectorización IA:** Script para generar vectores de recetas (`.github/scripts/vectorize_recipes.py`).

### 🚦 Flujo automatizado de metadatos y protección de rama

1. **Extracción y generación automática de metadatos:**
   - Cada vez que se realiza un push a `main` o se abre un Pull Request, el workflow `metadata.yml` ejecuta el script de extracción de metadatos.
   - Si hay cambios en `recipes_metadata.json`, se crea automáticamente un Pull Request con la actualización.

2. **Pull Request automático y automerge:**
   - El Pull Request generado por el workflow se etiqueta y habilita para "automerge".
   - El PR solo se fusiona cuando todos los checks de CI/CD (lint, build, etc.) pasan correctamente.
   - Este proceso es compatible con las reglas de protección de rama más estrictas y no requiere intervención manual.

3. **Validación obligatoria:**
   - Todos los cambios (manuales o automáticos) deben pasar los workflows de CI/CD antes de ser fusionados a `main`.
   - No se permite push directo a `main` si hay reglas de protección activas.
   - La integración continua asegura calidad y consistencia en toda la base de recetas.

### Ejemplo de flujo completo

- Un colaborador o workflow genera cambios en recetas.
- Se actualiza `recipes_metadata.json` automáticamente.
- Se abre un Pull Request automático con los cambios de metadatos.
- Los workflows de CI/CD validan el PR.
- Si todo es correcto, el PR se fusiona automáticamente a `main`.

### Requisitos para contribuir

- Todas las recetas deben tener YAML Front Matter completo y cumplir la metodología.
- Corrección de lints obligatoria (Markdown).
- Los workflows deben pasar antes de aceptar un Pull Request.
- Consulta la sección "Automatización" para entender cómo se integran los cambios de metadatos y cómo se revisan de forma automática.

## 🤖 Vectorización para IA y RAG

1. Ejecuta el script `.github/scripts/vectorize_recipes.py` tras actualizar los metadatos.
2. El archivo `recipes_vectors.jsonl` estará listo para importar en ChromaDB, Qdrant o motores RAG.
3. Puedes adaptar los campos a vectorizar según necesidades de tu app o agente.

## 🤝 ¿Cómo contribuir?

- Crea una rama desde main.
- Usa la plantilla de receta y sigue la metodología documentada.
- Agrega fuentes, imágenes libres y licencia.
- Haz Pull Request y espera que los checks CI/CD pasen.
- Puedes contribuir en español o inglés. Consulta `CONTRIBUTING.md` y `CONTRIBUTING.es.md`.

## 🛡️ Protección de rama main

- Solo se puede mergear a main si todos los checks CI/CD pasan.
- No se permite force-push ni borrado accidental de main.
- Los administradores pueden ajustar las reglas en Settings > Branches.

## 📑 Documentos clave

- [`CODE_OF_CONDUCT.md`](./CODE_OF_CONDUCT.md) | [`CODE_OF_CONDUCT.es.md`](./CODE_OF_CONDUCT.es.md)
- [`CONTRIBUTING.md`](./CONTRIBUTING.md) | [`CONTRIBUTING.es.md`](./CONTRIBUTING.es.md)
- [`METODOLOGIA.md`](./METODOLOGIA.md)

## 📚 Licencia

MIT. Todo el contenido es open source y reutilizable.

## 🌐 Créditos y agradecimientos

Inspirado por HowToCook y la comunidad de cocina y tecnología.

## 📂 Estructura del repositorio y formato estándar

Cada receta debe comenzar con un bloque YAML Front Matter que contenga los metadatos clave. Esto permite búsquedas, filtrados y procesamiento automático por agentes inteligentes y facilita la interoperabilidad.

### Ejemplo de bloque YAML

```yaml
---
title: "Chuzo Colombiano"
region: "Nacional"
categories: ["Snack", "Comida callejera", "Plato fuerte"]
sensory:
  flavor: ["Umami", "Ahumado"]
  texture: ["Jugoso", "Dorado por fuera"]
  aroma: ["Ahumado", "Especiado"]
  presentation: "Se sirve en brocheta, acompañado de papa y arepa. Ideal para compartir en fiestas y eventos nocturnos."
main_ingredients:
  - Carne de res
  - Pollo
  - Papa salada
  - Arepa
difficulty: "★★☆☆☆"
prep_time: "40 minutos"
servings: 6
images:
  - url: "https://pixabay.com/es/photos/chorizo-parrilla-barbacoa-2314640/"
    description: "Chuzo colombiano en parrilla (Pixabay)"
sources:
  - "https://www.recetasdecolombia.com/chuzo"
  - "https://www.youtube.com/results?search_query=chuzo+colombiano"
license: "MIT"
---
```

## 📋 Campos estándar de metadatos YAML para recetas

Cada receta debe incluir un bloque YAML Front Matter al inicio, con los siguientes campos:

- `title`: Nombre completo del plato.
- `region`: Región o categoría principal (ejemplo: Andina, Caribe, Nacional).
- `categories`: Lista de categorías de uso (ejemplo: Snack, Plato fuerte, Comida callejera).
- `sensory`: Objeto con subcampos para `flavor` (sabores dominantes), `texture` (texturas principales), `aroma` (aromas destacados) y `presentation` (descripción de presentación y experiencia).
- `main_ingredients`: Ingredientes principales o diferenciadores.
- `difficulty`: Dificultad estimada (puede ser en estrellas o texto).
- `prep_time`: Tiempo estimado de preparación total.
- `servings`: Porciones aproximadas.
- `images`: Lista de objetos con `url` y `description` de imágenes libres de uso.
- `sources`: Lista de enlaces a fuentes, recetas, videos, artículos o entrevistas.
- `license`: Licencia de uso del contenido (ejemplo: MIT, CC BY 4.0).

Consulta ejemplos y plantillas en los archivos de cada región y en `COLOMBIAN_RECIPES_PLAN.md`.

- `region`: Región o categoría principal (ejemplo: Andina, Caribe, Nacional).
- `categories`: Lista de categorías de uso (ejemplo: Snack, Plato fuerte, Comida callejera).
- `sensory`: Objeto con subcampos para `flavor` (sabores dominantes), `texture` (texturas principales), `aroma` (aromas destacados) y `presentation` (descripción de presentación y experiencia).
- `main_ingredients`: Ingredientes principales o diferenciadores.
- `difficulty`: Dificultad estimada (puede ser en estrellas o texto).
- `prep_time`: Tiempo estimado de preparación total.
- `servings`: Porciones aproximadas.
- `images`: Lista de objetos con `url` y `description` de imágenes libres de uso.
- `sources`: Lista de enlaces a fuentes, recetas, videos, artículos o entrevistas.
- `license`: Licencia de uso del contenido (ejemplo: MIT, CC BY 4.0).

Consulta ejemplos y plantillas en los archivos de cada región y en `COLOMBIAN_RECIPES_PLAN.md`.

## 🤝 Cómo Contribuir

1. Crea tus recetas siguiendo la plantilla YAML Front Matter y el estándar de enriquecimiento sensorial/nutricional.
2. Haz un Pull Request. Solo se aceptarán cambios que cumplan con la estructura y pasen la validación automática.
3. Consulta el archivo `.github/PULL_REQUEST_TEMPLATE.md` y la documentación para detalles.

1. Crea tus recetas siguiendo la plantilla YAML Front Matter y el estándar de enriquecimiento sensorial/nutricional.
2. Haz un Pull Request. Solo se aceptarán cambios que cumplan con la estructura y pasen la validación automática.
3. Consulta el archivo `.github/PULL_REQUEST_TEMPLATE.md` y la documentación para detalles.

## 🛡️ Licencia

Este proyecto es open source bajo la licencia MIT. Consulta el archivo `LICENSE` para más detalles.

Este proyecto es open source bajo la licencia MIT. Consulta el archivo `LICENSE` para más detalles.

---

## 📚 Enlaces y recursos

- [COLOMBIAN_RECIPES_PLAN.md](dishes/colombian/COLOMBIAN_RECIPES_PLAN.md): Plan y metodología detallada
- [PLAN_SABORES_LATINOS.md](PLAN_SABORES_LATINOS.md): Plan para otras cocinas latinoamericanas
- [plan_enriquecimiento_recetas.md](plan_enriquecimiento_recetas.md): Metodología de enriquecimiento sensorial y nutricional
- Carpetas por región y categoría en `dishes/colombian/`

- [COLOMBIAN_RECIPES_PLAN.md](dishes/colombian/COLOMBIAN_RECIPES_PLAN.md): Plan y metodología detallada
- [PLAN_SABORES_LATINOS.md](PLAN_SABORES_LATINOS.md): Plan para otras cocinas latinoamericanas
- [plan_enriquecimiento_recetas.md](plan_enriquecimiento_recetas.md): Metodología de enriquecimiento sensorial y nutricional
- Carpetas por región y categoría en `dishes/colombian/`

## 📝 Metodología y lecciones aprendidas

La estandarización y enriquecimiento de recetas se basa en:

- Investigación en fuentes académicas, colectivas y restaurantes reconocidos
- Análisis sensorial y nutricional por ingrediente
- Inclusión de imágenes libres y enlaces verificados
- Documentación abierta y colaborativa

Para detalles, consulta los archivos de metodología y el plan general.

Inspirado en [HowToCook](https://github.com/Anduin2017/HowToCook) y adaptado para IA, conocimiento abierto y la cocina colombiana.

- [Buñuelos](dishes/colombian/snacks/buñuelo/buñuelo.md)
- [Almojábanas](dishes/colombian/snacks/almojábana/almojábana.md)
- [Arepa de Huevo](dishes/colombian/caribe/arepa_de_huevo/arepa_de_huevo.md)
- [Pandebono](dishes/colombian/panes/pandebono/pandebono.md)

### Salsas y Acompañamientos

- [Hogao](dishes/colombian/condimentos/hogao/hogao.md)
- [Ají Picante](dishes/colombian/condimentos/aji_picante/aji_picante.md)
- [Guacamole Colombiano](dishes/colombian/condimentos/guacamole_colombiano/guacamole_colombiano.md)
- [Suero Costeño](dishes/colombian/condimentos/suero_costeño/suero_costeño.md)

# 🌍 Recetas del Mundo (Pendientes de Adaptación)

### Platos de Carne

- [Cerdo salteado con cebolla (pendiente de traducir)](dishes/meat_dish/洋葱炒猪肉.md)
- [Pollo asado a la italiana (pendiente de traducir)](dishes/meat_dish/意式烤鸡.md)
- [Berenjena en salsa de pescado (pendiente de traducir)](dishes/meat_dish/鱼香茄子/鱼香茄子.md)
- [Cerdo en salsa de pescado (pendiente de traducir)](dishes/meat_dish/鱼香肉丝.md)
- [Estofado de cordero con tofu seco (pendiente de traducir)](dishes/meat_dish/枝竹羊腩煲/枝竹羊腩煲.md)
- [Gelatina de piel de cerdo (pendiente de traducir)](dishes/meat_dish/猪皮冻/猪皮冻.md)
- [Cerdo estofado con chucrut (pendiente de traducir)](dishes/meat_dish/猪肉烩酸菜.md)
- [Cerdo cocido dos veces (pendiente de traducir)](dishes/meat_dish/回锅肉.md)

### Pescados y Mariscos

- [Perca al vapor con aceite de cebollín (pendiente de traducir)](dishes/aquatic/葱油桂鱼/葱油桂鱼.md)
- [Langostinos rojos argentinos a la plancha (pendiente de traducir)](dishes/aquatic/干煎阿根廷红虾/干煎阿根廷红虾.md)
- [Carpa estofada en salsa roja (pendiente de traducir)](dishes/aquatic/红烧鲤鱼.md)
- [Pescado estofado en salsa roja (pendiente de traducir)](dishes/aquatic/红烧鱼.md)
- [Cabeza de pescado estofada en salsa roja (pendiente de traducir)](dishes/aquatic/红烧鱼头.md)
- [Langostinos salteados con mantequilla (pendiente de traducir)](dishes/aquatic/黄油煎虾/黄油煎虾.md)
- [Pescado a la parrilla mixto (pendiente de traducir)](dishes/aquatic/混合烤鱼/烤鱼.md)
- [Langostinos con mantequilla y mostaza (pendiente de traducir)](dishes/aquatic/芥末黄油罗氏虾/芥末黄油罗氏虾.md)
- [清蒸鲈鱼](dishes/aquatic/清蒸鲈鱼/清蒸鲈鱼.md)

- [清蒸生蚝](dishes/aquatic/清蒸生蚝.md)

- [水煮鱼](dishes/aquatic/水煮鱼.md)

- [蒜蓉虾](dishes/aquatic/蒜蓉虾/蒜蓉虾.md)

- [蒜香黄油虾](dishes/aquatic/蒜香黄油虾/蒜香黄油虾.md)

- [糖醋鲤鱼](dishes/aquatic/糖醋鲤鱼/糖醋鲤鱼.md)

- [微波葱姜黑鳕鱼](dishes/aquatic/微波葱姜黑鳕鱼.md)

- [香煎翘嘴鱼](dishes/aquatic/香煎翘嘴鱼/香煎翘嘴鱼.md)

- [小龙虾](dishes/aquatic/小龙虾/小龙虾.md)

- [油焖大虾](dishes/aquatic/油焖大虾/油焖大虾.md)

#

## 早餐

- [茶叶蛋](dishes/breakfast/茶叶蛋.md)

- [蛋煎糍粑](dishes/breakfast/蛋煎糍粑.md)

- [桂圆红枣粥](dishes/breakfast/桂圆红枣粥.md)

- [鸡蛋三明治](dishes/breakfast/鸡蛋三明治.md)

- [煎饺](dishes/breakfast/煎饺.md)

- [金枪鱼酱三明治](dishes/breakfast/金枪鱼酱三明治.md)

- [空气炸锅面包片](dishes/breakfast/空气炸锅面包片.md)

- [美式炒蛋](dishes/breakfast/美式炒蛋.md)

- [牛奶燕麦](dishes/breakfast/牛奶燕麦.md)

- [手抓饼](dishes/breakfast/手抓饼.md)

- [水煮玉米](dishes/breakfast/水煮玉米.md)

- [苏格兰蛋](dishes/breakfast/苏格兰蛋/苏格兰蛋.md)

- [太阳蛋](dishes/breakfast/太阳蛋.md)

- [溏心蛋](dishes/breakfast/溏心蛋.md)

- [吐司果酱](dishes/breakfast/吐司果酱.md)

- [完美水煮蛋](dishes/breakfast/完美水煮蛋.md)

- [微波炉蛋糕](dishes/breakfast/微波炉蛋糕.md)

- [微波炉荷包蛋](dishes/breakfast/微波炉荷包蛋.md)

- [温泉蛋](dishes/breakfast/温泉蛋/温泉蛋.md)

- [燕麦鸡蛋饼](dishes/breakfast/燕麦鸡蛋饼.md)

- [蒸花卷](dishes/breakfast/蒸花卷.md)

- [蒸水蛋](dishes/breakfast/蒸水蛋.md)

#

## 主食

- [炒方便面](dishes/staple/炒方便面.md)

- [炒河粉](dishes/staple/炒河粉.md)

- [炒凉粉](dishes/staple/炒凉粉/炒凉粉.md)

- [炒馍](dishes/staple/炒馍.md)

- [炒年糕](dishes/staple/炒年糕.md)

- [炒意大利面](dishes/staple/炒意大利面/炒意大利面.md)

- [葱油拌面](dishes/staple/葱油拌面.md)

- [蛋包饭](dishes/staple/蛋包饭.md)

- [蛋炒饭](dishes/staple/蛋炒饭.md)

- [电饭煲三文鱼炊饭](dishes/staple/电饭煲三文鱼炊饭/电饭煲三文鱼炊饭.md)

- [豆角焖面](dishes/staple/豆角焖面/豆角焖面.md)

- [韩式拌饭](dishes/staple/韩式拌饭/韩式拌饭.md)

- [河南蒸面条](dishes/staple/河南蒸面条/河南蒸面条.md)

- [火腿饭团](dishes/staple/火腿饭团/火腿饭团.md)

- [基础牛奶面包](dishes/staple/基础牛奶面包/基础牛奶面包.md)

- [茄子肉煎饼](dishes/staple/茄子肉煎饼/茄子肉煎饼.md)

- [鲣鱼海苔玉米饭](dishes/staple/鲣鱼海苔玉米饭/鲣鱼海苔玉米饭.md)

- [酱拌荞麦面](dishes/staple/酱拌荞麦面/酱拌荞麦面.md)

- [韭菜盒子](dishes/staple/韭菜盒子.md)

- [空气炸锅照烧鸡饭](dishes/staple/空气炸锅照烧鸡饭/空气炸锅照烧鸡饭.md)

- [醪糟小汤圆](dishes/staple/醪糟小汤圆.md)

- [老干妈拌面](dishes/staple/老干妈拌面.md)

- [老友猪肉粉](dishes/staple/老友猪肉粉/老友猪肉粉.md)

- [烙饼](dishes/staple/烙饼/烙饼.md)

- [凉粉](dishes/staple/凉粉/凉粉.md)

- [螺蛳粉](dishes/staple/螺蛳粉.md)

- [麻辣减脂荞麦面](dishes/staple/麻辣减脂荞麦面.md)

- [麻油拌面](dishes/staple/麻油拌面.md)

- [电饭煲蒸米饭](dishes/staple/米饭/电饭煲蒸米饭.md)

- [煮锅蒸米饭](dishes/staple/米饭/煮锅蒸米饭.md)

- [披萨饼皮](dishes/staple/披萨饼皮/披萨饼皮.md)

- [热干面](dishes/staple/热干面.md)

- [日式肥牛丼饭](dishes/staple/日式肥牛丼饭/日式肥牛丼饭.md)

- [日式咖喱饭](dishes/staple/日式咖喱饭/日式咖喱饭.md)

- [肉蛋盖饭](dishes/staple/肉蛋盖饭.md)

- [芝麻烧饼](dishes/staple/烧饼/芝麻烧饼.md)

- [手工水饺](dishes/staple/手工水饺.md)

- [酸辣蕨根粉](dishes/staple/酸辣蕨根粉.md)

- [汤面](dishes/staple/汤面.md)

- [微波炉腊肠煲仔饭](dishes/staple/微波炉腊肠煲仔饭/微波炉腊肠煲仔饭.md)

- [西红柿鸡蛋挂面](dishes/staple/西红柿鸡蛋挂面/西红柿鸡蛋挂面.md)

- [扬州炒饭](dishes/staple/扬州炒饭/扬州炒饭.md)

- [意式肉酱面](dishes/staple/意式肉酱面/意式肉酱面.md)

- [炸酱面](dishes/staple/炸酱面.md)

- [蒸卤面](dishes/staple/蒸卤面.md)

- [中式馅饼](dishes/staple/中式馅饼/中式馅饼.md)

- [煮泡面加蛋](dishes/staple/煮泡面加蛋.md)

#

## 半成品加工

- [半成品意面](dishes/semi-finished/半成品意面.md)

- [空气炸锅鸡翅中](dishes/semi-finished/空气炸锅鸡翅中/空气炸锅鸡翅中.md)

- [空气炸锅羊排](dishes/semi-finished/空气炸锅羊排/空气炸锅羊排.md)

- [懒人蛋挞](dishes/semi-finished/懒人蛋挞/懒人蛋挞.md)

- [凉皮](dishes/semi-finished/凉皮.md)

- [牛油火锅底料](dishes/semi-finished/牛油火锅底料.md)

- [速冻馄饨](dishes/semi-finished/速冻馄饨.md)

- [速冻水饺](dishes/semi-finished/速冻水饺.md)

- [速冻汤圆](dishes/semi-finished/速冻汤圆/速冻汤圆.md)

- [炸薯条](dishes/semi-finished/炸薯条/炸薯条.md)

#

## 汤与粥

- [昂刺鱼豆腐汤](dishes/soup/昂刺鱼豆腐汤/昂刺鱼豆腐汤.md)

- [陈皮排骨汤](dishes/soup/陈皮排骨汤/陈皮排骨汤.md)

- [陈皮排骨汤](dishes/soup/陈皮排骨汤.md)

- [番茄牛肉蛋花汤](dishes/soup/番茄牛肉蛋花汤.md)

- [勾芡香菇汤](dishes/soup/勾芡香菇汤/勾芡香菇汤.md)

- [金针菇汤](dishes/soup/金针菇汤.md)

- [菌菇炖乳鸽](dishes/soup/菌菇炖乳鸽/菌菇炖乳鸽.md)

- [腊八粥](dishes/soup/腊八粥.md)

- [罗宋汤](dishes/soup/罗宋汤.md)

- [米粥](dishes/soup/米粥.md)

- [奶油蘑菇汤](dishes/soup/奶油蘑菇汤.md)

- [排骨苦瓜汤](dishes/soup/排骨苦瓜汤/排骨苦瓜汤.md)

- [皮蛋瘦肉粥](dishes/soup/皮蛋瘦肉粥.md)

- [生汆丸子汤](dishes/soup/生汆丸子汤.md)

- [西红柿鸡蛋汤](dishes/soup/西红柿鸡蛋汤.md)

- [小米粥](dishes/soup/小米粥.md)

- [羊肉汤](dishes/soup/羊肉汤/羊肉汤.md)

- [银耳莲子粥](dishes/soup/银耳莲子粥/银耳莲子粥.md)

- [玉米排骨汤](dishes/soup/玉米排骨汤/玉米排骨汤.md)

- [朱雀汤](dishes/soup/朱雀汤/朱雀汤.md)

- [紫菜蛋花汤](dishes/soup/紫菜蛋花汤.md)

#

## 饮料

- [耙耙柑茶](dishes/drink/耙耙柑茶/耙耙柑茶.md)

- [百香果橙子特调](dishes/drink/百香果橙子特调/百香果橙子特调.md)

- [冰粉](dishes/drink/冰粉/冰粉.md)

- [菠萝咖啡特调](dishes/drink/菠萝咖啡特调/菠萝咖啡特调.md)

- [冬瓜茶](dishes/drink/冬瓜茶.md)

- [海边落日](dishes/drink/海边落日/海边落日.md)

- [金菲士](dishes/drink/金菲士/金菲士.md)

- [金汤力](dishes/drink/金汤力/金汤力.md)

- [酒酿醪糟](dishes/drink/酒酿醪糟/酒酿醪糟.md)

- [可乐桶](dishes/drink/可乐桶.md)

- [奶茶](dishes/drink/奶茶.md)

- [柠檬水](dishes/drink/柠檬水/柠檬水.md)

- [奇异果菠菜特调](dishes/drink/奇异果菠菜特调/奇异果菠菜特调.md)

- [砂糖椰子冰沙](dishes/drink/砂糖椰子冰沙/砂糖椰子冰沙.md)

- [酸梅汤](dishes/drink/酸梅汤/酸梅汤.md)

- [酸梅汤（半成品加工）](dishes/drink/酸梅汤（半成品加工）.md)

- [泰国手标红茶](dishes/drink/泰国手标红茶/泰国手标红茶.md)

- [杨枝甘露](dishes/drink/杨枝甘露.md)

- [长岛冰茶](dishes/drink/长岛冰茶.md)

- [B52轰炸机](dishes/drink/B52轰炸机.md)

- [Mojito莫吉托](dishes/drink/Mojito莫吉托.md)

#

## 酱料和其它材料

- [草莓酱](dishes/condiment/草莓酱/草莓酱.md)

- [葱油](dishes/condiment/葱油.md)

- [简易版炒糖色](dishes/condiment/简易版炒糖色.md)

- [蒜香酱油](dishes/condiment/蒜香酱油.md)

- [糖醋汁](dishes/condiment/糖醋汁.md)

- [油泼辣子](dishes/condiment/油泼辣子/油泼辣子.md)

- [油酥](dishes/condiment/油酥.md)

- [炸串酱料](dishes/condiment/炸串酱料.md)

- [蔗糖糖浆](dishes/condiment/蔗糖糖浆/蔗糖糖浆.md)

#

## 甜品

- [奥利奥冰淇淋](dishes/dessert/奥利奥冰淇淋/奥利奥冰淇淋.md)

- [草莓冰淇淋](dishes/dessert/草莓冰淇淋/草莓冰淇淋.md)

- [反沙芋头](dishes/dessert/反沙芋头/反沙芋头.md)

- [龟苓膏](dishes/dessert/龟苓膏/龟苓膏.md)

- [红柚蛋糕](dishes/dessert/红柚蛋糕/红柚蛋糕.md)

- [咖啡椰奶冻](dishes/dessert/咖啡椰奶冻/咖啡椰奶冻.md)

- [烤蛋挞](dishes/dessert/烤蛋挞/烤蛋挞.md)

- [玛格丽特饼干](dishes/dessert/玛格丽特饼干/玛格丽特饼干.md)

- [魔芋蛋糕](dishes/dessert/魔芋蛋糕/魔芋蛋糕.md)

- [戚风蛋糕](dishes/dessert/戚风蛋糕/戚风蛋糕.md)

- [酸奶意式奶冻](dishes/dessert/酸奶意式奶冻/酸奶意式奶冻.md)

- [提拉米苏](dishes/dessert/提拉米苏/提拉米苏.md)

- [无厨师机蜂蜜面包](dishes/dessert/无厨师机蜂蜜面包/无厨师机蜂蜜面包.md)

- [雪花酥](dishes/dessert/雪花酥/雪花酥.md)

- [英式司康](dishes/dessert/英式司康/英式司康.md)

- [芋泥雪媚娘](dishes/dessert/芋泥雪媚娘/芋泥雪媚娘.md)

- [炸鲜奶](dishes/dessert/炸鲜奶/炸鲜奶.md)

## 进阶知识学习

如果你已经做了许多上面的菜，对于厨艺已经入门，并且想学习更加高深的烹饪技巧，请继续阅读下面的内容：

### Técnicas de ingredientes

- [辅料技巧](tips/advanced/辅料技巧.md)

### Términos profesionales avanzados

- [高级专业术语](tips/advanced/高级专业术语.md)

### Caramelización del azúcar

- [糖色的炒制](tips/advanced/糖色的炒制.md)

### Técnicas para medir la temperatura del aceite

- [油温判断技巧](tips/advanced/油温判断技巧.md)

## Proyectos derivados

- [HowToCook-mcp 让 AI 助手变身私人大厨，为你的一日三餐出谋划策](https://github.com/worryzyy/HowToCook-mcp)

- [HowToCook-py-mcp 让 AI 助手变身私人大厨，为你的一日三餐出谋划策 (Python)](https://github.com/DusKing1/howtocook-py-mcp)
