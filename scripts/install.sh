#!/usr/bin/env bash

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CODEX_HOME_DIR="${CODEX_HOME:-$HOME/.codex}"
SKILLS_SOURCE="$REPO_ROOT/.agents/skills"
SKILLS_TARGET="$CODEX_HOME_DIR/skills"
AGENTS_SOURCE="$REPO_ROOT/agents"
AGENTS_TARGET="$CODEX_HOME_DIR/agents"
INSTALL_GLOBAL_AGENTS="false"
FORCE_GLOBAL_AGENTS="false"
CHECK_ONLY="false"

usage() {
  cat <<'EOF'
Usage: ./scripts/install.sh [--check] [--with-global-agents] [--force-global-agents]

Copies repository skills and custom subagents into ${CODEX_HOME:-~/.codex}.
Matching skill files and agent TOML files are replaced; unrelated files remain.

Options:
  --check              Report missing/different managed files without writing.
  --with-global-agents  Also install global/AGENTS.md as ~/.codex/AGENTS.md.
  --force-global-agents Allow replacing an existing ~/.codex/AGENTS.md.
  -h, --help            Show this help.
EOF
}

for argument in "$@"; do
  case "$argument" in
    --check)
      CHECK_ONLY="true"
      ;;
    --with-global-agents)
      INSTALL_GLOBAL_AGENTS="true"
      ;;
    --force-global-agents)
      INSTALL_GLOBAL_AGENTS="true"
      FORCE_GLOBAL_AGENTS="true"
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown option: $argument" >&2
      usage >&2
      exit 2
      ;;
  esac
done

if [[ ! -d "$SKILLS_SOURCE" ]]; then
  echo "Skills directory not found: $SKILLS_SOURCE" >&2
  exit 1
fi

if [[ ! -d "$AGENTS_SOURCE" ]]; then
  echo "Custom agents directory not found: $AGENTS_SOURCE" >&2
  exit 1
fi

global_agents="$REPO_ROOT/global/AGENTS.md"
target_agents="$CODEX_HOME_DIR/AGENTS.md"
if [[ "$INSTALL_GLOBAL_AGENTS" == "true" && ! -f "$global_agents" ]]; then
  echo "Global instructions not found: $global_agents" >&2
  exit 1
fi

if [[ "$CHECK_ONLY" == "true" ]]; then
  sync_status=0
  for skill_directory in "$SKILLS_SOURCE"/*; do
    [[ -d "$skill_directory" ]] || continue
    skill_name="$(basename "$skill_directory")"
    while IFS= read -r -d '' source_file; do
      relative_path="${source_file#"$skill_directory"/}"
      if ! cmp -s "$source_file" "$SKILLS_TARGET/$skill_name/$relative_path"; then
        echo "Missing or different skill: $skill_name ($relative_path)"
        sync_status=1
      fi
    done < <(find "$skill_directory" -type f -print0)
  done
  for agent_file in "$AGENTS_SOURCE"/*.toml; do
    [[ -f "$agent_file" ]] || continue
    agent_name="$(basename "$agent_file")"
    if ! cmp -s "$agent_file" "$AGENTS_TARGET/$agent_name"; then
      echo "Missing or different custom agent: $agent_name"
      sync_status=1
    fi
  done
  if [[ "$INSTALL_GLOBAL_AGENTS" == "true" ]] && ! cmp -s "$global_agents" "$target_agents"; then
    echo "Missing or different global instructions: $target_agents"
    sync_status=1
  fi
  if [[ "$sync_status" -eq 0 ]]; then
    echo "Managed Codex configuration is synchronized."
  fi
  exit "$sync_status"
fi

# Detect a global-instruction conflict before updating skills or custom agents.
if [[ "$INSTALL_GLOBAL_AGENTS" == "true" && -e "$target_agents" && "$FORCE_GLOBAL_AGENTS" != "true" ]] && ! cmp -s "$global_agents" "$target_agents"; then
  echo "Refusing to replace existing global instructions: $target_agents" >&2
  echo "Review the files or rerun with --force-global-agents if replacement is intended." >&2
  exit 1
fi

mkdir -p "$SKILLS_TARGET"

for skill_directory in "$SKILLS_SOURCE"/*; do
  [[ -d "$skill_directory" ]] || continue

  skill_name="$(basename "$skill_directory")"
  target_directory="$SKILLS_TARGET/$skill_name"
  mkdir -p "$target_directory"
  cp -R "$skill_directory"/. "$target_directory"/
  echo "Installed skill: $skill_name"
done

mkdir -p "$AGENTS_TARGET"
for agent_file in "$AGENTS_SOURCE"/*.toml; do
  [[ -f "$agent_file" ]] || continue
  agent_name="$(basename "$agent_file")"
  cp "$agent_file" "$AGENTS_TARGET/$agent_name"
  echo "Installed custom agent: $agent_name"
done

if [[ "$INSTALL_GLOBAL_AGENTS" == "true" ]]; then
  cp "$global_agents" "$target_agents"
  echo "Installed global instructions: $CODEX_HOME_DIR/AGENTS.md"
fi

echo "Codex configuration installed from: $REPO_ROOT"
