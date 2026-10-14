#!/usr/bin/env bash
# Install the DAiL Claude skill into ~/.claude/skills/
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEST="${HOME}/.claude/skills"
mkdir -p "$DEST"
cp -r "$HERE/skills/dail-marketplace" "$DEST/"
echo "installed: $DEST/dail-marketplace/SKILL.md"
python3 "$HERE/verify_skill.py" "$DEST/dail-marketplace/SKILL.md"
