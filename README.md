# Codex Config

Repositorio central para mantener y reutilizar la configuración y los flujos de trabajo personales de Codex entre distintos equipos.

Incluye:

- Skills reutilizables.
- Roles personales de subagentes y coordinación de análisis/revisiones.
- Instrucciones globales opcionales.
- Flujos de desarrollo asistido por IA.
- Contexto y reglas de trabajo.
- Documentación de integraciones MCP.
- Plantillas de configuración sin credenciales.
- Scripts para instalar la configuración en otro equipo.

## Estructura

```text
codex-config/
├── .agents/skills/              # Skills del repositorio
├── agents/                     # Roles personales de subagentes
├── global/AGENTS.md             # Instrucciones globales opcionales
├── docs/                        # Flujos e integraciones
├── examples/                    # Configuraciones de ejemplo
├── scripts/                     # Instalación y mantenimiento
└── README.md
```

## Skills incluidas

| Skill | Propósito |
|---|---|
| `review-user-story` | Revisar historias de usuario de Azure DevOps. |
| `technical-planner` | Investigar el código y preparar planes técnicos. |
| `code-review` | Revisar cambios con reglas generales y referencias específicas por tecnología. |
| `story-analysis` | Coordinar investigación por capas y consolidar requisitos y planificación técnica. |
| `parallel-review` | Delegar revisión por capas y consolidar hallazgos verificables. |
| `story-workflow` | Coordinar desarrollo local completo desde un ID, URL, documento o texto, sin exigir una historia en Azure. |
| `security-review` | Revisar límites de seguridad en un diff o módulo, separando defectos demostrados y hechos pendientes de validar. |
| `grill-me` | Someter planes y diseños a una entrevista exhaustiva antes de implementarlos. |
| `grilling` | Procedimiento compartido de entrevista por rondas utilizado por `grill-me`. |
| `performance-optimizer` | Diagnosticar y optimizar rendimiento con evidencia. |
| `data-model-review` | Revisar migraciones y derivar un modelo de datos verificable, con criterios Laravel/PostgreSQL para grandes volúmenes. |
| `api-documentation` | Generar o actualizar documentación de APIs a partir del código y los tests, incluyendo contratos Laravel/OpenAPI. |
| `impersonate-user` | Pedir las URLs de cada entorno local, llegar a Roma mediante Saitama y revisar el módulo indicado de forma observacional. |
| `resumen-pie-plus` | Resumir historias activas, tareas y asignaciones de PIE Plus, con análisis opcional del avance en Nemo. |

### Revisión modular

`code-review` selecciona referencias según el alcance de la revisión. Una revisión de un componente Vue utiliza principalmente las reglas de Vue/JavaScript; las reglas de Laravel, PostgreSQL o Redis solo se cargan cuando el cambio involucra esas capas.

### Planificación con aclaraciones

`technical-planner` investiga los requisitos y el código existente.
Cuando encuentra decisiones relevantes que no puede resolver con
esa información, formula preguntas mediante la herramienta
interactiva disponible o en el chat.

Las respuestas se incorporan al plan. Las decisiones bloqueantes
pendientes impiden clasificarlo como READY.

### Entrevista de planes e ideas

`grill-me` es la entrada de invocación explícita y carga las instrucciones de
`grilling`, incluida en este repositorio. El instalador copia ambas skills,
sus metadatos y licencias; no se necesita instalar un paquete npm ni modificar
el proyecto de aplicación.

```text
$grill-me Examina el plan que acabamos de preparar. Cuestiona los supuestos,
riesgos y decisiones pendientes antes de implementarlo.
```

La entrevista agrupa en cada ronda las preguntas que pueden resolverse sin
depender de respuestas todavía pendientes. Cada pregunta incluye una
recomendación; las respuestas del usuario determinan las rondas siguientes.
Puede pedirse una pregunta a la vez. Los hechos se investigan con las fuentes
disponibles y las decisiones se consultan al usuario. El cierre resume acuerdos
y pendientes y confirma el entendimiento compartido. No modifica archivos ni
inicia implementación; para ello hace falta una solicitud separada.

La entrada `grill-me` conserva `allow_implicit_invocation: false` en
`agents/openai.yaml`. `grilling` conserva la disponibilidad automática del
original cuando corresponde una entrevista; no se añade una fase obligatoria
a `story-workflow` ni a cada planificación.

#### Procedencia y actualizaciones

