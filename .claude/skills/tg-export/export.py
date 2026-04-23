#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["telethon"]
# ///
import argparse
import asyncio
import copy
import json
import re
from datetime import timezone
from pathlib import Path
from typing import Optional

from telethon import TelegramClient
from telethon.errors import ChannelPrivateError
from telethon.extensions import markdown as tg_markdown
from telethon.helpers import add_surrogate, del_surrogate

CONFIG_FILE = "config.json"


def load_config() -> dict:
    if not Path(CONFIG_FILE).exists():
        raise FileNotFoundError(f"{CONFIG_FILE} not found — copy config.default.json to config.json and fill in your credentials")
    with open(CONFIG_FILE, encoding="utf-8") as f:
        return json.load(f)


def load_state(path: Path) -> dict:
    if path.exists():
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_state(state: dict, path: Path) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)


def safe_name(text: str, max_len: int = 40) -> str:
    text = re.sub(r"[^\w\s-]", "", text or "")
    text = re.sub(r"\s+", "-", text.strip())
    return text[:max_len] or "unknown"


def _message_text(message) -> str:
    text = message.text
    if not text:
        return ""
    entities = message.entities or []
    if not entities:
        return text
    # Entity offsets are into the clean text (Telegram strips inline markdown before counting).
    # Strip __ ** and [text](url) notation so entity offsets align with the clean text.
    clean = text.replace('__', '').replace('**', '')
    clean = re.sub(r'\[([^\]\n]*)\]\([^)\n]*\)', r'\1', clean)
    # Trim trailing whitespace from entity boundaries: Telegram often includes \n\n,
    # which places closing markers at the start of the next paragraph.
    # Skip entities whose content is entirely whitespace (would produce empty __ or **).
    trimmed = []
    for e in entities:
        chunk = clean[e.offset:e.offset + e.length]
        stripped = chunk.rstrip()
        if not stripped:
            continue
        if len(stripped) < len(chunk):
            e = copy.copy(e)
            e.length = len(stripped)
        trimmed.append(e)
    result = del_surrogate(tg_markdown.unparse(add_surrogate(clean), trimmed))
    # Remove lines that consist only of __ or ** (empty formatting artifacts).
    result = re.sub(r'(?m)^[_*]{2,4}\s*$', '', result)
    # Collapse multiple consecutive blank lines left after removal.
    result = re.sub(r'\n{3,}', '\n\n', result)
    # Fix: whitespace immediately inside opening marker — move space before the marker.
    result = re.sub(r'\*\* (\S)', r' **\1', result)
    result = re.sub(r'__ (\S)', r' __\1', result)
    # Fix: whitespace immediately inside closing marker — move space after the marker.
    result = re.sub(r' (\*\*)(?=\W|$)', r'\1 ', result)
    result = re.sub(r' (__)(?=\W|$)', r'\1 ', result)
    # Close any unclosed __ or ** at line start whose closing was removed by cleanup above.
    lines = result.split('\n')
    fixed = []
    for line in lines:
        if line.startswith('__') and line.count('__') % 2 == 1:
            line = line + '__'
        elif line.startswith('**') and line.count('**') % 2 == 1:
            line = line + '**'
        fixed.append(line)
    return '\n'.join(fixed).strip()


def render_md(message, author: Optional[str] = None) -> str:
    lines = [
        "---",
        f"id: {message.id}",
        f"date: {message.date.isoformat()}",
    ]
    if author:
        lines.append(f"author: {author}")
    lines += ["---", ""]
    text = _message_text(message)
    if text:
        lines.append(text)
    return "\n".join(lines)


def _append_media_link(md_file: Path, subdir: str, filename: str) -> None:
    ext = Path(filename).suffix.lower()
    if ext in (".jpg", ".jpeg", ".png", ".gif", ".webp"):
        link = f"\n![{filename}](./{subdir}/{filename})\n"
    else:
        link = f"\n[{filename}](./{subdir}/{filename})\n"
    with open(md_file, "a", encoding="utf-8") as f:
        f.write(link)


