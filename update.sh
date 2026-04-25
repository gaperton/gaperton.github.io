#!/usr/bin/env bash
set -e

ROOT="$(cd "$(dirname "$0")" && pwd)"
TG_EXPORT="$ROOT/.claude/skills/tg-export"
NPM="C:/Program Files/nodejs/npm.cmd"

echo ""
echo "=== 1. Syncing posts ==="
cd "$TG_EXPORT"
uv run --no-project export.py --limit 0

echo ""
echo "=== 2. Syncing comments ==="
uv run --no-project export.py --comments --limit 0

echo ""
echo "=== 3. Building site ==="
cd "$ROOT/site"
"$NPM" run build

echo ""
echo "=== 4. Committing and pushing ==="
cd "$ROOT"
git add docs/ tg-export/ site/

if git diff --cached --quiet; then
    echo "Nothing to commit."
    exit 0
fi

DATE=$(date '+%Y-%m-%d %H:%M')
git commit -m "Update $DATE"
git push

echo ""
echo "Done."
