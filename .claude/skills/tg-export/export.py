#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10,<3.14"
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
from telethon.errors import ChannelPrivateError, FloodWaitError
from telethon.extensions import markdown as tg_markdown
from telethon.helpers import add_surrogate
from telethon.tl.functions.channels import GetFullChannelRequest

CONFIG_FILE = "config.json"


def load_config() -> dict:
    if not Path(CONFIG_FILE).exists():
        raise FileNotFoundError(f"{CONFIG_FILE} not found — copy config.default.json to config.json and fill in your credentials")
    with open(CONFIG_FILE, encoding="utf-8") as f:
        return json.load(f)


def load_state(path: Path) -> dict:
    if path.exists():
        with open(path, encoding="utf-8-sig") as f:
            return json.load(f)
    return {}


def recover_state(out: Path) -> dict:
    """Scan post files (not comment subdirs) to reconstruct last synced IDs."""
    state = {}
    # Structure: out/channel/YYYY-MM/post.md  — only scan at this exact depth.
    # Comment files live in out/channel/YYYY-MM/post-dir/comment.md and use
    # discussion-group IDs (different namespace), so they must be excluded.
    for channel_dir in out.iterdir():
        if not channel_dir.is_dir() or channel_dir.name.startswith(".") or channel_dir.name.endswith(".old"):
            continue
        for month_dir in channel_dir.iterdir():
            if not month_dir.is_dir():
                continue
            for md in month_dir.glob("*.md"):
                try:
                    for line in md.read_text(encoding="utf-8").splitlines():
                        if line.startswith("id: "):
                            msg_id = int(line[4:])
                            ch = state.setdefault(channel_dir.name, {"last_post_id": 0})
                            ch["last_post_id"] = max(ch["last_post_id"], msg_id)
                            break
                except Exception:
                    pass
    return state


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
    try:
        result = tg_markdown.unparse(add_surrogate(clean), trimmed)
    except (UnicodeDecodeError, UnicodeEncodeError):
        result = clean  # exotic character caused illegal surrogate; keep plain text
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


def render_md(message, author: Optional[str] = None, author_handle: str = "") -> str:
    lines = [
        "---",
        f"id: {message.id}",
        f"date: {message.date.isoformat()}",
    ]
    if author:
        lines.append(f"author: {author}")
    if author_handle:
        lines.append(f"author_handle: {author_handle}")
    reply_to = getattr(message, 'reply_to', None)
    reply_id = getattr(reply_to, 'reply_to_msg_id', None)
    if reply_id:
        lines.append(f"reply_to: {reply_id}")
        quote_text = getattr(reply_to, 'quote_text', None)
        if quote_text:
            # Single-quote the value (YAML-safe); escape any existing single quotes
            safe = quote_text.replace(chr(10), ' ').strip().replace("'", "''")
            lines.append(f"reply_quote: '{safe}'")
    lines += ["---", ""]
    text = _message_text(message)
    if text:
        lines.append(text)
    return "\n".join(lines)


async def author_info(message) -> tuple[str, str]:
    """Return (display_name, @handle) for the message sender."""
    try:
        sender = await message.get_sender()
        if sender is None:
            return "unknown", ""
        if hasattr(sender, "first_name"):
            parts = [sender.first_name or "", sender.last_name or ""]
            name = " ".join(p for p in parts if p).strip() or "unknown"
            handle = f"@{sender.username}" if getattr(sender, "username", None) else ""
            return safe_name(name), handle
        if hasattr(sender, "title"):
            handle = f"@{sender.username}" if getattr(sender, "username", None) else ""
            return safe_name(sender.title) or "unknown", handle
    except Exception:
        pass
    return "unknown", ""


def _has_media(directory: Path, exclude: Path = None) -> bool:
    """Return True if directory contains any non-.md files (i.e. media already downloaded)."""
    if not directory.exists():
        return False
    return any(f for f in directory.iterdir() if f.suffix != '.md' and f != exclude)




