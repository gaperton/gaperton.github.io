#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10,<3.14"
# ///
"""
Copy posts from @gaperton_tech.old/ to @gaperton_tech/ with new naming.
Source files are never modified.

New name format: YYYY-MM-DD_HH-MM_<postId>.md
"""
import json
import re
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path


def read_frontmatter(md_file: Path) -> dict:
    result = {}
    try:
        for line in md_file.read_text(encoding="utf-8").splitlines():
            if line == "---" and result:
                break
            if line.startswith("id: "):
                result["id"] = int(line[4:].strip())
            elif line.startswith("date: "):
                result["date"] = line[6:].strip()
    except Exception:
        pass
    return result


def migrate(src_channel: Path, dst_channel: Path, dry_run: bool) -> None:
    copied = skipped = 0

    for month_dir in sorted(src_channel.iterdir()):
        if not month_dir.is_dir():
            continue

        for md in sorted(month_dir.glob("*.md")):
            fm = read_frontmatter(md)
            if not fm.get("id") or not fm.get("date"):
                print(f"  SKIP (missing frontmatter): {md.name}")
                skipped += 1
                continue

            dt = datetime.fromisoformat(fm["date"]).astimezone(timezone.utc)
            new_stem = f"{dt.strftime('%Y-%m-%d')}_{fm['id']}"
            dst_dir = dst_channel / month_dir.name
            dst_md = dst_dir / f"{new_stem}.md"

            if dst_md.exists():
                skipped += 1
                continue

            print(f"  {md.relative_to(src_channel.parent)} -> {dst_md.relative_to(dst_channel.parent)}")
            if not dry_run:
                dst_dir.mkdir(parents=True, exist_ok=True)
                # Strip embedded media links — media lives in .files/ dir instead
                text = re.sub(r'^!?\[.*?\]\(\./[^\n]*\)[ \t]*\n?', '', md.read_text(encoding="utf-8"), flags=re.MULTILINE).rstrip() + '\n'
                dst_md.write_text(text, encoding="utf-8")

            # Copy matching media directory (same stem as source file)
            src_media = month_dir / md.stem
            if src_media.is_dir():
                dst_media = dst_dir / f"{new_stem}.files"
                print(f"  {src_media.relative_to(src_channel.parent)}/ -> {dst_media.relative_to(dst_channel.parent)}/")
                if not dry_run:
                    dst_media.mkdir(parents=True, exist_ok=True)
                    for f in src_media.iterdir():
                        if f.is_file() and f.suffix != '.md':
                            shutil.copy2(f, dst_media / f.name)

            copied += 1

    label = "[DRY RUN] " if dry_run else ""
    print(f"\n{label}Done: {copied} copied, {skipped} skipped.")


if __name__ == "__main__":
    dry_run = "--dry-run" in sys.argv

    with open("config.json", encoding="utf-8") as f:
        config = json.load(f)

    out = Path(config.get("output_dir", "export"))

    for channel in config["channels"]:
        src = out / (channel + ".old")
        dst = out / channel
        if not src.exists():
            print(f"Source not found: {src}")
            continue
        print(f"Copying {src.name} -> {dst.name}  {'(dry run)' if dry_run else ''}\n")
        migrate(src, dst, dry_run)
