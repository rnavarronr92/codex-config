# Testing and validation review reference

Load this reference when the review needs to assess checks, test coverage, browser behavior or validation evidence.

Discover available checks from `composer.json`, `package.json`, configuration files and project documentation.

When feasible, execute relevant existing checks without modifying the project:

- PHPStan or Larastan.
- PHPUnit or Pest.
- ESLint.
- Type checking.
- Existing Vue component tests.
- Existing build validation.
- Playwright when browser behavior must be verified and a safe environment is available.
- SonarQube MCP when available and relevant.

Do not install dependencies, change configuration, update snapshots, modify data or run destructive commands. Distinguish clearly between verified failure, strongly supported defect and unverified risk. Never claim tests passed unless they were actually executed.