async def sync_channel(client, channel: str, state: dict, out: Path,
                       limit: int, wait_time: float, fetch_client=None,
                       state_path: Path = None, sync_replies_only: bool = False) -> None:
    # fetch_client is the takeout client when in takeout mode; falls back to client.
    fetch = fetch_client or client

    ch_state = state.setdefault(channel, {"last_post_id": 0})
    last_id = ch_state["last_post_id"]
    print(f"\n[{channel}] last synced id={last_id}")

    try:
        entity = await client.get_entity(channel)
    except (ChannelPrivateError, ValueError) as e:
        print(f"  Cannot access channel: {e}")
        return

    posts = []
    async for msg in fetch.iter_messages(entity, reverse=True, min_id=last_id, limit=limit, wait_time=wait_time):
        posts.append(msg)

    if not posts:
        print("  Nothing new.")
        return

    print(f"  {len(posts)} new post(s).")

    for msg in posts:
        ts = msg.date.astimezone(timezone.utc)
        month_dir = out / channel / ts.strftime("%Y-%m")
        stem = f"{ts.strftime('%Y-%m-%d')}_{msg.id}"

        post_file = month_dir / f"{stem}.md"
        post_dir = month_dir / f"{stem}.files"

        month_dir.mkdir(parents=True, exist_ok=True)

        reply_id = getattr(getattr(msg, 'reply_to', None), 'reply_to_msg_id', None)
        if sync_replies_only:
            # Only update .md if reply_to/reply_quote is missing but should be present
            if reply_id and post_file.exists():
                existing = post_file.read_text(encoding="utf-8", errors="replace")
                has_reply_to = "reply_to:" in existing
                has_quote = "reply_quote:" in existing
                quote_text = getattr(getattr(msg, 'reply_to', None), 'quote_text', None)
                needs_update = not has_reply_to or (quote_text and not has_quote)
                if needs_update:
                    post_file.write_text(render_md(msg), encoding="utf-8", errors="replace")
                    print(f"  ~ {post_file.relative_to(out)}")
        else:
            post_file.write_text(render_md(msg), encoding="utf-8", errors="replace")
            print(f"  + {post_file.relative_to(out)}")

            if msg.media and not _has_media(post_dir):
                post_dir.mkdir(exist_ok=True)
                try:
                    await fetch.download_media(msg, file=str(post_dir) + "/")
                except Exception as e:
                    print(f"    media error: {e}")


        ch_state["last_post_id"] = max(ch_state["last_post_id"], msg.id)
        if state_path:
            save_state(state, state_path)

    print(f"  Synced up to id={ch_state['last_post_id']}")


