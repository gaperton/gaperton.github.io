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
    # Entity offsets are into the clean text (Telegram strips __ before counting).
    # Strip __ and ** from raw text before applying entity-based conversion.
    clean = text.replace('__', '').replace('**', '')
    # Trim entity lengths to exclude trailing newlines: Telegram includes \n\n in
    # entity boundaries, which causes closing markers to land at the next paragraph start.
    trimmed = []
    for e in entities:
        chunk = clean[e.offset:e.offset + e.length]
        stripped_len = len(chunk.rstrip('\n'))
        if stripped_len and stripped_len < len(chunk):
            e = copy.copy(e)
            e.length = stripped_len
        trimmed.append(e)
    return del_surrogate(tg_markdown.unparse(add_surrogate(clean), trimmed))


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
        stem = ts.strftime("%d-%H%M%S")  # e.g. 15-143022

        post_file = month_dir / f"{stem}.md"
        post_dir = month_dir / stem  # comments and media go here

        month_dir.mkdir(parents=True, exist_ok=True)
        post_file.write_text(render_md(msg), encoding="utf-8")
        print(f"  + {post_file.relative_to(out)}")

        if msg.media:
            post_dir.mkdir(exist_ok=True)
            try:
                await client.download_media(msg, file=str(post_dir) + "/")
            except Exception as e:
                print(f"    media error: {e}")

        # Fetch comments (only works if channel has a linked discussion group)
        try:
            async for comment in client.iter_messages(entity, reply_to=msg.id):
                post_dir.mkdir(exist_ok=True)
                cts = comment.date.astimezone(timezone.utc)
                author = await get_sender_name(client, comment)
                cfile = post_dir / f"{cts.strftime('%Y-%m-%dT%H%M%S')}-{safe_name(author)}.md"
                cfile.write_text(render_md(comment, author), encoding="utf-8")

                if comment.media:
                    try:
                        await client.download_media(comment, file=str(post_dir) + "/")
                    except Exception as e:
                        print(f"    comment media error: {e}")
        except Exception:
            pass  # channel has no comments enabled

        ch_state["last_post_id"] = max(ch_state["last_post_id"], msg.id)

    print(f"  Synced up to id={ch_state['last_post_id']}")


async def main() -> None:
    parser = argparse.ArgumentParser(description="Sync Telegram channels to markdown files.")
    parser.add_argument("--limit", type=int, default=10, metavar="N", help="Max posts to fetch per channel per run (default: 10)")
    args = parser.parse_args()

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
