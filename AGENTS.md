# Instrucciones del repositorio

## Commits

Cuando se cree un commit, el mensaje debe seguir Conventional Commits:

```text
<type>(<scope>): <description>
```

Tipos permitidos: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`,
`build`, `ci`, `chore` y `revert`.

Usa un scope breve y relacionado con el cambio cuando corresponda. Para este
repositorio son comunes `skill`, `docs`, `config` y `scripts`.

Ejemplos válidos:

- `fix(skill): correct performance-optimizer front matter`
- `feat(skill): add API documentation workflow`
- `docs(readme): document skill installation`

Antes de ejecutar `git commit`, revisa que el mensaje incluya el tipo, el
scope opcional, los dos puntos y un espacio, y una descripción breve en
imperativo. No uses mensajes como `Fix ...` o `updated files` sin el prefijo
Conventional Commits.
