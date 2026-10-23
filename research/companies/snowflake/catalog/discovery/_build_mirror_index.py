import json
from pathlib import Path

DIR = Path(__file__).parent / "mirror_1p3a_snowflake"
posts = json.loads((DIR / "_parsed.json").read_text(encoding="utf-8"))

# Drop the one off-topic match (Agoda thread that only mentions "Snowflake" as a SQL dialect name)
posts = [p for p in posts if p["1p3a_id"] != "1185287"]

lines = [
    "# t.me/s/usinterview mirror — query `snowflake` (2026-09-13)",
    "",
    "Source: Telegram public preview of channel `usinterview` (镜像/转发一亩三分地北美面经 bot)."
    " Fetched via `curl` with a desktop UA against `https://t.me/s/usinterview?q=snowflake`, paging"
    " backwards with `&before=<lowest message id>`. Page 3 (`before=28631`) returned 0 matching"
    " messages, so the query is exhausted (well under the 8-page / 2024-06 cutoff budget — all 22"
    " hits are from 2026-05 through 2026-09, i.e. this channel's snowflake-tagged backlog is short,"
    " not truncated by paging).",
    "",
    "Pages saved: `page_1.html` (20 hits, ids 28723-29627), `page_2.html` (2 hits, ids 28631-28661),"
    " `page_3.html` (0 hits, confirms exhaustion). One off-topic hit (Agoda DA thread that only"
    " name-drops \"Snowflake\" as the SQL warehouse used in an OA, id 1185287) was dropped from the"
    " table below.",
    "",
    "Each Telegram message is itself a second-hand repost of a 1point3acres.com/bbs thread (the"
    " `usinterview` bot auto-forwards new 面经 posts tagged `#snowflake`); the text below is the"
    " Telegram caption + the site's own link-preview description (both already truncated by"
    " Telegram/the source site, not by us) — full thread bodies are behind 1point3acres's login wall"
    " (see raw_1p3a_nextdata/ for the direct-access attempt and why it failed).",
    "",
    "| Date (UTC) | Title | First ~600 chars | 1p3a thread | Telegram link |",
    "|---|---|---|---|---|",
]

for p in posts:
    date = p["datetime"][:10]
    title = p["title"].split("|")[0].strip() or p["text"][:40]
    body = (p["text"] + " — " + p["desc"]).strip(" —")
    body = body.replace("\n", " ").replace("|", "\\|")
    body = body[:600]
    thread = f"[{p['1p3a_id']}](https://www.1point3acres.com/bbs/thread-{p['1p3a_id']}-1-1.html)" if p["1p3a_id"] else ""
    tg = f"[tg]({p['tg_url']})"
    lines.append(f"| {date} | {title} | {body} | {thread} | {tg} |")

(DIR / "index.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
print(f"wrote index.md with {len(posts)} rows")
