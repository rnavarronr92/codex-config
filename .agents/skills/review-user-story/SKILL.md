---
name: review-user-story
description: Revisa historias de usuario de Azure DevOps antes del desarrollo, identificando ambigüedades, escenarios faltantes, criterios de aceptación no verificables y preguntas para el Product Owner.
---

# Objetivo

Analizar una historia de usuario de Azure DevOps antes de iniciar el desarrollo y determinar si contiene información suficiente para comenzar.

# Herramientas

- Utiliza el MCP de Azure DevOps conectado para recuperar el work item solicitado.
- Si el MCP no está disponible, solicita al usuario el contenido de la historia o indica que no se pudo verificar la información en Azure DevOps.

# Procedimiento

1. Identifica el ID del work item. Si falta, solicítalo.
2. Consulta la historia en Azure DevOps.
3. Lee el título, la descripción, los criterios de aceptación, los comentarios y las dependencias relevantes.
4. Separa los requisitos confirmados de las inferencias y sugerencias.
5. Identifica requisitos ambiguos, incompletos o contradictorios.
6. Identifica escenarios funcionales no contemplados y casos límite relevantes.
7. Propón criterios de aceptación verificables únicamente cuando ayuden a cerrar una omisión o ambigüedad.
8. Formula preguntas concretas para el Product Owner.
9. Concluye si la historia está lista para desarrollo o requiere aclaraciones.

# Restricciones

- No inventes reglas de negocio, datos, dependencias ni decisiones del Product Owner.
- No modifiques historias, comentarios, estados ni otros datos en Azure DevOps.
- No implementes código ni sugieras cambios de implementación como si fueran requisitos.
- Diferencia claramente entre requisitos confirmados, observaciones, sugerencias y preguntas abiertas.
- Indica explícitamente qué información falta para comenzar, si aplica.
- Si no puedes consultar el work item, dilo claramente y no presentes como verificados datos que no hayas podido leer.

# Formato de respuesta

## Resumen

Resume el objetivo de la historia y su estado de preparación para desarrollo.

## Ambigüedades

Enumera cada ambigüedad e indica por qué impide o puede afectar la implementación.

## Criterios de aceptación faltantes

Propón criterios concretos, observables y verificables para cubrir omisiones identificadas.

## Casos límite

Enumera escenarios funcionales no contemplados y condiciones de error relevantes.

## Preguntas para el PO

Formula preguntas cerradas o concretas que permitan resolver las dudas pendientes.

## Recomendación

Concluye con una de estas opciones:

- **Lista**: la historia tiene información suficiente para comenzar.
- **Requiere aclaraciones**: existen dudas o faltantes que deben resolverse antes del desarrollo.
