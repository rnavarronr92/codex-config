# Seguridad en el workflow de desarrollo

La revisión cotidiana debe seguir el alcance de la tarea y las fronteras de
confianza que realmente cambia. Las skills existentes ya consideran autorización,
aislamiento y datos sensibles; `security-review` aporta una investigación explícita
de esas fronteras y una separación entre defectos y hechos aún no demostrados.

## Integración

| Etapa | Comportamiento |
| --- | --- |
| Análisis y plan | Identificar actor, recurso protegido, entrada controlada, control esperado y pruebas negativas cuando el cambio toca seguridad |
| Implementación | Mantener invariantes y preparar regresiones pertinentes con datos de prueba aislados |
| Revisión | Delegar `security-review` a un `security-reviewer` cuando procede; revisar controles reales y contrastar candidatos |
| Correcciones | El coordinador corrige defectos confirmados dentro del alcance y vuelve a verificar lo afectado |
| Entrega | Informar cobertura y límites; P0/P1 confirmados sin resolver impiden declarar COMPLETE |

Se activa una investigación focalizada al cambiar autenticación/autorización,
aislamiento de datos, archivos privados, entradas o salidas no confiables,
credenciales, dependencias o ejecución de CI; también cuando el usuario la pide.
Un cambio cosmético no exige otra auditoría. El análisis usa conceptos y reglas
del proyecto, sin inventar roles, dimensiones de institución ni permisos.

La coordinación conserva un máximo de tres subagentes activos. Si hay más áreas,
programa otras asignaciones después. El investigador de seguridad devuelve sus
candidatos al coordinador para una segunda revisión cuando no puede delegar.
Un agente distinto intenta refutar los candidatos relevantes cuando está
disponible; la ausencia de validación independiente se informa. El coordinador
reúne una sola entrada por causa raíz y reutiliza una revisión ya realizada.

## Uso

No necesitas cambiar la invocación habitual:

```text
$story-workflow Implementa los requisitos de docs/requisitos.md.
```

Si la tarea modifica una frontera de seguridad, la fase pertinente se incorpora
al plan y a la revisión. Para pedir una revisión explícita:

```text
$security-review Revisa el acceso a documentos privados y el aislamiento entre instituciones.
```

```text
$parallel-review Revisa mi rama contra main, incluyendo los cambios de autorización.
```

```bash
./scripts/run-workflow.sh security-review /ruta/al/proyecto \
  --base main --request 'Revisa el diff de autorización e intercambio de archivos' \
  --output /tmp/security-review.md
```

El modo es `read-only` y no admite `--implement`. Si no se proporciona `--base`,
el lanzador fija el HEAD inicial; para comparar una rama, indica su base. Una
solicitud explícita de revisar un módulo puede inspeccionarlo sin limitarse al diff.

## Evidencia y resultado

Los informes distinguen:

- **confirmed**: la fuente y las condiciones demostradas establecen un fallo
  alcanzable. Se indica si es una conclusión de código o si existe evidencia
  de reproducción; no se inventa ejecución. Solo estos hallazgos tienen prioridad.
- **needs_validation**: hay una hipótesis concreta respaldada por la fuente,
  pero falta un hecho decisivo. Se identifica ese hecho y el próximo chequeo
  seguro, sin asignar una severidad de vulnerabilidad confirmada.
- **rejected**: un control o evidencia contradice la sospecha. Se conserva en
  el informe solo si explica una frontera relevante o evita repetir el análisis.

No se reporta como vulnerabilidad una preferencia de hardening, un `v-html` con
contenido fijo, SQL parametrizado por usar sintaxis raw o un permiso legítimo del
mismo actor. Se sigue la entrada real hasta el recurso y se comprueban middleware,
policies, consultas y controles previos antes de concluir que falta autorización.

Una revisión focalizada sin hallazgos no certifica la seguridad del sistema.
Una condición de despliegue desconocida no se asume presente ni ausente. Si falta
un hecho necesario para un invariante de la tarea, el resultado del desarrollo es
PARTIAL; las mejoras opcionales no se convierten por sí mismas en bloqueos.

## Ejecución y herramientas

Esta skill inspecciona fuentes. No ejecuta código del objetivo, tests, escáneres,
payloads o instaladores, ni sondea endpoints o servicios compartidos. Puede leer
configuración y resultados existentes, sin dar por verificados sus diagnósticos.
Nunca copia valores de credenciales a los informes.

Las pruebas de regresión que corresponden a una implementación continúan en su
fase normal, con su autorización y un entorno verificado. No se ejecutan dentro
del encargo de revisión de seguridad. Un worktree separa archivos, pero no crea
aislamiento de servicios, secretos, red o recursos de ejecución.

Los análisis deterministas de dependencias, secretos, SAST y CI complementan esta
revisión. No se instalan ni configuran herramientas nuevas automáticamente: usa
las disponibles en cada proyecto con permisos y alcance conocidos. La falta de un
escáner no equivale a cero vulnerabilidades ni obliga a instalarlo en toda tarea.

## Relación con Cloudflare

La referencia revisada es
[cloudflare/security-audit-skill](https://github.com/cloudflare/security-audit-skill).
Su workflow completo incluye fases de reconocimiento, búsqueda, validación,
verificación independiente y reportes estructurados con cobertura. Es una opción
para auditorías explícitas del repositorio o de un alcance mayor.

`security-review` es una skill propia para la revisión cotidiana y no incorpora
el paquete de Cloudflare ni afirma ejecutar su protocolo. Toma como referencia
la importancia de límites de confianza, evidencia y contraste independiente;
su resultado de código confirmado sigue siendo una conclusión estática, con
ese límite declarado. No debe confundirse con una reproducción ni con los
requisitos de confirmación de una auditoría externa.

Si posteriormente instalas la skill oficial, conserva una revisión identificable
del upstream y revisa sus instrucciones/scripts antes de sincronizarla. Su modo
de auditoría completa y sus requisitos de sandbox, red, entorno y recursos se
evalúan por separado; no se activan automáticamente desde este workflow.

## Referencias

- [Cloudflare: repositorio y requisitos](https://github.com/cloudflare/security-audit-skill)
- [Cloudflare: instrucciones de la skill](https://github.com/cloudflare/security-audit-skill/blob/main/skills/security-audit/SKILL.md)
- [OWASP ASVS](https://asvs.owasp.org/)
- [Vue: seguridad](https://vuejs.org/guide/best-practices/security.html)
