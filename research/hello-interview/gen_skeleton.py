"""Write skeleton/hello-interview.yaml from research/hello-interview/pages.json, mirroring Hello Interview's own order.

    uv run python research/hello-interview/gen_skeleton.py

Two sub-decks, System Design and Low-Level Design, each with Hello Interview's sections in its order and one node per
page, split into 摘要 / 考点 / 拓展 leaves. After the material is learned, these leaves are meant to merge into the system-design and
low-level-design domains (research/hello-interview/BUILD.md).
"""
from __future__ import annotations

import json
import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
PAGE_PARTS = [("notes", "摘要", "按小节总结这一章的核心内容。"),
              ("exam", "考点", "这一章里的内容会怎么被问到。"),
              ("beyond", "拓展", "这一章没讲、但 senior 面试会追问的内容。")]
TRACKS = [("system-design", "系统设计（System Design）"), ("low-level-design", "低层设计（Low-Level Design）")]
SECTIONS = {
    "system-design": [("in-a-hurry", "速成（In a Hurry）"), ("core-concepts", "核心概念（Core Concepts）"),
                      ("patterns", "常见模式（Patterns）"), ("deep-dives", "关键技术深入（Key Technologies）"),
                      ("problem-breakdowns", "经典题拆解（Problem Breakdowns）"), ("in-the-wild", "真实系统案例（In the Wild）")],
    "low-level-design": [("in-a-hurry", "速成（In a Hurry）"), ("concurrency", "并发（Concurrency）"),
                         ("problem-breakdowns", "经典题拆解（Problem Breakdowns）")],
}
ZH = {
    "system-design/in-a-hurry/introduction": "系统设计速成：总览", "system-design/in-a-hurry/how-to-prepare": "怎样准备系统设计面试",
    "system-design/in-a-hurry/delivery": "答题框架（Delivery Framework）", "system-design/in-a-hurry/core-concepts": "核心概念速览",
    "system-design/in-a-hurry/key-technologies": "关键技术速览", "system-design/in-a-hurry/patterns": "常见模式速览",
    "system-design/in-a-hurry/problem-breakdowns": "经典题拆解怎么用",
    "system-design/core-concepts/networking-essentials": "网络基础", "system-design/core-concepts/api-design": "API 设计",
    "system-design/core-concepts/data-modeling": "数据建模", "system-design/core-concepts/caching": "缓存",
    "system-design/core-concepts/sharding": "分片（Sharding）", "system-design/core-concepts/consistent-hashing": "一致性哈希",
    "system-design/core-concepts/cap-theorem": "CAP 定理", "system-design/core-concepts/db-indexing": "数据库索引",
    "system-design/core-concepts/numbers-to-know": "必须知道的数字",
    "system-design/patterns/realtime-updates": "实时更新", "system-design/patterns/dealing-with-contention": "处理争用（Contention）",
    "system-design/patterns/multi-step-processes": "多步骤流程", "system-design/patterns/scaling-reads": "扩展读",
    "system-design/patterns/scaling-writes": "扩展写", "system-design/patterns/large-blobs": "大文件（Blob）处理",
    "system-design/patterns/long-running-tasks": "长时间运行的任务",
    "system-design/deep-dives/redis": "Redis", "system-design/deep-dives/elasticsearch": "Elasticsearch",
    "system-design/deep-dives/kafka": "Kafka", "system-design/deep-dives/temporal": "Temporal",
    "system-design/deep-dives/api-gateway": "API 网关", "system-design/deep-dives/cassandra": "Cassandra",
    "system-design/deep-dives/dynamodb": "DynamoDB", "system-design/deep-dives/postgres": "PostgreSQL",
    "system-design/deep-dives/flink": "Flink", "system-design/deep-dives/zookeeper": "ZooKeeper",
    "system-design/deep-dives/proximity-search": "邻近搜索（Proximity Search）", "system-design/deep-dives/vector-databases": "向量数据库",
    "system-design/deep-dives/time-series-databases": "时序数据库", "system-design/deep-dives/data-structures-for-big-data": "大数据数据结构",
    "system-design/deep-dives/change-data-capture": "变更数据捕获（CDC）",
    "system-design/problem-breakdowns/bitly": "短链接服务（Bitly）", "system-design/problem-breakdowns/dropbox": "文件存储（Dropbox）",
    "system-design/problem-breakdowns/gopuff": "本地配送（Gopuff）", "system-design/problem-breakdowns/ticketmaster": "票务预订（Ticketmaster）",
    "system-design/problem-breakdowns/fb-news-feed": "Facebook 信息流", "system-design/problem-breakdowns/tinder": "约会应用（Tinder）",
    "system-design/problem-breakdowns/leetcode": "在线判题平台（LeetCode）", "system-design/problem-breakdowns/whatsapp": "即时通讯（WhatsApp）",
    "system-design/problem-breakdowns/distributed-rate-limiter": "分布式限流器", "system-design/problem-breakdowns/youtube": "视频平台（YouTube）",
    "system-design/problem-breakdowns/fb-live-comments": "Facebook 直播评论", "system-design/problem-breakdowns/top-k": "YouTube 热门 Top K",
    "system-design/problem-breakdowns/uber": "网约车（Uber）", "system-design/problem-breakdowns/web-crawler": "网络爬虫",
    "system-design/problem-breakdowns/ad-click-aggregator": "广告点击聚合", "system-design/problem-breakdowns/fb-post-search": "Facebook 帖子搜索",
    "system-design/problem-breakdowns/yelp": "商户点评（Yelp）", "system-design/problem-breakdowns/instagram": "图片分享（Instagram）",
    "system-design/problem-breakdowns/strava": "运动记录（Strava）", "system-design/problem-breakdowns/distributed-cache": "分布式缓存（Redis）",
    "system-design/problem-breakdowns/online-auction": "在线拍卖（eBay）", "system-design/problem-breakdowns/job-scheduler": "分布式任务调度（Airflow）",
    "system-design/problem-breakdowns/google-news": "新闻聚合（Google News）", "system-design/problem-breakdowns/camelcamelcamel": "价格追踪（CamelCamelCamel）",
    "system-design/problem-breakdowns/notification-system": "通知系统", "system-design/problem-breakdowns/robinhood": "股票交易（Robinhood）",
    "system-design/problem-breakdowns/google-docs": "协同文档（Google Docs）", "system-design/problem-breakdowns/payment-system": "支付系统（Stripe）",
    "system-design/problem-breakdowns/metrics-monitoring": "指标监控（Datadog）", "system-design/problem-breakdowns/online-chess": "在线国际象棋",
    "system-design/problem-breakdowns/chatgpt": "ChatGPT", "system-design/problem-breakdowns/flash-sale": "秒杀系统",
    "system-design/in-the-wild": "真实系统案例：总览", "system-design/in-the-wild/shopify-inventory-reservations": "Shopify 库存预留：从 Redis 到 MySQL",
    "system-design/in-the-wild/discord-messages-scylladb": "Discord 万亿消息迁到 ScyllaDB", "system-design/in-the-wild/slack-job-queue": "Slack 在 Redis 任务队列前加 Kafka",
    "system-design/in-the-wild/figma-multiplayer": "Figma 多人编辑与简化 CRDT", "system-design/in-the-wild/spotify-data-lake-point-queries": "Spotify 在 EB 级数据湖上做点查",
    "system-design/in-the-wild/meta-zgateway-zippydb": "Meta 把数据库扩展到百万客户端的 5 个技巧",
    "low-level-design/in-a-hurry/introduction": "低层设计速成：总览", "low-level-design/in-a-hurry/delivery": "答题框架（Delivery Framework）",
    "low-level-design/in-a-hurry/design-principles": "设计原则", "low-level-design/in-a-hurry/oop-concepts": "面向对象概念",
    "low-level-design/in-a-hurry/patterns": "设计模式", "low-level-design/concurrency/intro": "并发入门",
    "low-level-design/concurrency/correctness": "并发正确性", "low-level-design/concurrency/coordination": "线程协调",
    "low-level-design/concurrency/scarcity": "稀缺资源", "low-level-design/problem-breakdowns/connect-four": "四子棋（Connect Four）",
    "low-level-design/problem-breakdowns/amazon-locker": "Amazon 快递柜", "low-level-design/problem-breakdowns/elevator": "电梯",
    "low-level-design/problem-breakdowns/parking-lot": "停车场", "low-level-design/problem-breakdowns/file-system": "文件系统",
    "low-level-design/problem-breakdowns/bookmyshow": "电影票预订（BookMyShow）", "low-level-design/problem-breakdowns/logging-service": "日志服务",
    "low-level-design/problem-breakdowns/rate-limiter": "限流器", "low-level-design/problem-breakdowns/inventory-management": "库存管理",
}


