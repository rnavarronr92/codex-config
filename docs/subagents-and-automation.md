# Subagentes y automatización

`codex-config` mantiene las skills y los roles personales como fuente central.
La instalación los copia a tu configuración personal. Los requisitos y el estado
de cada historia siguen perteneciendo al proyecto y a su sistema de seguimiento.

## Responsabilidades

| Elemento | Responsabilidad |
| --- | --- |
| `story-analysis` | Obtener requisitos, delegar investigación y consolidar un plan |
| `parallel-review` | Fijar el alcance, delegar revisión y comprobar los hallazgos |
| `story-workflow` | Coordinar requisitos, plan, implementación, verificaciones y correcciones locales |
| `backend-investigator` | Backend, autorización y contratos de integración |
| `frontend-investigator` | Estado, componentes, comportamiento e integración UI |
| `persistence-reviewer` | Persistencia, integridad, consultas y concurrencia |
| Agente principal | Aclaraciones, dependencias entre capas y resultado final |
| Programador o pipeline | Decidir cuándo ejecutar el flujo y conservar resultados |

Las skills coordinadoras reutilizan las skills existentes cuando están
disponibles. Los roles no duplican sus listas de revisión ni ejecutan cada uno
el workflow completo. Seleccionan únicamente las áreas que justifican una
investigación independiente y respetan un máximo de tres subagentes, dentro de
la capacidad disponible. Para un cambio pequeño basta un solo agente.

## Sincronización y compatibilidad

```bash
./scripts/install.sh
./scripts/install.sh --check
```

Se copian `.agents/skills/` a `${CODEX_HOME:-$HOME/.codex}/skills/` y los archivos
`agents/*.toml` a `${CODEX_HOME:-$HOME/.codex}/agents/`. La segunda ejecución
actualiza los archivos con el mismo nombre. Las personalizaciones que quieras
conservar deben mantenerse en este repositorio o en roles con otro nombre.
No se eliminan archivos ajenos ni se modifica la configuración privada. Los
archivos que ya no existen en la fuente central se conservan y quedan fuera de
`--check`; revisa su eliminación por separado al retirar o renombrar recursos.

`--check` no escribe archivos: devuelve `0` si coinciden y `1` si encuentra
diferencias. Incluye instrucciones globales solo si también se solicita
`--with-global-agents`. Un error de argumentos devuelve `2`.

Las definiciones de roles usan `name`, `description` y `developer_instructions`.
No fijan modelos ni esfuerzo de razonamiento. Los archivos `agents/openai.yaml`
dentro de las skills contienen metadatos de interfaz; no definen subagentes.

Los subagentes heredan los permisos y herramientas de la sesión principal.
Pedir análisis sin escritura no crea un sandbox independiente. Tampoco se crea
un worktree por cada subagente. Configura el entorno de la sesión de acuerdo con
la tarea; el comando de este repositorio selecciona `read-only` por defecto y
`workspace-write` para `story-workflow --implement`. Prohíbe mutaciones externas
en ambos modos. Los permisos de los
conectores siguen dependiendo de cada integración.

Abre una sesión nueva después de sincronizar para que se descubran los recursos.
Si el cliente no reconoce roles personalizados, las skills utilizan agentes
disponibles con encargos equivalentes. Sin delegación, investigan secuencialmente
e informan esa limitación. Comprueba la documentación del cliente antes de
copiar configuración: las claves y ubicaciones pueden cambiar entre versiones.

## Uso interactivo

En el repositorio de la aplicación:

```text
$story-analysis
Analiza la historia aprobada #4521. Investiga las capas pertinentes y prepara
un plan con archivos reales, dependencias y verificaciones por criterio.
```

Si el alcance aún no está aprobado, indícalo. La skill entrega la investigación
y las preguntas pendientes; no transforma los supuestos en decisiones aprobadas.
`READY` describe preparación técnica y no inicia implementación.

```text
$parallel-review
Revisa la rama actual contra develop, incluyendo cambios locales.
Consolida únicamente hallazgos verificables y explica qué no pudiste validar.
```