async def sync_comments(client, channel: str, state: dict, out: Path,
                        wait_time: float, limit: int = None, state_path: Path = None,
                        skip_media: bool = False) -> None:
    ch_state = state.setdefault(channel, {"last_post_id": 0})
    last_comment_id = ch_state.get("last_comment_id", 0)

    try:
        entity = await client.get_entity(channel)
    except (ChannelPrivateError, ValueError) as e:
        print(f"  Cannot access channel: {e}")
        return

    # Get linked discussion group
    try:
        full = await client(GetFullChannelRequest(entity))
        linked_chat_id = full.full_chat.linked_chat_id
        if not linked_chat_id:
            print(f"  No linked discussion group for {channel}")
            return
        discussion = await client.get_entity(linked_chat_id)
    except Exception as e:
        print(f"  Failed to get discussion group: {e}")
        return

    channel_dir = out / channel
    stub_cache: dict[int, int] = {}   # discussion_msg_id -> channel_post_id
    post_dir_cache: dict[int, tuple] = {}  # channel_post_id -> (month_dir, stem)

    def find_post_dir(channel_post_id: int) -> tuple:
        if channel_post_id in post_dir_cache:
            return post_dir_cache[channel_post_id]
        if not channel_dir.exists():
            return None, None
        for month_dir in sorted(channel_dir.iterdir()):
            if not month_dir.is_dir():
                continue
            matches = list(month_dir.glob(f"*_{channel_post_id}.md"))
            if matches:
                stem = matches[0].stem
                post_dir_cache[channel_post_id] = (month_dir, stem)
                return month_dir, stem
        return None, None

    async def get_channel_post_id(msg) -> int | None:
        # Stub forwarded from channel
        if msg.fwd_from and getattr(msg.fwd_from, 'channel_post', None):
            return msg.fwd_from.channel_post
        # Comment: find its top-level stub
        if msg.reply_to:
            top_id = getattr(msg.reply_to, 'reply_to_top_id', None) or msg.reply_to.reply_to_msg_id
            if top_id in stub_cache:
                return stub_cache[top_id]
            try:
                stub = await client.get_messages(discussion, ids=top_id)
                if stub and stub.fwd_from and getattr(stub.fwd_from, 'channel_post', None):
                    post_id = stub.fwd_from.channel_post
                    stub_cache[top_id] = post_id
                    return post_id
            except Exception:
                pass
        return None

    print(f"\n[{channel}] comments: last_comment_id={last_comment_id}")
    synced = 0

    async for msg in client.iter_messages(discussion, reverse=True, min_id=last_comment_id, wait_time=wait_time, limit=limit):
        channel_post_id = await get_channel_post_id(msg)

        # Record stubs in cache but don't write them as comment files
        if msg.fwd_from and getattr(msg.fwd_from, 'channel_post', None):
            stub_cache[msg.id] = msg.fwd_from.channel_post
        elif channel_post_id and (msg.message or msg.media):
            month_dir, post_stem = find_post_dir(channel_post_id)
            if month_dir:
                comments_dir = month_dir / f"{post_stem}.comments"
                comments_dir.mkdir(exist_ok=True)

                name, handle = await author_info(msg)
                cfile = comments_dir / f"{msg.id}-{name}.md"

                reply_id = getattr(getattr(msg, 'reply_to', None), 'reply_to_msg_id', None)
                needs_write = not cfile.exists()
                if not needs_write and reply_id:
                    # Backfill reply_to / reply_quote into existing files that don't have it yet
                    existing = cfile.read_text(encoding="utf-8", errors="replace")
                    if "reply_to:" not in existing:
                        needs_write = True
                    elif "reply_quote:" not in existing and getattr(getattr(msg, 'reply_to', None), 'quote_text', None):
                        needs_write = True
                if needs_write:
                    cfile.write_text(render_md(msg, author=name, author_handle=handle),
                                     encoding="utf-8", errors="replace")
                    synced += 1

                if msg.media and not skip_media:
                    already_have = any(
                        f.name.startswith(f"{msg.id}-") and f.suffix != '.md'
                        for f in comments_dir.iterdir()
                    )
                    if not already_have:
                        try:
                            dl = await client.download_media(msg, file=str(comments_dir) + "/")
                            if dl:
                                orig = Path(dl).name
                                new_path = comments_dir / f"{msg.id}-{orig}"
                                if not new_path.exists():
                                    Path(dl).rename(new_path)
                        except Exception as e:
                            print(f"    comment media error: {e}")

        ch_state["last_comment_id"] = max(last_comment_id, msg.id)
        last_comment_id = ch_state["last_comment_id"]
        if state_path:
            save_state(state, state_path)

    print(f"  {synced} new comment(s). last_comment_id={ch_state.get('last_comment_id', 0)}")


