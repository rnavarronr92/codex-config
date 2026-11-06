---
name: resumen-pie-plus
description: Resume las historias activas y tareas hijas de PIE Plus en Azure DevOps, con análisis opcional del avance frontend y backend de Nemo.
---

# Resumen de PIE Plus

Genera un informe en español, basado en datos actuales, para el proyecto Azure DevOps PIE Plus (`https://dev.azure.com/lirmi/PIE%20Plus`). Usa el conector o MCP de Azure DevOps disponible. Trabaja en modo de solo lectura: no modifiques historias, tareas, código ni archivos, y no envíes mensajes.

## Alcance y modos

- Por defecto, entrega el **resumen rápido**: historias activas, tareas hijas directas y asignaciones.
- Si el usuario pide análisis de código, frontend/backend o el **resumen completo**, agrega el análisis de implementación en Nemo.
- Atiende filtros y variantes expresamente solicitados por el usuario. No programes ejecuciones automáticamente.

## Resumen rápido

1. Consulta todas las `User Story` del proyecto cuyo estado sea `Active`. No limites por iteración o equipo salvo que el usuario lo pida. Recupera todos los resultados, respetando paginación y límites.
2. Obtén las relaciones de jerarquía y cuenta exclusivamente los elementos de tipo `Task` que sean hijos directos de esas historias, sin filtrar por estado. Deduplica por ID y comprueba el tipo y la relación padre antes de agregarlos.
3. Agrupa las historias por su responsable actual y las tareas por su propio responsable y estado actual. Incluye explícitamente los elementos sin asignar. Define el total de asignaciones como historias más tareas; cada elemento cuenta una sola vez.
4. Muestra cantidad de historias, tareas por estado, y una tabla por usuario con historias, tareas por estado y total de asignaciones. Incluye nombres de estados de Azure DevOps y enlaces útiles. Indica fecha, hora y zona horaria de consulta.
5. Si hay datos anteriores fiables disponibles y comparables, resume las variaciones y aclara que una variación en el conjunto no prueba que los elementos se hayan creado ese día. No inventes históricos; informa si no hay una referencia anterior accesible.

## Resumen completo

Además del resumen rápido, lee títulos, descripción y criterios de aceptación de cada historia activa y consulta comentarios o dependencias cuando sean relevantes para interpretar el alcance. Inspecciona el código de Nemo disponible; usa el repositorio abierto si es Nemo o, si está disponible, `~/Documents/Code/nemo`. Indica la ruta, rama, commit y si hay cambios locales relevantes para la evaluación. No hagas fetch, pull ni cambies de rama.

Para cada historia, entrega un resumen, avance cualitativo de frontend y backend, evidencias con enlaces a archivos, pruebas existentes y pendientes o dependencias relevantes. Distingue entre implementado, parcial, no evidenciado y no aplicable; no deduzcas cumplimiento por tareas cerradas ni inventes porcentajes. Diferencia pruebas existentes de pruebas ejecutadas y no afirmes que una integración externa funciona sin verificarla.

## Limitaciones

Si Azure DevOps o el repositorio no están disponibles, indícalo y presenta únicamente lo que se haya podido verificar; no uses cifras antiguas como actuales. Señala paginación incompleta, permisos insuficientes o elementos no recuperados. No ejecutes pruebas que puedan modificar datos existentes o requieran acceso a producción. Si una comprobación no se ejecuta, no la presentes como aprobada.
