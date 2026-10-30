# Azure DevOps MCP

Esta guía documenta una configuración local de referencia para que Codex pueda consultar Azure DevOps mediante MCP.

## Requisitos

- Codex Desktop o Codex CLI.
- Node.js y `npx`.
- Acceso a la organización de Azure DevOps.
- Permisos de lectura sobre los proyectos y work items necesarios.
- El paquete y la versión del servidor MCP aprobados por el equipo.

## Configuración local

La configuración de MCP debe mantenerse fuera de este repositorio cuando incluya credenciales o valores específicos del equipo. En Codex, la configuración de usuario se guarda normalmente en:

```text
~/.codex/config.toml
```

Ejemplo de referencia:

```toml
[mcp_servers.azure-devops]
command = "npx"
args = [
  "-y",
  "@azure-devops/mcp",
  "TU_ORGANIZACION"
]
```

Reemplaza `TU_ORGANIZACION` por el identificador real de la organización. Confirma el nombre del paquete, los argumentos y el método de autenticación contra la documentación oficial de la versión que utilice tu equipo antes de habilitar esta configuración.

El archivo [`examples/config.example.toml`](../../examples/config.example.toml) contiene únicamente una plantilla y no debe copiarse sin revisar.

## Contexto por repositorio

La organización, el proyecto y el área de Azure DevOps pueden documentarse en el `AGENTS.md` del repositorio de la aplicación:

```md
## Azure DevOps

- Organization: mi-organizacion
- Project: Engineering
- Team: Communications
- Area Path: Engineering\Hermes
- Relevant tags: Hermes, Comunicaciones

## Work Item Resolution

When using Azure DevOps:

1. Read the Azure DevOps configuration.
2. Use the configured MCP server.
3. Retrieve the requested work item.
4. Validate project and Area Path.
5. Read the description and acceptance criteria.
6. Do not modify work items without explicit approval.
```

Estos valores son ilustrativos. `AGENTS.md` entrega contexto al agente, pero no concede permisos adicionales al servidor MCP.

## Verificación

Después de configurar el servidor, solicita una operación de solo lectura:

```text
Consulta los proyectos disponibles en Azure DevOps.

Utiliza el MCP configurado.
No modifiques información.
```

Si Codex puede recuperar únicamente los proyectos autorizados, la conexión está operativa.

## Seguridad y límites

- No subas tokens, contraseñas ni archivos de configuración privados.
- No uses credenciales de producción para pruebas locales.
- No concedas permisos de escritura si solo necesitas consultar work items.
- La skill `review-user-story` no debe modificar historias ni comentarios.
- La autenticación y autorización dependen de Azure DevOps y de la configuración real del servidor MCP.
