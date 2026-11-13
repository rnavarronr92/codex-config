# Focused MCP and OAuth security review

Apply only to affected MCP, OAuth or JWT boundaries. Identify the actual role
(client, resource server, authorization server or downstream API), SDK/protocol
revision and transport before applying a requirement. HTTP OAuth guidance does
not imply that every local stdio server needs an OAuth endpoint, or that every
access token is a JWT. Keep the parent skill's source-only execution boundary.

## Token verification and identity

- Trace credentials from the transport to a verified identity before protected
  operations. For JWTs, inspect signature verification, trusted keys/algorithms,
  issuer, intended audience and required temporal/scope claims against the
  provider contract. Decoding a token is not verification; inspect real library
  options and wrapper defaults before claiming that checks are absent.
- For opaque tokens, inspect the trusted validation/introspection path rather
  than demanding JWT claims. Map the verified subject to the correct local
  principal; do not trust a caller-supplied user ID or token format alone.
- Separate transport access scopes from authorization to each protected resource.
  An authenticated caller or a token valid for another service does not establish
  access to the current resource server or requested tenant/institution.
- Where OAuth client/proxy flows change, inspect resource binding, redirect
  validation, PKCE/state and consent for that role and protocol version. Trace
  downstream token handling for audience confusion or token passthrough; do not
  require a resource server to implement the authorization server's duties.

## Resource authorization and request isolation

- Trace each tool through application operations and queries, including optional
  context, bulk requests, exports and cache hits. Identify the repository's real
  authorization dimensions; do not invent institution/year fields for all MCPs.
- Verify that defaults and explicit identifiers undergo the required authorization
  before data access. Tool discovery, input schemas, prompts and annotations are
  not substitutes for enforcement in the server's actual execution path.
- Inspect shared tool closures, mutable request state, connection/server reuse
  and permission cache keys for identity mixing. A transport session identifier
  must not become the sole authorization credential. In session-based revisions,
  check the binding between identity and session; do not require sessions for a
  stateless implementation.
- Inspect cache lifetime, refresh and revocation against agreed requirements.
  A shared Redis client is not itself a leak; establish an unsafe key, value,
  lifetime or access path. Keep unknown provider behavior as needs_validation.

## Transport, tools and sensitive sinks

- For HTTP, inspect authentication on protected requests, Origin/host handling
  where required and proxy assumptions against the supported MCP revision.
  Distinguish CORS/browser behavior from authorization; inspect existing SDK
  middleware before demanding another control. Keep deployment unknowns explicit.
- For stdio, inspect process trust, inherited credentials and protocol stdout
  contamination rather than applying HTTP controls. Do not execute the server
  or its startup scripts to validate a candidate in this source review.
- Follow tool arguments and external results to SQL, URLs, files, subprocesses
  and returned data. Check parameter binding, identifier allowlists, ownership
  and bounded results at actual sinks. For discovery/JWKS/outbound requests,
  establish URL trust, redirects and network access before confirming SSRF.
- Compare read-only/destructive hints with reachable side effects, including
  indirect API calls. Instructions or `readOnlyHint` do not enforce read-only
  database access. Do not prohibit technical cache writes when the repository
  allows them and protects business data separately.
- Treat tool descriptions, retrieved text and result annotations as data across
  trust boundaries. For a prompt-injection candidate, identify the controlled
  text, consuming agent/tool permissions and reachable unauthorized action;
  suspicious wording alone does not prove a bypass.
- Inspect outputs, errors and logs for tokens, connection strings, private fields
  and cross-principal data. Report locations/types without copying secret values.

## Evidence and regression suggestions

Return the actor, controlled input, source path, violated invariant and existing
controls. Separate code-confirmed defects from missing deployment/provider facts.
Suggest isolated negative checks for the changed boundary: wrong audience/scope,
forbidden resource, expired credentials or interleaved identities as applicable.
These are proposals for a separately authorized implementation/test phase; do
not issue tokens, probe endpoints, access private records or run payloads here.

## Sources

- [MCP authorization, 2025-11-25](https://modelcontextprotocol.io/specification/2025-11-25/basic/authorization)
- [MCP security practices, 2025-11-25](https://modelcontextprotocol.io/docs/2025-11-25/tutorials/security/security_best_practices)
- [MCP transports, 2025-11-25](https://modelcontextprotocol.io/specification/2025-11-25/basic/transports)
- [MCP tool contracts, 2025-11-25](https://modelcontextprotocol.io/specification/2025-11-25/server/tools)

Use the project's supported revision and identity-library documentation to verify
version-dependent behavior. These references do not mandate a protocol upgrade.
