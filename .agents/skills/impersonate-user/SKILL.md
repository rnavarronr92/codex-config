---
name: impersonate-user
description: >-
  Navigate a local Lirmi session through Saitama to Roma, then continue to a
  user-provided local URL and review the visible module. Use for read-only
  walkthroughs of local modules, not production access or code changes.
---

# Impersonate User

Use this skill to reach a module through the local Saitama → Roma flow and inspect its visible behavior. The user chooses the destination URL after Roma loads.

## Workflow

1. Use the available browser automation, preferring Playwright MCP when configured and otherwise using the available computer-use browser. Keep navigation in the existing local browser profile when it contains the Saitama session.
2. Ask for the full Saitama URL if it was not included in the request or a trusted local config. Do not assume a domain suffix. Accept an `http` or `https` URL without embedded credentials. Treat `localhost`, `.localhost`, `.local`, and `.test` hosts (including `.lirmi.test`) as common local-development names. For a custom hostname, ask the user to confirm it is their local or test instance before opening it; do not continue to a production site. If the session is already authenticated, continue without asking for credentials. If Saitama shows its login page, ask the user for the Saitama username/email and password immediately before signing in, and state that they will be submitted only to the confirmed Saitama host. Use them only to fill that login form; never repeat them in chat, save them in files, logs, screenshots, browser notes, or this skill. If the user does not want to share the password in chat, leave the login page open and let them enter it manually before continuing.
3. Identify the account to impersonate from the user's request. If it is missing, ask for the account's email or other unique identifier. In Saitama, search for that identifier and open only the exact matching user. Stop if there is no unique match.
4. Before selecting **Usurpar**, ask the user for confirmation at that moment. If they decline or do not confirm, stop on the user profile page.
5. Select **Usurpar** and verify that Roma's home page loads under the expected account. Discover Roma from the actual redirect; do not derive its hostname from Saitama's suffix. If the redirect host is not a recognized local-development name, ask the user to confirm it is their local or test instance before continuing. Stop if the account or destination is unexpected.
6. Once Roma is visibly loaded, ask the user for the full destination URL to continue to. Do not guess a route. Require `http` or `https`, reject URLs containing embedded usernames or passwords, and accept common local-development hosts (`localhost`, `.localhost`, `.local`, `.test`). For other hostnames, ask the user to confirm that the destination is their local or test instance; do not continue to a production site.
7. Navigate to that URL and review only the requested module's visible behavior. Use accessible page state and screenshots as evidence. If the page redirects to an unrecognized host, stop and ask the user to confirm it is part of their local or test environment before further interaction.
8. Keep the review read-only: do not create, edit, delete, submit, approve, or otherwise change application data. Do not dismiss security or account-protection prompts on the user's behalf. Avoid opening student or other personal records unless the user identifies that data as necessary to the requested review.

## Review and report

- Confirm the final URL and whether the module loaded, denied access, or showed an error.
- Report reproducible UI or navigation defects with the steps and visible evidence. Separate observed behavior from inference; do not claim source-code defects without inspecting the relevant code.
- If the user also asks for a source review and the relevant repository is available, inspect only the code connected to the requested module and use the applicable code-review skill.
- State what was and was not reviewed. Do not modify application code, configuration, data, or MCP settings.

## Local flow note

Roma's visible **PIE+** entry uses `/nemo-auth`. `/auth-nemo` was not a valid Roma route in the observed local application. Treat the UI's current link as authoritative and do not assume either route without checking the page.
