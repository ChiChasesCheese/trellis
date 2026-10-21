# 20-minute OOD write-ups — instructions for one agent

Chi's Amazon onsite is tomorrow. Chi asked (2026-10-19): for every high-frequency classic OOD problem and every Amazon OOD
problem, an article that combines the **full solution with the answer framework, key points in bold**, textbook-level
but **concise — readable in 20 minutes**, with a **Python skeleton to practise on**; the priority is reading: **after
reading alone Chi should understand 80%** without coding. Sources go **only at the very bottom**.

Repository `/Users/chizhang/Code/trellis`. Folder: `vault/interviews/core/low-level-design/amazon/`. One file per problem:
`oodNN-<slug>.md` (your task lists the ids). Do not run git, do not start agents, touch only your files.
Read `proposals/WRITING_RULES.md` (voice, no provenance in the body, diagrams) — it applies except that a final `## 来源`
section is allowed and required.

## You are condensing, not inventing

Each problem already has a long, tested solution in this repo (paths in your task list): a solution article
(`vault/domains/low-level-design/readings/problems/solution-<slug>.md`), the tested code
(`vault/domains/low-level-design/problems/<slug>/solution.py`), and for Amazon variants the cards
(`vault/domains/low-level-design/cards/amazon/amz-<x>-*.md`). Read them, keep their decisions and their facts, and
compress. Where your article differs from the source design, the source wins unless it is wrong.

## The page — exactly these `##` sections, in order (`python3 scripts/check_ood.py` checks)

`# <中文名>（<English>）` — append `（low priority）` if your task says so.

1. `## 题目` — 3–5 plain sentences: the system, who uses it, **what the interviewer is really testing** (bold). Then the
   prompt as you would hear it, and the 2–3 follow-ups that usually come next.
2. `## 先问这几个问题` — 3–5 bullets: question → **what the answer changes** in the design.
3. `## 核心对象` — a table `类 | 职责（一句话） | 守住的不变量`, then a ```mermaid classDiagram (≤ 8 classes, one member
   per line, only what the text discusses).
4. `## 主流程` — the 1–2 core operations as numbered steps (what calls what, where the lock is, what can fail). A
   sequenceDiagram only if it helps (WRITING_RULES §9 form).
5. `## 关键决策` — 3–4 `###` decisions. Each: the problem in one line → 2 options with their cost → **the choice and why
   (bold)**. At least one is "the simpler answer wins, no pattern".
6. `## Python 骨架` — exactly one ```python block, ≤ 170 lines, standard library only, **runs with `python3 -I` and exits
   0**: the main classes with the key methods fully implemented (the parts the interviewer grades), the rest as short
   bodies, and a `if __name__ == "__main__":` demo with 3–6 `assert`s showing the core flow and one failure path. Chinese
   comments on the non-obvious lines. This is what Chi practises on — keep it typeable in 30 minutes.
7. `## 面试官加需求时` — a table `新需求 | 改哪里 | 不用动哪里`, 4–6 rows: the extensibility proof.
8. `## 并发与扩展` — 3–5 bullets: what races and the lock/structure that prevents it; what changes at scale/persistence.
9. `## 常见错误` — 3–5 bullets, each a concrete mistake and its fix.
10. `## 30 秒复述` — 5–7 bullets Chi can say aloud at the end of the round (objects, the key decision, the extension
    story, the concurrency story).
11. `## 来源` — last section: plain links to the long solution in this repo (wikilink `[[solution-<slug>]]`) and any
    external page used. Nothing else after it.

Length: **3,000–7,500 characters of prose outside code** (≈ 20 minutes with the code). Chinese prose, English terms in
parentheses. Short sentences, bullets over paragraphs, **bold the sentence that carries the decision**.

## Checks before you report

- `python3 scripts/check_ood.py <your ids>` → ok for each.
- Re-read one of your pages as Chi tonight: can it be understood without running the code? Is every bold line a real
  decision? Fix what fails.

Report ≤ 8 lines: the gate lines and anything you could not fit.

## Task list

`src` = the long solution slug (`solution-<src>.md`, `problems/<src>/solution.py`); `cards` = Amazon card prefix to read too.

