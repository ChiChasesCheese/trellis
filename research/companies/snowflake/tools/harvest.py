#!/usr/bin/env python3
"""面经收割器：Reddit（RSS）与小红书（移动端 SSR）。纯标准库。

为什么是这两个：2026-09-03 实测发现它们都**能**机器读取，而此前的 catalog 把
reddit 记成"全站 403 不可达"、把小红书记成"必须登录"。两条都是错的，纠正的代价
是几百条一手面经。

  python3 tools/harvest.py reddit --sub leetcode --q "stripe interview"
  python3 tools/harvest.py reddit-post 1k1d2rl --sub leetcode   # 正文 + 评论
  python3 tools/harvest.py sweep [--out DIR]                    # 预置矩阵，跑一遍全的
  python3 tools/harvest.py hn --q "stripe onsite" --tags comment  # Hacker News
  python3 tools/harvest.py xhs "<小红书分享链接>"                # 单篇笔记正文

## Reddit 的门在哪

- **必须带浏览器 UA**。默认 UA 一律 403。
- **HTML 页没用**：现在是 JS 壳，`<title>` 就是 "Reddit"，正文要 JS 才渲染。
- **`.json` 接口 403**（未鉴权已被封）。
- **`.rss` 可用**，而且单帖 `.rss` 连**评论全文**一起给——评论里常有比正文更具体的题面。
- **只能按 subreddit 搜**：`r/<sub>/search.rss?restrict_sr=1` 每次返回 25 条；
  全站 `search.rss` 返回 0 条。

## 小红书的门在哪

- **移动端 UA 是开关**：桌面 UA 会被 302 到 `/login`，移动 UA 直接吐 SSR。
- 完整笔记在 `window.__INITIAL_STATE__` 里，无需登录、无需签名。
- 分享短链里的 `xsec_token` 是访问凭证，**必须原样保留**，别清理 query。
- 做法取自用户自己的 `quant-stroller` 仓库 `src/quant/scout/social.py`（2026-07 实测）。
- **能取正文，不能按关键词搜**：站内搜索要登录，而搜索引擎几乎不索引小红书。
  所以笔记 URL 得由人来提供（App 里分享→复制链接）。
"""
from __future__ import annotations

import argparse
import html
import json
import random
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT_DEFAULT = ROOT / "catalog" / "discovery" / "harvest"

DESKTOP_UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
)
# 移动端 UA 是小红书免登录 SSR 的开关 — 桌面 UA 会被 302 到 /login。
MOBILE_UA = (
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) "
    "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"
)

# 宁滥勿缺：先全量收，去重和筛选留到最后一步。多搜一个组合的成本是一次 HTTP 请求，
# 漏掉一个组合的成本是一道没见过的题。
SUBS = [
    # 只留真的会返回结果的。2026-09-03 实测：这两个各返回 25 条，
    # 而 csMajors / ExperiencedDevs / developersIndia / InterviewPrep 等一律返回 0 条——
    # 它们要么关了搜索，要么没有 Stripe 内容。对着 0 结果的板块穷举只会白吃 429，
    # 把真正有货的两个板块也拖慢。宁滥勿缺不等于对着空井打水。
    "leetcode",
    "cscareerquestions",
]
QUERIES = [
    "stripe interview",
    "stripe oa",
    "stripe online assessment",
    "stripe onsite",
    "stripe virtual onsite",
    "stripe phone screen",
    "stripe coding round",
    "stripe new grad",
    "stripe intern",
    "stripe integration round",
    "stripe bug squash",
    "stripe debugging round",
    "stripe system design",
    "stripe hackerrank",
    "stripe take home",
    "stripe offer",
    "stripe recruiter",
    "stripe rejected",
    "stripe l2",
    "stripe backend interview",
]

# Hacker News 的 Algolia 接口完全开放、无需鉴权，story 和 comment 都能搜。
# 细节往往在评论里——搜 story 只能拿到标题。
HN_API = "https://hn.algolia.com/api/v1/search"
HN_QUERIES = [
    "stripe interview",
    "stripe interview process",
    "stripe onsite",
    "stripe hiring",
    "stripe engineering interview",
    "stripe take home",
    "stripe bug squash",
]