async def get_sender_name(client: TelegramClient, message) -> str:
    try:
        sender = await message.get_sender()
        if sender is None:
            return "unknown"
        if hasattr(sender, "first_name"):
            name = " ".join(p for p in [sender.first_name or "", sender.last_name or ""] if p)
            return name.strip() or str(sender.id)
        if hasattr(sender, "title"):
            return sender.title
    except Exception:
        pass
    return str(message.sender_id) if message.sender_id else "unknown"


async def sync_channel(client: TelegramClient, channel: str, state: dict, out: Path, limit: int) -> None:
    ch_state = state.setdefault(channel, {"last_post_id": 0})
    last_id = ch_state["last_post_id"]
    print(f"\n[{channel}] last synced id={last_id}")

    try:
        entity = await client.get_entity(channel)
    except (ChannelPrivateError, ValueError) as e:
        print(f"  Cannot access channel: {e}")
        return

    posts = []
    async for msg in client.iter_messages(entity, reverse=True, min_id=last_id, limit=limit):
        posts.append(msg)

    if not posts:
        print("  Nothing new.")
        return

    print(f"  {len(posts)} new post(s).")

    for msg in posts:
        ts = msg.date.astimezone(timezone.utc)
        month_dir = out / channel / ts.strftime("%Y-%m")
        stem = ts.strftime("%Y-%m-%d_%H-%M-%S")

        post_file = month_dir / f"{stem}.md"
        post_dir = month_dir / stem  # comments and media go here

        month_dir.mkdir(parents=True, exist_ok=True)
        post_file.write_text(render_md(msg), encoding="utf-8")
        print(f"  + {post_file.relative_to(out)}")

        if msg.media:
            post_dir.mkdir(exist_ok=True)
            try:
                dl = await client.download_media(msg, file=str(post_dir) + "/")
                if dl:
                    _append_media_link(post_file, stem, Path(dl).name)
            except Exception as e:
                print(f"    media error: {e}")

        # Fetch comments (only works if channel has a linked discussion group)
        try:
            async for comment in client.iter_messages(entity, reply_to=msg.id):
                post_dir.mkdir(exist_ok=True)
                cts = comment.date.astimezone(timezone.utc)
                author = await get_sender_name(client, comment)
                cfile = post_dir / f"{cts.strftime('%Y-%m-%d_%H-%M-%S')}_{safe_name(author)}.md"
                cfile.write_text(render_md(comment, author), encoding="utf-8")

                if comment.media:
                    try:
                        dl = await client.download_media(comment, file=str(post_dir) + "/")
                        if dl:
                            _append_media_link(cfile, post_dir.name, Path(dl).name)
                    except Exception as e:
                        print(f"    comment media error: {e}")
        except Exception:
            pass  # channel has no comments enabled

        ch_state["last_post_id"] = max(ch_state["last_post_id"], msg.id)

    print(f"  Synced up to id={ch_state['last_post_id']}")


async def main() -> None:
    parser = argparse.ArgumentParser(description="Sync Telegram channels to markdown files.")
    parser.add_argument("--limit", type=int, default=10, metavar="N", help="Max posts to fetch per channel per run (default: 10, 0 = all)")
    args = parser.parse_args()
    args.limit = args.limit or None  # 0 → None means no limit in Telethon

    config = load_config()
    out = Path(config.get("output_dir", "export"))
    state_path = out / ".state.json"
    out.mkdir(parents=True, exist_ok=True)
    state = load_state(state_path)

    async with TelegramClient(
        config.get("session_file", "session"),
        config["api_id"],
        config["api_hash"],
    ) as client:
        for channel in config["channels"]:
            await sync_channel(client, channel, state, out, limit=args.limit)
            save_state(state, state_path)

    print("\nSync complete.")


if __name__ == "__main__":
    asyncio.run(main())
