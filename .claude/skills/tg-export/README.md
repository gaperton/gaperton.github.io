# tg-export

Exports Telegram channels to markdown files, incrementally.

## Output structure

```
export/
  {channel}/
    YYYY-MM/
      DD-HHMMSS.md                        <- post
      DD-HHMMSS/
        YYYY-MM-DDTHHMMSS-Author.md       <- comment
        photo.jpg                         <- attached media
```

## Setup

**1. Get Telegram API credentials**

Go to [my.telegram.org](https://my.telegram.org) → API development tools → create an app.
Copy the `api_id` and `api_hash`.

**2. Configure**

```bash
cp config.default.json config.json
```

Edit `config.json`:

```json
{
  "api_id": "12345678",
  "api_hash": "abcdef1234567890abcdef1234567890",
  "session_file": "session",
  "output_dir": "export",
  "channels": [
    "channel_username"
  ]
}
```

`channels` accepts public usernames (`some_channel`) or numeric IDs (`-1001234567890`).
Add multiple channels to sync them all in one run.

## Usage

Requires [uv](https://docs.astral.sh/uv/). No separate Python or pip install needed — uv handles everything.

Use the `/tg-export` skill in Claude Code, or run manually:

```bash
cd .claude/skills/tg-export
uv run export.py
```

On first run Telegram will ask you to log in with your phone number and a confirmation code.
A `session` file is created to stay authenticated on subsequent runs — keep it private.

Each run only fetches posts newer than the last sync. State is stored in `export/.state.json`.

### Options

```
--limit N        Max posts to fetch per channel per run (default: 10, 0 = all)
--takeout        Use a Telegram takeout session — lower flood limits, recommended for full imports
--wait-time S    Seconds between request batches (default: 0 with --takeout, 1 otherwise)
```

Incremental sync (default):
```bash
uv run export.py --limit 100
```

Full channel import (recommended):
```bash
uv run export.py --takeout --limit 0
```

## Notes

- Comments are exported only if the channel has a linked discussion group enabled.
- `config.json`, `session*`, and `export/` are gitignored.
