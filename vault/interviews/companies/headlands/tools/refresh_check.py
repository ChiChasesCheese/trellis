#!/usr/bin/env python3
"""来源登记表的维护与复验工具（catalog/sources.json ← → catalog/SOURCES.md）。

题库的每一条结论都挂在一个 URL 上。时间一长，问题不是"当初有没有来源"，而是
**这些来源今天还在不在、有没有更新过**。这个工具把那件事变成一条命令。

  python3 tools/refresh_check.py rebuild     # 重扫仓库 md，刷新 URL 清单（保留人工维护的 sites 段）
  python3 tools/refresh_check.py stale       # 按站点复验周期，列出到期该复查的来源
  python3 tools/refresh_check.py ping        # 真发 HTTP 请求探活，回写状态码（403 是正常结果，见下）
  python3 tools/refresh_check.py report      # 打印中文汇总（可粘进 SOURCES.md）

关于 403，有两种完全不同的成因，别混为一谈：
  1. **站点反爬**：leetcode.com 的 discuss 页面、1point3acres、medium 对脚本一律 403。这些站在
     sources.json 里标 `access: manual`，`ping` 会跳过它们，`stale` 单列一栏。
     （teamblind 不在此列：它只卡机器人 UA，本工具用浏览器 UA 能拿到 200。
       leetcode 的 discuss 正文也另有活路——GraphQL 端点可用，见 SOURCES.md。）
  2. **你这台机器的出口被限制**：在沙箱/CI 容器里跑，连 github.com 都可能 403。这时 403
     跟站点死活毫无关系。所以每次探活都记下 `checked_from`（机器标签），`report` 会按标签
     分组并对沙箱来源的结果给出警告。**要拿准数，请在自己的机器上跑 ping。**
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import platform
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STORE = ROOT / "catalog" / "sources.json"
URL_RE = re.compile(r'https?://[^\s)\]｜|`"<>]+')
SCAN = ["catalog", "loop/raw", "loop/CATALOG.md", "loop/LOOP_GUIDE.md", "reports", "skills_matrix.md"]
TODAY = dt.date.today().isoformat()
# 用真实浏览器 UA：teamblind 对机器人 UA 返回 403、对浏览器 UA 返回 200，
# 差别只在这一个 header 上。老实标 bot 的代价是把活着的来源误判成死链。
UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
)


def _domain(url: str) -> str:
    try:
        return re.sub(r"^www\.", "", url.split("//", 1)[1].split("/", 1)[0])
    except IndexError:
        return "?"


def _load() -> dict:
    if STORE.exists():
        return json.loads(STORE.read_text(encoding="utf-8"))
    return {"generated": TODAY, "sites": {}, "urls": {}}


def _save(data: dict) -> None:
    STORE.parent.mkdir(parents=True, exist_ok=True)
    STORE.write_text(json.dumps(data, ensure_ascii=False, indent=1, sort_keys=False) + "\n", encoding="utf-8")


def _scan_files() -> list[Path]:
    files: list[Path] = []
    for entry in SCAN:
        p = ROOT / entry
        if p.is_dir():
            files += sorted(p.rglob("*.md"))
        elif p.exists():
            files.append(p)
    return files


def cmd_rebuild(_a) -> None:
    data = _load()
    found: dict[str, set[str]] = {}
    for f in _scan_files():
        rel = str(f.relative_to(ROOT))
        for raw in URL_RE.findall(f.read_text(encoding="utf-8", errors="replace")):
            found.setdefault(raw.rstrip(".,;:·、）)】]"), set()).add(rel)

    urls = data.setdefault("urls", {})
    for url, citers in found.items():
        entry = urls.setdefault(url, {"first_seen": TODAY, "last_verified": None, "http": None, "checked": None})
        entry["domain"] = _domain(url)
        entry["cited_by"] = sorted(citers)
    gone = [u for u in urls if u not in found]
    for u in gone:
        urls[u]["cited_by"] = []
        urls[u]["orphan"] = True

    sites = data.setdefault("sites", {})
    for url in found:
        sites.setdefault(
            _domain(url),
            {"tier": 3, "kind": "未分类", "access": "unknown", "cadence_days": 90, "last_verified": None, "note": ""},
        )
    for dom, site in sites.items():
        site["url_count"] = sum(1 for u, e in urls.items() if e.get("domain") == dom and e.get("cited_by"))

    data["generated"] = TODAY
    _save(data)
    live = sum(1 for e in urls.values() if e.get("cited_by"))
    print(f"rebuild: {live} 条在用 URL · {len(gone)} 条已从正文移除 · {len(sites)} 个站点")


def cmd_stale(a) -> None:
    data = _load()
    today = dt.date.fromisoformat(TODAY)
    auto, manual, never = [], [], []
    for dom, site in sorted(data.get("sites", {}).items(), key=lambda kv: -kv[1].get("url_count", 0)):
        if not site.get("url_count"):
            continue
        last = site.get("last_verified")
        if not last:
            never.append((dom, site))
            continue
        age = (today - dt.date.fromisoformat(last)).days
        if age >= site.get("cadence_days", 90):
            (manual if site.get("access") == "manual" else auto).append((dom, site, age))

    def show(title, rows, with_age=True):
        print(f"\n== {title}（{len(rows)}）==")
        for row in rows[: a.limit]:
            dom, site = row[0], row[1]
            age = f"{row[2]} 天前" if with_age else "从未复验"
            print(f"  {dom:28s} {site.get('url_count', 0):3d} 条  周期 {site.get('cadence_days')}d  上次 {age}")
            if site.get("recheck"):
                print(f"      复验方式：{site['recheck']}")

    show("到期 · 可脚本复验", auto)
    show("到期 · 只能人工复验（403/需登录）", manual)
    show("从未复验", never, with_age=False)
    if not (auto or manual or never):
        print("所有来源都在复验周期内。")


def _label(explicit: str | None) -> str:
    return explicit or os.environ.get("SOURCE_CHECK_LABEL") or platform.node() or "unknown"


def cmd_ping(a) -> None:
    data = _load()
    label = _label(a.label)
    urls = data.get("urls", {})
    sites = data.get("sites", {})
    targets = [
        (u, e)
        for u, e in urls.items()
        if e.get("cited_by")
        and (not a.domain or e.get("domain") == a.domain)
        and (a.recheck or not e.get("checked"))
        and sites.get(e.get("domain"), {}).get("access") != "manual"
    ][: a.limit]
    if not targets:
        print("没有需要探活的 URL（用 --recheck 强制重查，或 --domain 指定站点）。")
        return
    for url, entry in targets:
        code: object
        try:
            req = urllib.request.Request(url, headers={"User-Agent": a.ua}, method="GET")
            with urllib.request.urlopen(req, timeout=a.timeout) as resp:
                code = resp.status
        except urllib.error.HTTPError as exc:
            code = exc.code
        except Exception as exc:  # noqa: BLE001 - network layer raises a zoo of types
            code = type(exc).__name__
        entry["http"] = code
        entry["checked"] = TODAY
        entry["checked_from"] = label
        if code == 200:
            entry["last_verified"] = TODAY
        print(f"  {str(code):>12}  {url}")
    _save(data)
    print(f"\n已回写 {len(targets)} 条到 {STORE.relative_to(ROOT)}（machine={label}）")
    print("提醒：403 可能是站点反爬，也可能是这台机器的出口被限制。换机器复跑能区分两者。")


def cmd_report(_a) -> None:
    data = _load()
    urls = data.get("urls", {})
    sites = data.get("sites", {})
    live = {u: e for u, e in urls.items() if e.get("cited_by")}
    print(f"# 来源体检 · {TODAY}\n")
    print(f"在用 URL {len(live)} 条 · 站点 {sum(1 for s in sites.values() if s.get('url_count'))} 个\n")
    print("| 站点 | 条数 | 层级 | 类型 | 可抓取 | 复验周期 | 上次复验 |")
    print("|---|---|---|---|---|---|---|")
    for dom, site in sorted(sites.items(), key=lambda kv: -kv[1].get("url_count", 0)):
        if not site.get("url_count"):
            continue
        print(
            f"| {dom} | {site['url_count']} | T{site.get('tier')} | {site.get('kind')} | "
            f"{site.get('access')} | {site.get('cadence_days')}d | {site.get('last_verified') or '—'} |"
        )
    labels: dict[str, int] = {}
    for e in live.values():
        if e.get("checked"):
            labels[e.get("checked_from", "unknown")] = labels.get(e.get("checked_from", "unknown"), 0) + 1
    if labels:
        print("\n## 探活是在哪台机器上跑的\n")
        for lab, n in sorted(labels.items(), key=lambda kv: -kv[1]):
            print(f"- `{lab}` — {n} 条")
        print("\n沙箱/CI 容器的出口可能被限制（连 github.com 都会 403），那种 403 不是站点结论。")
    dead = {u: e for u, e in live.items() if isinstance(e.get("http"), int) and e["http"] >= 400}
    if dead:
        print(f"\n## 探活异常（{len(dead)}）—— 先按上面那条判断是站点问题还是网络问题\n")
        for u, e in sorted(dead.items(), key=lambda kv: kv[1]["http"]):
            print(f"- `{e['http']}` [{e.get('checked_from', '?')}] {u}  ←  {', '.join(e['cited_by'][:2])}")


def main(argv=None) -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("rebuild").set_defaults(fn=cmd_rebuild)
    s = sub.add_parser("stale")
    s.add_argument("--limit", type=int, default=40)
    s.set_defaults(fn=cmd_stale)
    s = sub.add_parser("ping")
    s.add_argument("--limit", type=int, default=25)
    s.add_argument("--domain", default=None)
    s.add_argument("--timeout", type=float, default=12.0)
    s.add_argument("--recheck", action="store_true", help="连已经查过的也重查")
    s.add_argument("--label", default=None, help="这次是在哪台机器上跑的（默认取主机名）")
    s.add_argument("--ua", default=UA, help="覆盖 User-Agent（默认用浏览器 UA，见文件头说明）")
    s.set_defaults(fn=cmd_ping)
    sub.add_parser("report").set_defaults(fn=cmd_report)
    a = p.parse_args(argv)
    a.fn(a)


if __name__ == "__main__":
    try:
        main()
    except BrokenPipeError:  # `... | head` closes the pipe early; that is not an error
        try:
            sys.stdout.close()
        finally:
            os._exit(0)