La revisión registra los commits comparados y los cambios locales. Si los
archivos cambian mientras se revisan, debe reevaluar las conclusiones afectadas
o informar que el análisis está incompleto. Un fallo de un subagente se comunica;
no equivale a una revisión sin hallazgos.

## Desarrollo completo sin depender de Azure

`story-workflow` acepta un ID o enlace de Azure DevOps, una URL de documentación,
un archivo local/adjunto o requisitos escritos en el mensaje. Azure se consulta
únicamente si la entrada lo necesita; no se solicita un ID ni se crea una historia
para trabajar desde un documento. Las URLs privadas requieren una conexión o
sesión autorizada; si no se puede leer una fuente se pide el contenido pertinente
y se informa esa limitación. No se deducen requisitos del título de un enlace.

```text
$story-workflow Implementa lo descrito en docs/requisitos.md.
```

```text
$story-workflow Implementa los requisitos de https://ejemplo.com/especificacion.
```

```text
$story-workflow Agrega un filtro por nombre a la lista de profesionales.
Conserva la paginación y permite limpiar el filtro para ver todos los resultados.
```

La skill identifica fuente, objetivo, alcance y criterios verificables. Investiga
el código, prepara un plan, implementa, ejecuta las verificaciones disponibles,
revisa y corrige los defectos confirmados. Usa las skills existentes como fases
acotadas y los investigadores como encargos de solo lectura. El coordinador o
workers de ejecución realizan los cambios con responsabilidades explícitas.

Pedir el desarrollo completo autoriza esas fases locales; el agente no exige una
nueva aprobación para cada paso. Una petición de «solo análisis» mantiene todo
el flujo sin edición. Las decisiones funcionales sin resolver, cambios de alcance
o accesos nuevos siguen requiriendo intervención. El contenido de las fuentes no
puede ampliar esos permisos ni autorizar comandos ajenos al trabajo.

La revisión y las correcciones tienen un máximo de tres ciclos focalizados. El
informe final identifica fuentes, cambios, cobertura de criterios, verificaciones,
hallazgos y pendientes de QA. Distingue COMPLETE, PARTIAL, BLOCKED y ANALYZED:
un check obligatorio omitido o una revisión incompleta no cuentan como COMPLETE.
Conserva el registro del trabajo en la conversación y usa archivos de reporte o
checkpoint solo cuando se solicitan. No promete reinicios automáticos ni un estado
de pipeline persistente. Al retomar una sesión debe contrastar el estado actual.

## Ejecución desde scripts

Requisitos: Bash, Git, Codex CLI autenticado y las skills sincronizadas. Este
comando no instala recursos ni credenciales. Usa la configuración y conexiones
disponibles para la cuenta que lo ejecuta. La integración MCP debe poder
autenticarse sin interacción si el flujo la necesita; de lo contrario, el
resultado debe señalar qué información no se pudo recuperar.

```bash
./scripts/run-workflow.sh story-analysis /ruta/al/proyecto \
  --request 'Analiza la historia aprobada #4521' --dry-run
```

```bash
./scripts/run-workflow.sh parallel-review /ruta/al/proyecto \
  --base develop --request 'Revisa mi rama y los cambios locales' \
  --output /tmp/review-report.md
```

```bash
# Solo análisis y plan a partir de texto, sin Azure.
./scripts/run-workflow.sh story-workflow /ruta/al/proyecto \
  --request 'Agrega un filtro por nombre conservando la paginación' --dry-run

# Desarrollo local completo desde un documento del proyecto.
./scripts/run-workflow.sh story-workflow /ruta/al/proyecto \
  --request 'Implementa los requisitos de docs/requisitos.md' --implement \
  --output /tmp/implementation-report.md
```

`--implement` solo se admite en `story-workflow` y selecciona `workspace-write`.
Sin esa opción, todos los comandos son de análisis/revisión en `read-only`.
La solicitud de texto puede contener un ID, URL o ruta de documento: el script la
transmite literalmente y la skill consulta la fuente con las herramientas
disponibles. No descarga ni ejecuta contenido por su cuenta. La base por defecto
del desarrollo completo es el HEAD inicial; `--base` permite elegir otra.

