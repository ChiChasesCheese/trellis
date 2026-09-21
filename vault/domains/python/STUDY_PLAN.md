# Python domain · 七天脱产计划

> 目标：七天后能在对冲基金 SWE 面试里被追问两层仍答得出机制。素材全在这个 domain：466 张卡 / 79 叶 / 11 个 drill / 171 篇 reading。
> 数字来源：`uv run trellis --domain python stats`（2026-09-21）。核心切面（`core: true`）= 38 叶 223 卡，是 45 分钟一轮能问到的范围，**先过核心，再补全量**。

## 每天的固定节奏（约 8 小时）

| 时段 | 做什么 | 工具 |
|---|---|---|
| 上午 1（2h） | 读当天节点的 reading：先官方文档/InternalDocs 那几篇，再看书的「读时提取」 | Obsidian `Python MOC` → 节点 → 叶子 map |
| 上午 2（1.5h） | 新卡：Anki 里当天节点的子牌组，逐张读完再答 | Anki `Trellis · Python::<节点>` |
| 下午 1（1.5h） | 复习：昨天和前天的卡；标 slipped 的卡回到 reading 找机制 | Anki |
| 下午 2（2h） | 当天节点的 drill：限时、先说结论、写代码跑起来；对照评分点，记录到「尝试记录」 | `vault/domains/python/drills/` |
| 晚上（1h） | 用 60 秒口播讲清当天 3 个最难的机制（录音）；写下没答上来的追问 | — |

Anki 节奏：`new_per_day: 70`、`reviews_per_day: 400`（七天冲刺口径；结束后 `scripts/sync_laptop.sh` 前把 skeleton 改回 30/150）。

## 日程

| 天 | 节点（卡数 / 核心卡数） | Drill | 面试追问的第二层 |
|---|---|---|---|
| D1 | model（54 / 30）+ functions（36 / 24） | `model-predict-identity-and-aliasing`、`functions-write-retry-decorator-live` | `is` vs `==`、可变默认参数、`__hash__`/`__eq__` 契约、dict 的紧凑布局与插入序、闭包迟绑定、`wraps` 保元数据 |
| D2 | iteration（41 / 18）+ classes（57 / 32） | `iteration-stream-a-10gb-log`、`classes-design-a-money-value-object` | 生成器帧挂起、`yield from` 双向通道、`with` 的异常传递、描述符决定属性查找顺序、C3 MRO、`__slots__` 代价 |
| D3 | memory（36 / 15）+ runtime（42 / 6） | `memory-debug-the-growing-worker`、`runtime-explain-the-traceback-and-the-import-cycle` | 引用计数 vs 分代 GC、pymalloc 为什么 RSS 不降、`tracemalloc` 两次快照、`sys.modules` 与循环导入、特化解释器与 JIT |
| D4 | concurrency（44 / 33）+ asyncio 前半（event-loop、coroutines-tasks、futures、gather-wait-timeout、cancellation） | `concurrency-pick-the-executor` | GIL 保护的是什么、`x += 1` 为什么不安全、fork 在多线程里的危险、线程/进程/asyncio 选型的代价 |
| D5 | asyncio 后半（sync-primitives、blocking-and-threads、debugging、streams-protocols、contextvars）+ types（23 / 6） | `asyncio-fix-the-silent-async-script`、`types-type-a-decorator-and-a-protocol` | 漏 `await`、Task 里没取的异常、`to_thread` vs 进程池、`Semaphore` 限流、`ContextVar` 跨 await、`Protocol` vs ABC、`ParamSpec` |
| D6 | performance（36 / 18）+ engineering（38 / 6） | `performance-aggregate-50m-rows`、`engineering-harden-a-payment-script` | 分块 + 进程池 vs pandas `chunksize` vs DuckDB、`category` dtype、`Decimal` 量化、aware datetime、`mock.patch` 打在哪、logging 不用 `print` 的理由 |
| D7 | 全量复习 + 模拟 | 重做 D1–D6 里评分点没命中的 drill；Millennium `02_python_internals` bank 走一遍 | 从 Anki 「slipped」卡列出弱叶子：`uv run trellis --domain python stats`，每个弱叶子回 reading 再讲一次 60 秒口播 |

D4/D5 把 asyncio 拆开是因为 concurrency + asyncio 共 103 卡，一天吃不下；asyncio 前半是机制，后半是工程。

## 每天结束前的检查

- [ ] 当天节点的新卡全部见过一遍（Anki 子牌组「New」归零）
- [ ] Drill 的评分点逐条打勾；没命中的写进「尝试记录」的「下次」
- [ ] 三个 60 秒口播录音存在，能不看卡讲出机制（不是定义）
- [ ] 追问没答上来的问题写进 `BUILD.md` §3 的表（有对应叶子就写叶子，没有就是 skeleton 缺口）

## 七天后

- `scripts/sync_laptop.sh` 一次；skeleton 的 `study:` 改回 `new_per_day: 30 / reviews_per_day: 150`
- 每周：`trellis pull` → `trellis brief` → `trellis grow --next`，只给有 slipped 判定的弱叶子加卡（ADR 0009）
- Millennium 之外的公司：这个 domain 是通用的，公司 kit 只加该公司真问过的题
