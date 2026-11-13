# Focused Laravel and Vue security review

Apply only the sections reached by the requested change. These are investigation
prompts, not findings. Follow deployed contracts and verified repository rules;
do not invent roles or assume missing infrastructure controls.

## Identity, ownership and data isolation

- Trace route middleware, guard, policy/gate, service and query before concluding
  that authorization is absent. Authentication and validation do not by themselves
  establish ownership of an arbitrary requested resource.
- Establish which identity and institution/tenant context is trusted and where
  identifiers are mapped. Check that a caller cannot choose another user's or
  institution's context through request fields, route parameters or serialized jobs.
- Follow resource reads/writes through joins, relationships, bulk actions, cache
  keys, exports and signed/private document routes. Use the project's actual
  isolation dimensions instead of assuming a particular tenant column.
- Verify that an intended public or same-principal action is not misclassified as
  a cross-user vulnerability. Do not treat an intentional administrator capability
  as privilege escalation without an unauthorized path to that capability.

## Laravel inputs and output

- Trace validated and unvalidated fields through mass assignment and service
  calls, including fields the UI hides. Confirm which model fields can change.
- Check actual parameter binding and allowlists around raw SQL, sort identifiers,
  process execution, outbound URLs and redirect destinations. A raw query with
  bound values is not SQL injection merely because it uses raw syntax.
- Inspect serialization and log/audit payloads for reachable disclosure of private
  fields or credentials. Do not reproduce sensitive values in review output.
- Account for existing framework CSRF, session and escaping behavior. Report a
  bypass or concrete unprotected path rather than requiring duplicate mechanisms.
- When token/OAuth code changes, use `passport-development` when available to
  inspect grant/client/scope and identity-context boundaries without issuing real
  tokens or changing clients during the review.

## Files and external requests

- Trace upload validation, storage keys/paths, visibility, resource ownership and
  retrieval authorization. MIME/extension checks and signed URLs address specific
  controls; none independently proves all file-access boundaries are correct.
- Look for attacker-controlled filesystem paths, object keys, outbound request
  targets or redirects reaching sensitive resources without appropriate controls.
- Treat external network restrictions, proxy policy and provider behavior as
  facts to establish. Missing deployment evidence is a validation gap, not proof
  that an exploit succeeds. Never test these hypotheses against live services.

## Vue and browser trust

- Follow user-controlled content to HTML/URL/script sinks, including `v-html`,
  raw DOM insertion, dynamic URLs and third-party rendering. Establish reachable
  unsanitized input; static trusted markup is not automatically an XSS finding.
- Check client-only authorization against server enforcement. A hidden/disabled
  button is not a security control, but the server may already enforce the rule.
- Inspect sensitive browser storage, exposed credentials, cross-window messages
  and request construction only when the changed flow involves them. Check
  origins and data handling in the actual call path.

## Dependencies, configuration and CI

- Review changed manifests, lockfiles, CI permissions, untrusted checkout inputs
  and credential use. Inspect configured security checks when present; do not
  install scanners, fetch new rules or run package lifecycle scripts in the review.
- Existing dependency advisories or scanner alerts are leads. Verify affected
  versions, reachability and impact before calling one a confirmed code defect;
  keep unavailable registry/deployment facts explicit.
- A dependency scan, secret scan and manual boundary review provide different
  evidence. Do not infer that any one check proves the others passed.
- If citing OWASP ASVS requirement IDs, read the actual requirement and include
  its version; do not claim full ASVS coverage from this focused reference.

## References

- [Laravel authorization](https://laravel.com/docs/authorization)
- [Laravel validation](https://laravel.com/docs/validation)
- [Vue security guidance](https://vuejs.org/guide/best-practices/security.html)
- [OWASP ASVS](https://asvs.owasp.org/)

Consult the relevant version-specific framework documentation when a finding
depends on framework behavior; prefer Laravel Boost when available.