async def main() -> None:
    parser = argparse.ArgumentParser(description="Sync Telegram channels to markdown files.")
    parser.add_argument("--limit", type=int, default=10, metavar="N",
                        help="Max posts to fetch per channel per run (default: 10, 0 = all)")
    parser.add_argument("--wait-time", type=float, default=None, metavar="S",
                        help="Seconds between request batches (default: 0 with --takeout, 1 otherwise)")
    parser.add_argument("--takeout", action="store_true",
                        help="Use a takeout session for lower flood limits — recommended for full imports")
    parser.add_argument("--redownload", type=int, metavar="ID",
                        help="Re-fetch a specific post by Telegram message ID and overwrite its files")
    parser.add_argument("--comments", action="store_true",
                        help="Sync comments from linked discussion group instead of posts")
    parser.add_argument("--sync-replies", action="store_true",
                        help="Re-scan all comments from the beginning to backfill reply_to fields in existing files")
    parser.add_argument("--sync-post-replies", action="store_true",
                        help="Re-scan all posts from the beginning to backfill reply_to fields (only updates .md, no media)")
    args = parser.parse_args()
    args.limit = args.limit or None  # 0 → None means no limit in Telethon
    if args.wait_time is None:
        args.wait_time = 0.0 if args.takeout else 1.0

    config = load_config()
    out = Path(config.get("output_dir", "export"))
    state_path = out / ".state.json"
    out.mkdir(parents=True, exist_ok=True)
    state = load_state(state_path)
    if not state:
        state = recover_state(out)
        if state:
            print(f"Recovered state from existing files: { {ch: s['last_post_id'] for ch, s in state.items()} }")

    async with TelegramClient(
        config.get("session_file", "session"),
        config["api_id"],
        config["api_hash"],
        flood_sleep_threshold=300,  # auto-sleep on flood waits up to 5 min
    ) as client:
        if args.sync_post_replies:
            for channel in config["channels"]:
                saved_id = state.get(channel, {}).get("last_post_id", 0)
                state.setdefault(channel, {})["last_post_id"] = 0
                try:
                    await sync_channel(client, channel, state, out,
                                       limit=None, wait_time=args.wait_time,
                                       state_path=None, sync_replies_only=True)
                finally:
                    state[channel]["last_post_id"] = saved_id
            return

        if args.sync_replies:
            # Re-scan all comments from the beginning to backfill reply_to fields
            for channel in config["channels"]:
                # Temporarily zero out last_comment_id so we scan from the start
                saved_id = state.get(channel, {}).get("last_comment_id", 0)
                state.setdefault(channel, {})["last_comment_id"] = 0
                try:
                    await sync_comments(client, channel, state, out,
                                        wait_time=args.wait_time, limit=None,
                                        state_path=None, skip_media=True)
                finally:
                    state[channel]["last_comment_id"] = saved_id  # restore
            return

        if args.comments:
            for channel in config["channels"]:
                while True:
                    try:
                        await sync_comments(client, channel, state, out,
                                            wait_time=args.wait_time, limit=args.limit,
                                            state_path=state_path)
                        break
                    except FloodWaitError as e:
                        print(f"  FloodWait: sleeping {e.seconds + 5}s...")
                        await asyncio.sleep(e.seconds + 5)
            print("\nComments sync complete.")
            return

        if args.redownload:
            for channel in config["channels"]:
                entity = await client.get_entity(channel)
                msg = await client.get_messages(entity, ids=args.redownload)
                if not msg:
                    print(f"Message {args.redownload} not found in {channel}")
                    continue
                ts = msg.date.astimezone(timezone.utc)
                month_dir = out / channel / ts.strftime("%Y-%m")
                stem = f"{ts.strftime('%Y-%m-%d')}_{msg.id}"
                post_file = month_dir / f"{stem}.md"
                post_dir = month_dir / f"{stem}.files"
                month_dir.mkdir(parents=True, exist_ok=True)
                post_file.write_text(render_md(msg), encoding="utf-8", errors="replace")
                print(f"  ~ {post_file.relative_to(out)}")
                if msg.media and not _has_media(post_dir):
                    post_dir.mkdir(exist_ok=True)
                    try:
                        await client.download_media(msg, file=str(post_dir) + "/")
                    except Exception as e:
                        print(f"    media error: {e}")
            print("\nRedownload complete.")
            return

        async def run_sync(fetch_client=None):
            for channel in config["channels"]:
                while True:
                    try:
                        await sync_channel(client, channel, state, out,
                                           limit=args.limit, wait_time=args.wait_time,
                                           fetch_client=fetch_client,
                                           state_path=state_path)
                        break
                    except FloodWaitError as e:
                        print(f"  FloodWait: sleeping {e.seconds + 5}s...")
                        await asyncio.sleep(e.seconds + 5)

        if args.takeout:
            try:
                print("Using takeout session...")
                async with client.takeout() as takeout:
                    await run_sync(fetch_client=takeout)
            except Exception as e:
                print(f"  Takeout failed ({e}), falling back to regular mode.")
                await run_sync()
        else:
            await run_sync()

    print("\nSync complete.")


if __name__ == "__main__":
    asyncio.run(main())
