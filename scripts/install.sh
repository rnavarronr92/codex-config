#!/usr/bin/env bash

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CODEX_HOME_DIR="${CODEX_HOME:-$HOME/.codex}"
SKILLS_SOURCE="$REPO_ROOT/.agents/skills"
SKILLS_TARGET="$CODEX_HOME_DIR/skills"
INSTALL_GLOBAL_AGENTS="false"
FORCE_GLOBAL_AGENTS="false"

usage() {
  cat <<'EOF'
Usage: ./scripts/install.sh [--with-global-agents] [--force-global-agents]

Installs the skills from this repository into ~/.codex/skills.

Options:
  --with-global-agents  Also install global/AGENTS.md as ~/.codex/AGENTS.md.
  --force-global-agents Allow replacing an existing ~/.codex/AGENTS.md.
  -h, --help            Show this help.
EOF
}

for argument in "$@"; do
  case "$argument" in
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

mkdir -p "$SKILLS_TARGET"

for skill_directory in "$SKILLS_SOURCE"/*; do
  [[ -d "$skill_directory" ]] || continue

  skill_name="$(basename "$skill_directory")"
  target_directory="$SKILLS_TARGET/$skill_name"
  mkdir -p "$target_directory"
  cp -R "$skill_directory"/. "$target_directory"/
  echo "Installed skill: $skill_name"
done

if [[ "$INSTALL_GLOBAL_AGENTS" == "true" ]]; then
  global_agents="$REPO_ROOT/global/AGENTS.md"
  if [[ ! -f "$global_agents" ]]; then
    echo "Global instructions not found: $global_agents" >&2
    exit 1
  fi

  mkdir -p "$CODEX_HOME_DIR"
  target_agents="$CODEX_HOME_DIR/AGENTS.md"
  if [[ -e "$target_agents" ]] && ! cmp -s "$global_agents" "$target_agents" && [[ "$FORCE_GLOBAL_AGENTS" != "true" ]]; then
    echo "Refusing to replace existing global instructions: $target_agents" >&2
    echo "Review the files or rerun with --force-global-agents if replacement is intended." >&2
    exit 1
  fi

  cp "$global_agents" "$target_agents"
  echo "Installed global instructions: $CODEX_HOME_DIR/AGENTS.md"
fi

echo "Codex configuration installed from: $REPO_ROOT"