def main() -> None:
    pages = json.loads((ROOT / "research/hello-interview/pages.json").read_text(encoding="utf-8"))
    nodes = []
    # 高频题库 first (Chi, 2026-11-01: the questions matter most; the courses are their prerequisites)
    qb_path = ROOT / "research/hello-interview/qb_selection.json"
    # Chi (2026-11-01): each question's prerequisites are a sub-deck of that question. A concept page lives once, under
    # the most-reported question that needs it; the course branches keep only pages no question uses.
    cards_dir = ROOT / "vault/domains/hello-interview/cards"
    home_path = ROOT / "research/hello-interview/concept_home.json"
    home = json.loads(home_path.read_text(encoding="utf-8")) if home_path.exists() else {}
    for f in sorted(cards_dir.glob("*/*/*.md")):  # course cards: remember the course leaf each one was written for
        rel = str(f.relative_to(cards_dir))
        if rel.startswith(("qb/", "premium/")) or rel in home:
            continue
        m = re.search(r"^node: (\S+)$", f.read_text(encoding="utf-8"), re.M)
        if m:
            home[rel] = m.group(1)
    home_path.write_text(json.dumps(home, ensure_ascii=False, indent=1, sort_keys=True), encoding="utf-8")
    pat_path = ROOT / "research/hello-interview/patterns.json"
    patterns = json.loads(pat_path.read_text(encoding="utf-8"))["patterns"] if pat_path.exists() else []
    pattern_of: dict[str, list[str]] = {}  # body slug -> titles of the cross-question patterns it appears in
    for x in patterns:
        for q in x["questions"]:
            pattern_of.setdefault(q["slug"], []).append(re.sub(r"\s*[（(].*?[）)]", "", x["title"]))
    placed: dict[str, str] = {}      # course leaf -> prerequisite leaf under a question
    where: dict[str, str] = {}       # prerequisite leaf -> title of the question it sits under
    extra = {}
    for f in sorted((ROOT / "research/hello-interview").glob("*_meta_*.json")):  # zh titles + requires from the agents
        extra.update(json.loads(f.read_text(encoding="utf-8")))
    card_meta: dict[str, str] = {}   # stub path -> header meta
    points_home: dict[str, str] = {}  # shared body slug -> the leaf holding its granular cards

    def question_branch(prefix: str, track: str, items: list[dict]) -> list[dict]:
        """One node per question: its new prerequisite pages (first come, first placed), then the answer."""
        leaves = []
        for q in items:
            e = extra.get(q["slug"], {})
            title = q.get("title_zh") or e.get("title") or q["title"]
            qid = f"{prefix}.{track}.{q['slug']}"
            pre = []
            for c in e.get("requires", []):
                if c in placed or c not in set(home.values()):
                    continue  # already a prerequisite of an earlier question, or a page without cards
                placed[c] = f"{qid}.pre-{c.replace('.', '-')}"
                where[placed[c]] = title
                key = next((pk for pk in ZH if pk.endswith("/" + c.split(".")[-1]) and pk.startswith(
                    "system-design" if c.startswith("sd.") else "low-level-design")), "")
                pre.append({"id": placed[c], "title": "先修 · " + ZH.get(key, c.split(".")[-1]), "summary": f"{title} 用到的概念。"})
            answer = {"id": f"{qid}.answer", "title": "解答 · " + title, "summary": q.get("why") or f"被报告 {q['reports']} 次。"}
            later = [placed[c] for c in e.get("requires", []) if c in placed and not placed[c].startswith(qid + ".")]
            if later:
                answer["requires"] = later  # prerequisites that sit under an earlier question
            elsewhere = list(dict.fromkeys(where[x] for x in later))
            pats = pattern_of.get(q.get("body_slug", q["slug"]), [])
            card_meta[q["stub"]] = (q["meta"] + (f" · 先修见：{'、'.join(elsewhere)}" if elsewhere else "")
                                    + (f" · 模式：{'、'.join(pats[:5])}" if pats else ""))
            kids = pre + [answer]
            body_slug = q.get("body_slug", q["slug"])
            if body_slug not in points_home and any(x for d in ("points", "premium/points") for x in (cards_dir / d / body_slug).glob("*.md")):
                points_home[body_slug] = f"{qid}.points"  # granular cards live under the first question using the body
                kids.append({"id": f"{qid}.points", "title": "要点 · " + title,
                             "summary": "从完整解答拆出的单个知识点，每张注明出自哪一部分；可以单独随机复习。"})
            leaves.append({"id": qid, "title": title, "summary": answer["summary"], "children": kids})
        return leaves

    more = json.loads((ROOT / "research/hello-interview/more_selection.json").read_text(encoding="utf-8"))
    bank_path = ROOT / "sources/local/hello-interview/premium/questions.json"
    bank = json.loads(bank_path.read_text(encoding="utf-8")) if bank_path.exists() else []

    def more_items(track: str, tiktok: bool) -> list[dict]:
        """Questions from the full bank. Their answers and stubs stay in the gitignored premium folder."""
        out = []
        for q in more["questions"]:
            if q["track"] != track or (tiktok and not q.get("tiktok")):
                continue
            rec = next((b for b in bank if b["slug"] == q["slug"] or b["title"] == q.get("search")), {})
            ups = rec.get("upvotes") or []
            comp = sorted({u["company"] for u in ups if u.get("company")})
            last = max((u.get("approxAskedOn") or "")[:7] for u in ups) if ups else ""
            meta = f"被报告 {len(ups)} 次" + (f" · {'、'.join(comp[:5])}" if comp else "") + (f" · 最近 {last}" if last else "")
            prefix = "tt" if tiktok else "qb"
            stub = cards_dir / f"premium/{prefix}/{track}/hi-{prefix}-{q['slug']}.md"
            if (ROOT / f"vault/domains/hello-interview/premium/bodies/{q['slug']}.md").exists():
                stub.parent.mkdir(parents=True, exist_ok=True)
                stub.write_text(f"---\nid: hi-{prefix}-{q['slug']}\nnode: {prefix}.{track}.{q['slug']}.answer\ntype: qa\n"
                                f"body: domains/hello-interview/premium/bodies/{q['slug']}\nmeta: \"\"\n---\n", encoding="utf-8")
            out.append({**q, "title": rec.get("title", q["title_zh"]), "reports": len(ups), "why": f"{q['title_zh']}：完整解答。", "meta": meta,  # the counts stay in the gitignored stub
                        "stub": str(stub.relative_to(cards_dir))})
        return out

    if qb_path.exists():
        qb = json.loads(qb_path.read_text(encoding="utf-8"))
        kids = []
        for track, title in (("sd", "系统设计高频题"), ("lld", "低层设计高频题")):
            items = []
            for q in qb:
                if q["track"] != track:
                    continue
                comp = "、".join(q["companies"][:5]) + (" 等" if len(q["companies"]) > 5 else "")
                items.append({**q, "stub": f"qb/{track}/hi-qb-{q['slug']}.md",
                              "meta": f"被报告 {q['reports']} 次" + (f" · {comp}" if comp else "") + (f" · 最近 {q['last'][:7]}" if q["last"] else "")})
            items += more_items(track, False)
            kids.append({"id": f"qb.{track}", "title": title, "summary": f"{title}：按被报告次数从高到低。",
                         "children": question_branch("qb", track, items)})
        nodes.append({"id": "qb", "order": 1, "core": True, "title": "高频真题（Question Bank）",
                      "summary": "Hello Interview 题库里被报告最多的设计题，每题一张完整解答；课程部分是它们的先修。", "children": kids})
    # TikTok / ByteDance: payments first, then general (Chi, 2026-11-01). Reused questions point at the same shared body.
    tt_path = ROOT / "research/hello-interview/tiktok_selection.json"
    if tt_path.exists():
        kids = []
        for track, title in (("sd", "TikTok 系统设计"), ("lld", "TikTok 低层设计")):
            items = []
            for q in json.loads(tt_path.read_text(encoding="utf-8"))["questions"]:
                if q["track"] != track:
                    continue
                body = ROOT / f"vault/interviews/core/design-questions/{q['slug']}.md"
                stub = cards_dir / f"tt/{track}/hi-tt-{q['slug']}.md"
                if body.exists():
                    stub.parent.mkdir(parents=True, exist_ok=True)
                    stub.write_text(f"---\nid: hi-tt-{q['slug']}\nnode: tt.{track}.{q['slug']}.answer\ntype: qa\n"
                                    f"body: interviews/core/design-questions/{q['slug']}\nmeta: \"\"\n---\n", encoding="utf-8")
                items.append({**q, "title_zh": q["title"], "title": q.get("title_en", q["title"]), "reports": 0,
                              "stub": f"tt/{track}/hi-tt-{q['slug']}.md", "meta": q["why"]})
            items += more_items(track, True)
            kids.append({"id": f"tt.{track}", "title": title, "summary": f"{title}：支付方向在前，其后是通用高频题。",
                         "children": question_branch("tt", track, items)})
        lc_kids = []
        for slug in more["tiktok_leetcode"]:  # the same shared problem body as every LeetCode deck
            body = ROOT / f"vault/interviews/core/leetcode/problems/{slug}.md"
            if not body.exists():
                continue
            name = re.search(r"^\*\*(LC .+?)\*\*", body.read_text(encoding="utf-8"), re.M)
            stub = cards_dir / f"tt/lc/hi-tt-lc-{slug}.md"
            stub.parent.mkdir(parents=True, exist_ok=True)
            stub.write_text(f"---\nid: hi-tt-lc-{slug}\nnode: tt.lc.{slug}\ntype: qa\nbody: interviews/core/leetcode/problems/{slug}\n"
                            "meta: TikTok 面试报告\n---\n", encoding="utf-8")
            lc_kids.append({"id": f"tt.lc.{slug}", "title": name.group(1) if name else slug, "summary": "TikTok 面试里被报告过的算法题。"})
        kids.append({"id": "tt.lc", "title": "TikTok 算法题", "summary": "报告过的算法题，共用 LeetCode 牌组的同一份解答。", "children": lc_kids})
        nodes.append({"id": "tt", "order": 2, "core": True, "title": "TikTok 高频设计题",
                      "summary": "TikTok / 字节面经里的设计题，支付方向优先；和题库重复的题共用同一份解答，先修指向它第一次出现的位置。",
                      "children": kids})
    for ti, (track, ttitle) in enumerate(TRACKS, 3):
        tid = "sd" if track == "system-design" else "lld"
        secs = []
        pats = [x for x in patterns if (x["track"] in ("sd", "both")) == (tid == "sd")]
        if pats:  # Chi (2026-11-01): cards that connect questions sharing one mechanism, as the shared core
            secs.append({"id": f"{tid}.cross", "title": "跨题模式（Patterns across questions）",
                         "summary": "多道题共用的机制：在每道题里怎么用、为什么不同、新题该选哪种。",
                         "children": [{"id": f"{tid}.cross.{x['id']}", "title": x["title"],
                                       "summary": x["summary"] + f"（涉及 {len(x['questions'])} 题）"} for x in pats]})
        for si, (sec, stitle) in enumerate(SECTIONS[track], 1):
            leaves = []
            for p in pages:
                key = p["url"].split("/learn/", 1)[1]
                if not (p["track"] == track and (p["section"] == sec or (not p["section"] and p["page"] == sec))):
                    continue
                pid, zh = f"{tid}.{sec}.{p['page']}", ZH.get(key, p["title"])
                # Chi (2026-11-03): every chapter is summary cards, then questions from the page, then questions beyond it
                leaves.append({"id": pid, "title": zh, "summary": f"Hello Interview：{p['title']}。", "children": [
                    {"id": f"{pid}.{part}", "title": f"{label} · {zh}", "summary": why} for part, label, why in PAGE_PARTS]})
            if leaves:
                secs.append({"id": f"{tid}.{sec}", "title": stitle, "summary": f"{ttitle} · {stitle}，按 Hello Interview 的顺序。",
                             "children": leaves})
        nodes.append({"id": tid, "order": ti, "title": ttitle,
                      "summary": f"Hello Interview 的{ttitle}课程，结构与原站一致。", "children": secs})
    sk = {"domain": "hello-interview", "title": "Hello Interview", "deck": "Hello Interview", "lang": "zh", "fold": True, "fold_code": 25,
          "vault": "domains/hello-interview", "study": {"order": "core-first", "mix": "new-first", "new_per_day": 15, "reviews_per_day": 200},
          "nodes": nodes}
    (ROOT / "skeleton/hello-interview.yaml").write_text(
        "# Hello Interview system design + low-level design, mirroring the site's order. Generated by\n"
        "# research/hello-interview/gen_skeleton.py from pages.json; re-run after research/hello-interview/fetch.py.\n"
        + yaml.safe_dump(sk, allow_unicode=True, sort_keys=False, width=200), encoding="utf-8")
    # one reading per page: the card footers and Obsidian link back to the original (never clipped: commercial site)
    rd = ROOT / "vault/domains/hello-interview/readings"
    rd.mkdir(parents=True, exist_ok=True)
    for p in pages:
        key = p["url"].split("/learn/", 1)[1]
        tid = "sd" if p["track"] == "system-design" else "lld"
        leaf = f"{tid}.{p['section'] or p['page']}.{p['page']}"
        nodes_of = ([placed[leaf]] if leaf in placed else []) + [f"{leaf}.{part}" for part, _, _ in PAGE_PARTS]
        tags = ["no-archive"] + (["premium"] if p["premium"] else [])
        (rd / f"hi-{key.replace('/', '-')}.md").write_text(
            f"---\nnodes: [{', '.join(nodes_of)}]\nurl: {p['url']}\ntags: [{', '.join(tags)}]\n---\n# {ZH.get(key, p['title'])}（Hello Interview）\n\n"
            f"原文：{p['title']}。\n", encoding="utf-8")
    page_ids = {f"{'sd' if p['track'] == 'system-design' else 'lld'}.{p['section'] or p['page']}.{p['page']}" for p in pages}
    for rel, course_leaf in home.items():  # move each course card to where its page now lives
        f = cards_dir / rel
        if f.exists():
            text = f.read_text(encoding="utf-8")
            target = placed.get(course_leaf) or (f"{course_leaf}.exam" if course_leaf in page_ids else course_leaf)
            new = re.sub(r"^node: \S+$", f"node: {target}", text, count=1, flags=re.M)
            if new != text:
                f.write_text(new, encoding="utf-8")
    for f in [*cards_dir.glob("qb/*/*.md"), *[x for x in cards_dir.glob("tt/*/*.md") if x.parent.name != "lc"],
              *cards_dir.glob("premium/qb/*/*.md"), *cards_dir.glob("premium/tt/*/*.md")]:  # answer stubs: node under the question, meta
        rel = str(f.relative_to(cards_dir))
        text = f.read_text(encoding="utf-8")
        text = re.sub(r"^node: ((?:qb|tt)\.\w+\.[a-z0-9-]+?)(\.answer)?$", r"node: \1.answer", text, count=1, flags=re.M)
        if rel in card_meta:
            text = re.sub(r"^meta: .*$", "meta: " + json.dumps(card_meta[rel], ensure_ascii=False), text, count=1, flags=re.M)
        f.write_text(text, encoding="utf-8")
    for f in [*cards_dir.glob("points/*/*.md"), *cards_dir.glob("premium/points/*/*.md")]:  # granular cards follow their question
        leaf = points_home.get(f.parent.name)
        if leaf:
            text = f.read_text(encoding="utf-8")
            f.write_text(re.sub(r"^node: \S+$", f"node: {leaf}", text, count=1, flags=re.M), encoding="utf-8")
    print(len(placed), "concept pages placed under questions;", len(points_home), "questions with granular cards")


if __name__ == "__main__":
    main()
