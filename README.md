# Codex Config

Repositorio central para mantener y reutilizar la configuración y los flujos de trabajo personales de Codex entre distintos equipos.

Incluye:

- Skills reutilizables.
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
| `performance-optimizer` | Diagnosticar y optimizar rendimiento con evidencia. |
| `data-model-review` | Revisar migraciones y derivar un modelo de datos verificable, con criterios Laravel/PostgreSQL para grandes volúmenes. |
| `api-documentation` | Generar o actualizar documentación de APIs a partir del código y los tests, incluyendo contratos Laravel/OpenAPI. |
| `impersonate-user` | Pedir las URLs de cada entorno local, llegar a Roma mediante Saitama y revisar el módulo indicado de forma observacional. |

### Revisión modular

`code-review` selecciona referencias según el alcance de la revisión. Una revisión de un componente Vue utiliza principalmente las reglas de Vue/JavaScript; las reglas de Laravel, PostgreSQL o Redis solo se cargan cuando el cambio involucra esas capas.

### Planificación con aclaraciones

`technical-planner` investiga los requisitos y el código existente.
Cuando encuentra decisiones relevantes que no puede resolver con
esa información, formula preguntas mediante la herramienta
interactiva disponible o en el chat.

Las respuestas se incorporan al plan. Las decisiones bloqueantes
pendientes impiden clasificarlo como READY.

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

El instalador copia las skills a:

```text
~/.codex/skills/
```

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

## Seguridad

No subas credenciales, tokens, contraseñas, archivos `.env` ni configuraciones locales con secretos. Usa los archivos de `examples/` como referencia y configura las credenciales de cada equipo por separado.

El repositorio contiene instrucciones y plantillas; no contiene el estado completo de las cuentas, plugins, sesiones o credenciales de Codex.
