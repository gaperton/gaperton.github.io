# tg-export

Exports Telegram channel posts and comments to markdown files, incrementally.

## Output structure

```
tg-export/
  @channel/
    YYYY-MM/
      YYYY-MM-DD_postId.md           <- post
      YYYY-MM-DD_postId.files/       <- post media (photos, videos, docs)
        photo.jpg
      YYYY-MM-DD_postId.comments/    <- comments from linked discussion group
        commentId-AuthorName.md
        commentId-originalfile.ext   <- comment media
```

Comment frontmatter includes `author` (display name) and `author_handle` (@username if set).

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
  "output_dir": "../../../tg-export",
  "channels": [
    "channel_username"
  ]
}
```

`channels` accepts public usernames (`some_channel`) or numeric IDs (`-1001234567890`).

## Usage

Requires [uv](https://docs.astral.sh/uv/). No separate Python or pip install needed.

On first run Telegram will ask for your phone number and a confirmation code.
The `session` file stays authenticated for subsequent runs — keep it private.

### Sync posts

```bash
uv run export.py --limit 0
```

State is saved after every post to `tg-export/.state.json` — safe to interrupt and resume.

### Sync comments

Comments are fetched from the linked discussion group as one incremental stream
(not per-post), so each run only fetches new comments regardless of which post they're on.

```bash
uv run export.py --comments --limit 0
```

### Options

```
--limit N        Messages to fetch per run (default: 10, 0 = all)
--comments       Sync comments instead of posts
--redownload ID  Re-fetch a specific post by Telegram message ID
--wait-time S    Seconds between request batches (default: 1)
```

## Notes

- Comments require the channel to have a linked discussion group enabled.
- `config.json` and `session*` are gitignored.
