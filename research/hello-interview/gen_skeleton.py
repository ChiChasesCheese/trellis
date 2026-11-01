"""Write skeleton/hello-interview.yaml from research/hello-interview/pages.json, mirroring Hello Interview's own order.

    uv run python research/hello-interview/gen_skeleton.py

Two sub-decks, System Design and Low-Level Design, each with Hello Interview's sections in its order and one leaf per
page. Premium pages are leaves too (summary says 会员内容，待解锁) so the structure is complete; they get cards once Chi
gives access. After the material is learned, these leaves are meant to merge into the system-design and
low-level-design domains (research/hello-interview/BUILD.md).
"""
from __future__ import annotations

import json
import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
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
        if rel.startswith("qb/") or rel in home:
            continue
        m = re.search(r"^node: (\S+)$", f.read_text(encoding="utf-8"), re.M)
        if m:
            home[rel] = m.group(1)
    home_path.write_text(json.dumps(home, ensure_ascii=False, indent=1, sort_keys=True), encoding="utf-8")
    placed: dict[str, str] = {}      # course leaf -> prerequisite leaf under a question
    if qb_path.exists():
        extra = {}
        for f in sorted((ROOT / "research/hello-interview").glob("qb_meta_*.json")):  # zh titles + requires from the card agents
            extra.update(json.loads(f.read_text(encoding="utf-8")))
        qb = json.loads(qb_path.read_text(encoding="utf-8"))
        kids = []
        for track, title in (("sd", "系统设计高频题"), ("lld", "低层设计高频题")):
            leaves = []
            for q in [q for q in qb if q["track"] == track]:
                e = extra.get(q["slug"], {})
                qid = f"qb.{track}.{q['slug']}"
                pre = []
                for c in e.get("requires", []):
                    if c in placed or c not in {v for v in home.values()}:
                        continue  # already a prerequisite of a more frequent question, or a page without cards
                    placed[c] = f"{qid}.pre-{c.replace('.', '-')}"
                    key = next((pk for pk in ZH if pk.endswith("/" + c.split(".")[-1]) and pk.startswith(
                        "system-design" if c.startswith("sd.") else "low-level-design")), "")
                    pre.append({"id": placed[c], "title": "先修 · " + ZH.get(key, c.split(".")[-1]),
                                "summary": f"{e.get('title') or q['title']} 用到的概念。"})
                answer = {"id": f"{qid}.answer", "title": "解答 · " + (e.get("title") or q["title"]),
                          "summary": f"被报告 {q['reports']} 次；{q['title']}。"}
                later = [placed[c] for c in e.get("requires", []) if c in placed and not placed[c].startswith(qid + ".")]
                if later:
                    answer["requires"] = later  # prerequisites that sit under an earlier question
                leaves.append({"id": qid, "title": e.get("title") or q["title"],
                               "summary": f"被报告 {q['reports']} 次。", "children": pre + [answer]})
            kids.append({"id": f"qb.{track}", "title": title, "summary": f"{title}：按被报告次数从高到低。", "children": leaves})
        nodes.append({"id": "qb", "order": 1, "core": True, "title": "高频真题（Question Bank）",
                      "summary": "Hello Interview 题库里被报告最多的设计题，每题一张完整解答；课程部分是它们的先修。", "children": kids})
    for ti, (track, ttitle) in enumerate(TRACKS, 2):
        tid = "sd" if track == "system-design" else "lld"
        secs = []
        for si, (sec, stitle) in enumerate(SECTIONS[track], 1):
            leaves = []
            for p in pages:
                key = p["url"].split("/learn/", 1)[1]
                in_sec = p["track"] == track and (p["section"] == sec or (not p["section"] and p["page"] == sec))
                if not in_sec or f"{tid}.{p['section'] or p['page']}.{p['page']}" in placed:
                    continue
                leaves.append({"id": f"{tid}.{sec}.{p['page']}", "title": ZH.get(key, p["title"]),
                               "summary": ("会员内容，待解锁。" if p["premium"] else "") + f"Hello Interview：{p['title']}。"})
            if leaves:
                secs.append({"id": f"{tid}.{sec}", "title": stitle, "summary": f"{ttitle} · {stitle}，按 Hello Interview 的顺序。",
                             "children": leaves})
        nodes.append({"id": tid, "order": ti, "title": ttitle,
                      "summary": f"Hello Interview 的{ttitle}课程，结构与原站一致。", "children": secs})
    sk = {"domain": "hello-interview", "title": "Hello Interview", "deck": "Hello Interview", "lang": "zh",
          "vault": "domains/hello-interview", "study": {"order": "core-first", "mix": "new-first", "new_per_day": 15, "reviews_per_day": 200},
          "nodes": nodes}
    (ROOT / "skeleton/hello-interview.yaml").write_text(
        "# Hello Interview system design + low-level design, mirroring the site's order. Generated by\n"
        "# research/hello-interview/gen_skeleton.py from pages.json; re-run after research/hello-interview/fetch.py.\n"
        + yaml.safe_dump(sk, allow_unicode=True, sort_keys=False, width=200), encoding="utf-8")
    # one reading per page: the card footers and Obsidian link back to the original (never clipped: commercial site)
    rd = ROOT / "vault/domains/hello-interview/readings"
    rd.mkdir(parents=True, exist_ok=True)
    locked = []
    for p in pages:
        key = p["url"].split("/learn/", 1)[1]
        tid = "sd" if p["track"] == "system-design" else "lld"
        leaf = f"{tid}.{p['section'] or p['page']}.{p['page']}"
        leaf = placed.get(leaf, leaf)
        tags = ["no-archive"] + (["premium"] if p["premium"] else [])
        (rd / f"hi-{key.replace('/', '-')}.md").write_text(
            f"---\nnodes: [{leaf}]\nurl: {p['url']}\ntags: [{', '.join(tags)}]\n---\n# {ZH.get(key, p['title'])}（Hello Interview）\n\n"
            f"原文：{p['title']}。" + ("会员内容，解锁后补卡。" if p["premium"] else "") + "\n", encoding="utf-8")
        if p["premium"]:
            locked.append(f"| {ZH.get(key, p['title'])} | {p['title']} | {p['url']} |")
    (ROOT / "vault/domains/hello-interview/locked").mkdir(parents=True, exist_ok=True)
    (ROOT / "vault/domains/hello-interview/locked/README.md").write_text(
        "# 待解锁的会员内容\n\nHello Interview 的这些页面需要会员才能看全。结构已经在牌组里占好位置，"
        "拿到权限后重新抓取，就能给它们补卡。\n\n| 页面 | 原标题 | 链接 |\n|---|---|---|\n" + "\n".join(locked) + "\n",
        encoding="utf-8")
    for rel, course_leaf in home.items():  # move each course card to where its page now lives
        f = cards_dir / rel
        if f.exists():
            text = f.read_text(encoding="utf-8")
            new = re.sub(r"^node: \S+$", f"node: {placed.get(course_leaf, course_leaf)}", text, count=1, flags=re.M)
            if new != text:
                f.write_text(new, encoding="utf-8")
    for f in cards_dir.glob("qb/*/*.md"):  # the answer stubs hang under their question
        text = f.read_text(encoding="utf-8")
        f.write_text(re.sub(r"^node: (qb\.\w+\.[a-z0-9-]+?)(\.answer)?$", r"node: \1.answer", text, count=1, flags=re.M),
                     encoding="utf-8")
    print(len(placed), "concept pages placed under questions;", len(locked), "locked")


if __name__ == "__main__":
    main()