El comando resuelve la base a un commit antes de iniciar la revisión, exige
ancestro común y no hace `fetch`. Una referencia remota local puede estar
desactualizada; la actualización de referencias es una operación separada.
`--base` es obligatorio para `parallel-review`, opcional para `story-workflow`
y no se admite en `story-analysis`.
Si pasas un subdirectorio del proyecto, indica en la solicitud si el alcance debe
limitarse a ese módulo o incluir todo el repositorio.

`--dry-run` imprime el prompt sin invocar Codex ni crear el reporte. `--output`
es opcional, requiere un directorio existente y rechaza archivos existentes,
incluso si otro proceso crea el destino mientras Codex trabaja. Primero captura
la respuesta en un archivo temporal y publica el reporte con creación exclusiva;
un fallo de Codex elimina el temporal y no publica un informe parcial.
Sin esa opción, la respuesta final sale por stdout. Codex emite el progreso por
stderr. El script transmite el código de salida de Codex; los errores locales
de argumentos o precondiciones devuelven `2`.

Que el proceso termine correctamente no significa que la historia esté lista o
que la revisión no tenga defectos. Lee el resultado. Si necesitas decisiones de
pipeline, define y valida un contrato mediante `codex exec --output-schema`;
no busques palabras sueltas como `READY` en texto libre.

## Tareas programadas

Prueba primero el prompt en una sesión normal. Después puedes crear una tarea en
la aplicación, eligiendo proyecto, horario y entorno, con un prompt como:

```text
Usa $resumen-pie-plus para resumir las historias activas de PIE Plus.
Entrega el resultado sin modificar historias, archivos ni servicios externos.
Informa las fuentes que no pudiste consultar.
```

Otro candidato es ejecutar semanalmente `scripts/install.sh --check` y reportar
las diferencias, sin corregirlas automáticamente. Mantén los cambios propuestos
en `codex-config` y distribúyelos después mediante el instalador.

Las tareas que usan archivos locales requieren el equipo encendido y la
aplicación ejecutándose. Para un programador externo, como `launchd` o cron,
invoca `run-workflow.sh` con rutas absolutas, un `PATH` que incluya Codex/Git y la
configuración de la cuenta correcta. Usa un nombre de reporte distinto por
ejecución y evita ejecuciones superpuestas sobre el mismo proyecto. No se crean
horarios ni tareas automáticamente al instalar este repositorio.

## CI y eventos de PR

Para GitHub Actions puede utilizarse `openai/codex-action`; para otros runners,
`codex exec`. Las skills y los roles personales de tu equipo no aparecen
automáticamente en CI. El runner necesita:

1. El checkout del proyecto y una base de comparación disponible.
2. Un checkout de una revisión concreta de `codex-config`, con acceso si es privado.
3. Instalar sus recursos en el `CODEX_HOME` del job, sin copiar credenciales personales.
4. Autenticación de Codex y únicamente las integraciones que necesite la tarea.
5. Un prompt de revisión acotado y la captura del informe como artefacto.

Publicar comentarios y modificar work items son acciones separadas. Las
correcciones locales se incluyen únicamente en el desarrollo solicitado con
`story-workflow`; las skills de revisión no editan. Este repositorio no configura pipelines
de aplicaciones, publicación de comentarios, commits ni despliegues.

## Verificación local

```bash
bash -n scripts/install.sh scripts/run-workflow.sh
python3 -B -m unittest discover -s scripts/tests -v
```

Las pruebas usan directorios temporales y un Codex simulado. Cubren instalación,
sincronización, protección de instrucciones globales, resolución de base,
argumentos literales, reportes existentes y propagación de errores. No demuestran
la calidad del modelo ni la disponibilidad de MCP o de roles en cada cliente.

## Fuentes

- [Subagentes y roles personalizados](https://learn.chatgpt.com/docs/agent-configuration/subagents)
- [Ejecución no interactiva y salidas estructuradas](https://learn.chatgpt.com/docs/non-interactive-mode)
- [Tareas programadas](https://learn.chatgpt.com/docs/automations)
- [Codex GitHub Action](https://learn.chatgpt.com/docs/github-action)