| id | file | title | low priority | src | cards |
|---|---|---|---|---|---|
| ood00 | ood00-round-framework.md | Amazon OOD 轮怎么打（作答框架） | no | — (method.delivery / method.evaluation map notes) | amz-round |
| ood01 | ood01-file-search.md | Linux find / 文件搜索 API | no | amz-linux-find | amz-linux-find |
| ood02 | ood02-amazon-locker.md | 快递柜（Amazon Locker） | no | amazon-locker | amz-locker-onsite |
| ood03 | ood03-checkout-discount.md | 购物车折扣引擎 | no | amz-discount-engine | amz-discount-engine |
| ood04 | ood04-pizza-order.md | 披萨订单 | no | amz-pizza-order | amz-pizza-order |
| ood05 | ood05-train-fare.md | 火车线路票价 | no | amz-train-fare | amz-train-fare |
| ood06 | ood06-parking-lot.md | 停车场与计费（Parking Lot） | no | parking-lot + amz-parking-fees | amz-parking-fees |
| ood07 | ood07-configurable-cache.md | 可配置缓存（LRU / LFU） | no | amz-configurable-cache + lru-cache | amz-configurable-cache |
| ood08 | ood08-pubsub.md | 发布订阅（Pub/Sub） | no | amz-emergency-pubsub + pub-sub | amz-emergency-pubsub |
| ood09 | ood09-dag-runner.md | DAG 执行器与依赖安装 | no | amz-dag-runner | amz-dag-runner |
| ood10 | ood10-closest-store.md | 增删查最近值 | no | amz-closest-store | amz-closest-store |
| ood11 | ood11-robot-restaurant.md | 机器人餐厅 | no | amz-robot-restaurant + restaurant | amz-robot-restaurant |
| ood12 | ood12-file-watcher.md | 文件监听器 | no | amz-file-watcher | amz-file-watcher |
| ood13 | ood13-in-memory-db.md | 内存数据库 | no | amz-in-memory-db + kv-store | amz-in-memory-db |
| ood14 | ood14-rate-limiter.md | 限流器 | yes | rate-limiter | amz-rate-limiter |
| ood15 | ood15-logger.md | 日志框架 | yes | logger | amz-logger |
| ood16 | ood16-splitwise.md | 分账（Splitwise） | yes | splitwise | amz-splitwise |
| ood17 | ood17-task-scheduler.md | 任务调度器 | yes | task-scheduler | amz-task-scheduler |
| ood18 | ood18-aws-billing.md | AWS 账单服务 | yes | amz-aws-billing | amz-aws-billing |
| ood19 | ood19-occupancy-tracker.md | 办公室人数追踪 | yes | amz-occupancy-tracker | amz-occupancy-tracker |
| ood20 | ood20-wallet.md | 钱包与银行账户 | yes | digital-wallet + bank-account | amz-wallet |
| ood21 | ood21-dns-resolver.md | DNS 解析器与 TTL 缓存 | yes | ttl-cache | amz-dns-resolver |
| ood22 | ood22-music-playlist.md | 音乐播放与播放列表 | yes | music-streaming | amz-playlist-dj |
| ood23 | ood23-video-catalogue.md | 视频目录与续播 | yes | music-streaming (closest), movie-booking | amz-video-catalogue |
| ood24 | ood24-elevator.md | 电梯系统 | yes | elevator | — |
| ood25 | ood25-vending-machine.md | 自动售货机 | yes | vending-machine | — |
| ood26 | ood26-atm.md | ATM 取款机 | yes | atm | — |
| ood27 | ood27-movie-booking.md | 电影订票 | yes | movie-booking | — |
| ood28 | ood28-hotel-booking.md | 酒店预订 | yes | hotel-booking | — |
| ood29 | ood29-library.md | 图书馆管理 | yes | library | — |
| ood30 | ood30-tic-tac-toe.md | 井字棋 | yes | tic-tac-toe | — |
| ood31 | ood31-chess.md | 国际象棋 | yes | chess | — |
| ood32 | ood32-snake-and-ladder.md | 蛇梯棋 | yes | snake-and-ladder | — |
| ood33 | ood33-online-shopping.md | 在线购物 | yes | online-shopping | — |
| ood34 | ood34-ride-sharing.md | 网约车 | yes | ride-sharing | — |
| ood35 | ood35-food-delivery.md | 外卖平台 | yes | food-delivery | — |
| ood36 | ood36-stock-brokerage.md | 股票交易系统 | yes | stock-brokerage | — |
| ood37 | ood37-notification-service.md | 通知服务 | yes | notification-service | — |
| ood38 | ood38-meeting-scheduler.md | 会议室预订 | yes | meeting-scheduler | — |
| ood39 | ood39-text-editor.md | 文本编辑器与撤销重做 | yes | text-editor | — |
| ood40 | ood40-car-rental.md | 租车系统 | yes | car-rental | — |
| ood41 | ood41-coffee-machine.md | 咖啡机 | yes | coffee-machine | — |
| ood42 | ood42-traffic-signal.md | 交通信号灯 | yes | traffic-signal | — |
| ood43 | ood43-kv-store.md | 内存键值存储 | yes | kv-store | — |
| ood44 | ood44-in-memory-file-system.md | 内存文件系统 | yes | in-memory-file-system | — |
| ood45 | ood45-social-network.md | 社交网络 | yes | social-network | — |
| ood46 | ood46-linkedin.md | 职业社交（LinkedIn） | yes | linkedin | — |
| ood47 | ood47-stack-overflow.md | 问答社区（Stack Overflow） | yes | stack-overflow | — |
| ood48 | ood48-chat-room.md | 聊天室 | yes | chat-room | — |
| ood49 | ood49-airline.md | 航班管理 | yes | airline | — |
| ood50 | ood50-cricinfo.md | 体育比分系统 | yes | cricinfo | — |
| ood51 | ood51-deck-of-cards.md | 扑克牌 | yes | deck-of-cards | — |
| ood52 | ood52-online-auction.md | 在线拍卖 | yes | online-auction | — |
| ood53 | ood53-thread-pool.md | 线程池 | yes | thread-pool | — |
| ood54 | ood54-bounded-blocking-queue.md | 有界阻塞队列 | yes | bounded-blocking-queue | — |
| ood55 | ood55-task-management.md | 任务管理（看板） | yes | task-management | — |