_ENTRY = re.compile(r"<entry>(.*?)</entry>", re.S)
_TAG = re.compile(r"<(\w+)[^>]*>(.*?)</\1>", re.S)
_LINK = re.compile(r'<link[^>]*href="([^"]+)"')
_CONTENT = re.compile(r'<content type="html">(.*?)</content>', re.S)
_STATE = re.compile(r"window\.__INITIAL_STATE__\s*=\s*(.*?)</script>", re.S)


def _get(url: str, ua: str = DESKTOP_UA, timeout: float = 25.0, tries: int = 4) -> str:
    """GET with polite backoff. 429 是收割器的常态，不是异常——尊重 Retry-After，
    没有就指数退避加抖动（所有客户端同时重来会把对方打得更狠）。"""
    delay = 2.0
    for attempt in range(tries):
        req = urllib.request.Request(url, headers={"User-Agent": ua})
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.read().decode("utf-8", "replace")
        except urllib.error.HTTPError as exc:
            if exc.code not in (429, 500, 502, 503, 504) or attempt == tries - 1:
                raise
            wait = float(exc.headers.get("Retry-After") or 0) or delay * (0.5 + random.random())
            print(f"  … HTTP {exc.code}，等 {wait:.1f}s 再试（第 {attempt + 1}/{tries} 次）", file=sys.stderr)
            time.sleep(wait)
            delay *= 2
    raise RuntimeError("unreachable")


def _strip_html(s: str) -> str:
    """RSS 把正文塞进 <content type="html">，且是**双重**转义。"""
    return re.sub(r"\s*\n\s*\n+", "\n\n", re.sub(r"<[^>]+>", "", html.unescape(html.unescape(s))).strip())


# ---------------------------------------------------------------- reddit


def reddit_search(sub: str, query: str, sort: str = "new") -> list[dict]:
    url = (
        f"https://www.reddit.com/r/{sub}/search.rss?"
        + urllib.parse.urlencode({"q": query, "restrict_sr": 1, "sort": sort})
    )
    try:
        xml = _get(url)
    except urllib.error.HTTPError as exc:
        print(f"  ! r/{sub} {query!r}: HTTP {exc.code}", file=sys.stderr)
        return []
    out = []
    for raw in _ENTRY.findall(xml):
        fields = {k: v for k, v in _TAG.findall(raw) if k in ("title", "published", "updated", "name")}
        link = _LINK.search(raw)
        href = link.group(1) if link else ""
        pid = ""
        m = re.search(r"/comments/([a-z0-9]+)/", href)
        if m:
            pid = m.group(1)
        out.append(
            {
                "id": pid,
                "sub": sub,
                "query": query,
                "title": html.unescape(fields.get("title", "")),
                "url": href,
                "published": fields.get("published", ""),
                "author": html.unescape(fields.get("name", "")),
            }
        )
    return out


def reddit_post(sub: str, post_id: str) -> dict:
    """单帖全文 + 评论。第一条 entry 是正文，其余是评论。"""
    xml = _get(f"https://www.reddit.com/r/{sub}/comments/{post_id}/.rss")
    bodies = [_strip_html(c) for c in _CONTENT.findall(xml)]
    # 标题只从 <entry> 里取：feed 级 <title> 是版块名，不是帖子名。
    entries = _ENTRY.findall(xml)
    titles = []
    for raw in entries:
        m = re.search(r"<title>(.*?)</title>", raw, re.S)
        if m:
            titles.append(html.unescape(m.group(1)).strip())
    return {
        "id": post_id,
        "sub": sub,
        "title": titles[0] if titles else "",
        "body": bodies[0] if bodies else "",
        "comments": bodies[1:],
        "url": f"https://www.reddit.com/r/{sub}/comments/{post_id}/",
    }


def cmd_reddit(a) -> None:
    hits = reddit_search(a.sub, a.q, a.sort)
    print(f"r/{a.sub} · {a.q!r} → {len(hits)} 条")
    for h in hits:
        print(f"  {h['published'][:10]}  {h['id']:8s}  {h['title'][:70]}")


def cmd_reddit_post(a) -> None:
    p = reddit_post(a.sub, a.id)
    print(f"# {p['title']}\n{p['url']}\n")
    print(p["body"][: a.chars])
    for i, c in enumerate(p["comments"][: a.comments], 1):
        print(f"\n--- 评论 {i} ---\n{c[: a.chars]}")


