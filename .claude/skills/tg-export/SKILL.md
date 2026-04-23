---
name: tg-export
description: Sync Telegram channels to markdown files. Use when the user wants to export or sync Telegram channel posts.
argument-hint: "[--limit N] [--takeout] [--redownload ID] [--wait-time S]"
allowed-tools: Bash
---

Sync Telegram channels to markdown files by running the export script.

```bash
cd "${CLAUDE_SKILL_DIR}" && C:\Users\Vlad\.local\bin\uv.exe run --no-project export.py $ARGUMENTS
```

Report how many posts were synced per channel and note any errors.