Adaptadas de [mattpocock/skills](https://github.com/mattpocock/skills), revisión
[`5863806dd4e15c63174bee4e7515a4256792ecfa`](https://github.com/mattpocock/skills/commit/5863806dd4e15c63174bee4e7515a4256792ecfa):

- [Entrada original `grill-me`](https://github.com/mattpocock/skills/blob/5863806dd4e15c63174bee4e7515a4256792ecfa/skills/productivity/grill-me/SKILL.md).
- [Procedimiento original `grilling`](https://github.com/mattpocock/skills/blob/5863806dd4e15c63174bee4e7515a4256792ecfa/skills/productivity/grilling/SKILL.md).
- [Explicación del autor](https://www.aihero.dev/skills-grill-me).

Se conserva la licencia MIT de Matt Pocock en cada skill. Las adaptaciones
locales sustituyen la llamada a una herramienta `Skill` por la lectura explícita
de la dependencia, usan la política de invocación de Codex en lugar del campo
`disable-model-invocation`, permiten investigación directa cuando no hay
delegación y explicitan los límites de solo lectura y cierre de la entrevista.
Los metadatos de interfaz de `grilling` se conservan desde esa revisión.

Las actualizaciones del upstream se revisan y versionan aquí, conservando estas
adaptaciones y actualizando la revisión documentada. No se descargan cambios
automáticamente al instalar o invocar las skills.

### Modelo de datos y documentación de APIs

`data-model-review` revisa migraciones, modelos ORM, restricciones, índices y
tests para reconstruir el esquema actual y proponer un diagrama entidad-
relación sin inventar reglas de negocio. En proyectos Laravel con PostgreSQL
considera además Eloquent, índices, locks, backfills, planes de ejecución y
riesgos de migraciones sobre grandes volúmenes.

`api-documentation` inspecciona rutas, validaciones, controladores,
serializadores y tests para generar o actualizar documentación OpenAPI y
detectar diferencias entre el contrato documentado y el comportamiento real.
En Laravel considera además Form Requests, API Resources, middleware,
autorización, semántica REST, códigos HTTP, paginación, límites de volumen y
compatibilidad de contratos.

Ambas skills trabajan por defecto en modo de análisis y documentación. No
modifican la aplicación ni bases de datos sin una solicitud explícita.

## Instalar en otro equipo

Clona el repositorio y ejecuta el instalador:

```bash
git clone https://github.com/rnavarronr92/codex-config.git
cd codex-config
./scripts/install.sh
```

El instalador copia las skills y los roles personales a:

```text
~/.codex/skills/
~/.codex/agents/
```

Respeta `CODEX_HOME` cuando está definido. Al volver a ejecutarlo actualiza los
archivos de las skills y los TOML de agentes con el mismo nombre. Conserva otros
archivos y no modifica `config.toml`, credenciales ni conexiones MCP. Los archivos
extra dentro de una skill instalada tampoco se eliminan ni se incluyen en
`--check`, que compara únicamente los archivos presentes en la fuente central.
La eliminación de recursos obsoletos se revisa por separado.

Para comprobar la sincronización sin escribir archivos:

```bash
./scripts/install.sh --check
```

Devuelve `0` cuando las copias coinciden y `1` si hay archivos diferentes o
faltantes. La comprobación de instrucciones globales se incluye únicamente al
agregar `--with-global-agents`.

Para instalar también las instrucciones globales de `global/AGENTS.md`:

```bash
./scripts/install.sh --with-global-agents
```

Las instrucciones globales pueden afectar todos los repositorios de Codex. Por eso su instalación es opt-in.

Si ya existe un `~/.codex/AGENTS.md` diferente y quieres reemplazarlo explícitamente:

```bash
./scripts/install.sh --force-global-agents
```

## Uso dentro de este repositorio

Cuando Codex trabaja dentro de este repositorio, puede descubrir las skills de `.agents/skills/`. También puede utilizar el flujo completo documentado en:

- [Flujo de desarrollo asistido por IA](docs/ai-development-workflow.md)
- [Configuración de Azure DevOps MCP](docs/integrations/azure-devops-mcp.md)
- [Subagentes y automatización](docs/subagents-and-automation.md)
- [Seguridad en el workflow](docs/security-workflow.md)

## Análisis y revisión coordinados

Después de sincronizar, abre una sesión nueva en el proyecto y usa:

```text
$story-analysis Analiza la historia aprobada #4521 y prepara un plan técnico.
```

```text
$parallel-review Revisa mi rama contra develop, incluyendo cambios locales.
```

Las skills eligen las áreas pertinentes, delegan hasta tres investigaciones
independientes y entregan un único resultado. Para cambios pequeños trabajan en
un solo hilo. Si faltan roles personalizados o soporte de delegación, informan
el modo alternativo. Trabajan en análisis/revisión y no implementan cambios.

También puedes ejecutar un flujo desde un script o programador externo:

```bash
./scripts/run-workflow.sh parallel-review /ruta/al/proyecto \
  --base develop --request 'Revisa los cambios de la rama y los cambios locales' \
  --output /tmp/review-report.md
```

El directorio del reporte debe existir y el archivo debe ser nuevo. Usa
`--dry-run` para inspeccionar el prompt sin ejecutar Codex. Consulta la
[guía](docs/subagents-and-automation.md) para requisitos, tareas programadas y CI.

## Desarrollo completo desde requisitos

`story-workflow` coordina análisis, planificación, implementación, verificaciones,
revisión y correcciones. Puede recibir requisitos sin un work item. Por ejemplo:

```text
$story-workflow Implementa la historia #4521 de PIE Plus.
```

```text
$story-workflow Implementa los requisitos de https://ejemplo.com/especificacion.
```

```text
$story-workflow Implementa lo descrito en docs/requisitos.md.
```

```text
$story-workflow Agrega un filtro por nombre a la lista de profesionales.
Conserva la paginación y permite limpiar el filtro para ver todos los resultados.
```

La fuente se consulta con las herramientas disponibles y se convierte en un
alcance y criterios verificables. El agente continúa entre etapas cuando se
solicitó el desarrollo completo y no hay decisiones funcionales bloqueantes.
Puedes pedir «solo analiza» o «solo planifica» para mantener el flujo sin edición.
Un enlace aislado en una pregunta no autoriza implementación.

Desde terminal, el nuevo flujo también comienza en análisis por defecto.
`--implement` habilita el desarrollo local con sandbox `workspace-write`:

```bash
./scripts/run-workflow.sh story-workflow /ruta/al/proyecto \
  --request 'Implementa los requisitos de docs/requisitos.md' --implement \
  --output /tmp/implementation-report.md
```

La revisión usa por defecto el HEAD inicial como base; puedes indicar `--base`.
Los roles investigadores siguen sin editar. Implementa el coordinador o un worker
de ejecución con responsabilidad acotada. El resultado incluye criterios cubiertos,
checks ejecutados, correcciones y pendientes para QA. No incluye publicación ni
despliegue automáticos. Más detalles en la [guía](docs/subagents-and-automation.md).

## Revisión de seguridad

`story-workflow` incorpora una revisión focalizada cuando cambia una frontera de
seguridad: permisos, aislamiento de datos, archivos privados, entradas no
confiables, credenciales o ejecución de CI, entre otras. Incluye un breve análisis
de amenazas en el plan y usa `security-reviewer` en la revisión cuando procede.
Un cambio cosmético no inicia una auditoría adicional.

```text
$security-review Revisa los cambios contra main, especialmente el acceso a documentos privados.
```

```bash
./scripts/run-workflow.sh security-review /ruta/al/proyecto \
  --base main --request 'Revisa autorización y aislamiento de instituciones'
```

La revisión inspecciona código sin ejecutar payloads, tests ni escáneres. Separa
hallazgos confirmados, hechos pendientes de validación y candidatos descartados;
las correcciones y pruebas pertenecen a la fase de implementación autorizada.
Esta skill propia toma como referencia principios de revisión con evidencia;
no instala ni ejecuta la auditoría completa de Cloudflare. Consulta la
[guía](docs/security-workflow.md) para alcance, límites y herramientas adicionales.

## Verificación de los scripts

```bash
bash -n scripts/install.sh scripts/run-workflow.sh
python3 -B -m unittest discover -s scripts/tests -v
```

Las pruebas requieren Python 3.11 o posterior y Git. Usan directorios temporales
y un ejecutable simulado de Codex; no llaman al modelo ni a servicios externos.

## Seguridad

No subas credenciales, tokens, contraseñas, archivos `.env` ni configuraciones locales con secretos. Usa los archivos de `examples/` como referencia y configura las credenciales de cada equipo por separado.

El repositorio contiene instrucciones y plantillas; no contiene el estado completo de las cuentas, plugins, sesiones o credenciales de Codex.