def cmd_sweep(a) -> None:
    out = Path(a.out or OUT_DEFAULT)
    out.mkdir(parents=True, exist_ok=True)
    seen: dict[str, dict] = {}
    stamp0 = time.strftime("%Y-%m-%d")
    idx_path = out / f"reddit_{stamp0}_index.json"
    for sub in SUBS:
        for q in QUERIES:
            for h in reddit_search(sub, q):
                if h["id"] and h["id"] not in seen:
                    seen[h["id"]] = h
            time.sleep(a.delay)
        # 每搜完一个板块就落盘，别把整轮搜索押在"能跑完"上
        idx_path.write_text(
            json.dumps(sorted(seen.values(), key=lambda h: h["published"], reverse=True),
                       ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"  r/{sub} 搜完，累计 {len(seen)} 帖（索引已落盘）")
    stamp = time.strftime("%Y-%m-%d")
    path = out / f"reddit_{stamp}.json"
    # 搜索结果先落盘：取全文要几十分钟，中途被杀不能把这一步的成果一起赔进去。
    (out / f"reddit_{stamp}_index.json").write_text(
        json.dumps(sorted(seen.values(), key=lambda h: h["published"], reverse=True), ensure_ascii=False, indent=1),
        encoding="utf-8",
    )
    print(f"搜索去重后 {len(seen)} 帖（索引已落盘），开始取全文…")

    # 断点续跑：已经取过的帖子不重复请求。
    posts: list[dict] = []
    done: set[str] = set()
    if path.exists():
        try:
            posts = json.loads(path.read_text(encoding="utf-8"))
            done = {p["id"] for p in posts}
            print(f"  发现上次的 {len(done)} 帖，跳过它们继续")
        except ValueError:
            posts, done = [], set()

    todo = [(pid, m) for pid, m in sorted(seen.items()) if pid not in done]
    for i, (pid, meta) in enumerate(todo, 1):
        try:
            p = reddit_post(meta["sub"], pid)
        except Exception as exc:  # noqa: BLE001 - 单帖失败不该中断整轮收割
            print(f"  ! {pid}: {exc}", file=sys.stderr)
            continue
        p["published"] = meta["published"]
        p["query"] = meta["query"]
        posts.append(p)
        # 每 5 帖存一次盘。usage limit / 超时 / 429 连环失败都可能随时终止进程，
        # 攒到最后一次性写文件等于把几十分钟的抓取押在"能跑完"上。
        if i % 5 == 0 or i == len(todo):
            path.write_text(json.dumps(posts, ensure_ascii=False, indent=1), encoding="utf-8")
            print(f"  …{i}/{len(todo)}（已存 {len(posts)} 帖）")
        time.sleep(a.delay)
    path.write_text(json.dumps(posts, ensure_ascii=False, indent=1), encoding="utf-8")
    substantive = [p for p in posts if len(p["body"]) > 200]
    print(f"\n写入 {path.relative_to(ROOT)}")
    print(f"  {len(posts)} 帖 · 其中正文 >200 字的 {len(substantive)} 帖 · 评论共 {sum(len(p['comments']) for p in posts)} 条")

    if not a.no_hn:
        hn_rows: list[dict] = []
        seen_hn: set[str] = set()
        for q in HN_QUERIES:
            for tags in ("comment", "story"):
                for r in hn_search(q, tags=tags):
                    if r["id"] not in seen_hn:
                        seen_hn.add(r["id"])
                        hn_rows.append(r)
                hn_path = out / f"hn_{stamp}.json"
                hn_path.write_text(json.dumps(hn_rows, ensure_ascii=False, indent=1), encoding="utf-8")
                time.sleep(a.delay)
        meaty = [r for r in hn_rows if len(r["text"]) > 200]
        print(f"写入 {hn_path.relative_to(ROOT)}")
        print(f"  {len(hn_rows)} 条 · 其中正文 >200 字的 {len(meaty)} 条")


# ---------------------------------------------------------------- hacker news


def hn_search(query: str, tags: str = "comment", pages: int = 3, per: int = 100) -> list[dict]:
    """搜 HN。tags='comment' 拿评论正文，tags='story' 拿帖子。"""
    out = []
    for page in range(pages):
        url = HN_API + "?" + urllib.parse.urlencode(
            {"query": query, "tags": tags, "hitsPerPage": per, "page": page}
        )
        try:
            data = json.loads(_get(url))
        except Exception as exc:  # noqa: BLE001 - 一页失败不该中断整轮
            print(f"  ! HN {query!r} p{page}: {exc}", file=sys.stderr)
            break
        hits = data.get("hits") or []
        for h in hits:
            text = re.sub(r"<[^>]+>", "", html.unescape(h.get("comment_text") or h.get("story_text") or ""))
            out.append(
                {
                    "id": h.get("objectID"),
                    "title": h.get("title") or h.get("story_title") or "",
                    "text": text.strip(),
                    "author": h.get("author"),
                    "created_at": h.get("created_at"),
                    "url": f"https://news.ycombinator.com/item?id={h.get('objectID')}",
                    "query": query,
                    "kind": tags,
                }
            )
        if len(hits) < per:
            break
    return out


def cmd_hn(a) -> None:
    rows = hn_search(a.q, tags=a.tags, pages=a.pages)
    print(f"HN {a.q!r} ({a.tags}) → {len(rows)} 条")
    for r in rows[: a.limit]:
        print(f"  {r['created_at'][:10]}  {r['title'][:50]:52s} {r['text'][:90]}")


# ---------------------------------------------------------------- 小红书


def xhs_note(url: str) -> dict:
    """取一篇笔记。url 必须是**分享链接原样**——里面的 xsec_token 是访问凭证。"""
    raw = _get(url, ua=MOBILE_UA)
    m = _STATE.search(raw)
    if not m:
        raise SystemExit("没找到 __INITIAL_STATE__：链接可能过期、被删，或 xsec_token 被清掉了")
    blob = m.group(1).strip().rstrip(";")
    # XHS 会在 JSON 里直接吐字面量 undefined，先归一成 null 才能解析。
    blob = re.sub(r"\bundefined\b", "null", blob)
    try:
        state = json.loads(blob)
    except ValueError as exc:
        raise SystemExit(f"SSR 状态解析失败：{exc}") from exc
    note_map = (state.get("note") or {}).get("noteDetailMap") or {}
    for nid, wrap in note_map.items():
        note = wrap.get("note") or {}
        if not note:
            continue
        return {
            "id": nid,
            "title": note.get("title", ""),
            "desc": note.get("desc", ""),
            "time": note.get("time"),
            "images": [im.get("urlDefault") for im in (note.get("imageList") or [])],
            "url": url,
        }
    raise SystemExit("SSR 状态里没有笔记内容（可能是列表页而非笔记页）")


def cmd_xhs(a) -> None:
    n = xhs_note(a.url)
    print(f"# {n['title']}\n{n['url']}\n")
    print(n["desc"])
    if n["images"]:
        print(f"\n（{len(n['images'])} 张图；图文笔记的干货常在图里，需要人工或视觉模型读）")
        for u in n["images"][: a.images]:
            print(f"  {u}")


def main(argv=None) -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("reddit", help="搜一个 subreddit")
    s.add_argument("--sub", default="leetcode")
    s.add_argument("--q", default="stripe interview")
    s.add_argument("--sort", default="new", choices=["new", "relevance", "top"])
    s.set_defaults(fn=cmd_reddit)

    s = sub.add_parser("reddit-post", help="取单帖正文 + 评论")
    s.add_argument("id")
    s.add_argument("--sub", default="leetcode")
    s.add_argument("--chars", type=int, default=1500)
    s.add_argument("--comments", type=int, default=5)
    s.set_defaults(fn=cmd_reddit_post)

    s = sub.add_parser("sweep", help="预置矩阵跑一遍，落 JSON")
    s.add_argument("--out", default=None)
    s.add_argument("--delay", type=float, default=1.0, help="每次请求之间等多久（别把人家打挂）")
    s.add_argument("--no-hn", action="store_true", help="跳过 Hacker News")
    s.set_defaults(fn=cmd_sweep)

    s = sub.add_parser("hn", help="搜 Hacker News（Algolia，开放接口）")
    s.add_argument("--q", default="stripe interview")
    s.add_argument("--tags", default="comment", choices=["comment", "story"])
    s.add_argument("--pages", type=int, default=3)
    s.add_argument("--limit", type=int, default=20)
    s.set_defaults(fn=cmd_hn)

    s = sub.add_parser("xhs", help="取一篇小红书笔记（需要你提供分享链接）")
    s.add_argument("url")
    s.add_argument("--images", type=int, default=5)
    s.set_defaults(fn=cmd_xhs)

    a = p.parse_args(argv)
    a.fn(a)


if __name__ == "__main__":
    try:
        main()
    except BrokenPipeError:
        pass
