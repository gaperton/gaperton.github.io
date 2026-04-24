---
name: tg-export
description: Sync Telegram channel posts and comments to markdown files. Use when the user wants to export, import, or sync a Telegram channel. Posts go to YYYY-MM-DD_postId.md, comments to postId.comments/, media to postId.files/.
argument-hint: "[--comments] [--limit N] [--redownload ID] [--wait-time S]"
allowed-tools: Bash
---

Sync a Telegram channel to markdown files by running the export script.

**Sync posts** (default):
```bash
cd "${CLAUDE_SKILL_DIR}" && uv run --no-project export.py $ARGUMENTS
```

**Sync comments** (pass `--comments`):
```bash
cd "${CLAUDE_SKILL_DIR}" && uv run --no-project export.py --comments $ARGUMENTS
```

Both commands are incremental — state is saved after every message and resumes where it left off.
Report how many posts/comments were synced and note any errors.
