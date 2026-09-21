# Drill 子代理指令 · `python` domain（skill 第 7 步：产出式练习）

> 你是 `sonnet` 子代理，不得再派生代理。你只拥有 `vault/domains/python/drills/` 下分配给你的文件。
> Drill 的目的是让学习者**产出机制**而不是回忆：预测行为（"这段代码打印什么、为什么"）、调试症状（"这个进程 RSS 一直涨，怎么定位"）、向同事解释设计（"为什么这里用进程池不用线程池"）。每个顶层节点至少一个 drill；评分点用 wikilink 指向已存在的卡片 id（`grep -h "^id:" vault/domains/python/cards/<node>/*.md`）。

## 文件格式（与 readings 相同的 frontmatter；照 `vault/domains/system-design/drills/design-payment-ledger.md` 的体例）

```markdown
---
nodes: [concurrency.gil, concurrency.choosing, concurrency.executors]
tags: [drill, interview]
---
# Drill：<一句话题目>

<题面：给一段代码或一个症状或一个设计要求。中文，术语英文。>

**限制与要求**
- <3–5 条：不许查资料、限时、必须先说结论再说机制、给出替代方案的代价>

**分关要求**（像真实面试的追问，一关做完再看下一关）
- 第 1 关（约 N 分钟）：…
- 第 2 关：…
- 第 3 关：…

**评分点（强答案会命中）**
- <每条一句 + 对应卡片 wikilink，如 [[gil-releases-on-io]]；只链接真实存在的卡片 id>

**参考答案**
<按关给出要点；代码片段 ≤ 30 行；数字有来源（卡片或文档）>

**尝试记录**
| 日期 | 用时 | 卡在哪 | 下次 |
|---|---|---|---|
```

## 每个顶层节点的 drill 题目（起点，可微调；文件名 = `<node>-<slug>.md`）

| 节点 | Drill |
|---|---|
| model | `predict-identity-and-aliasing`：六段小代码（`is` vs `==`、可变默认参数、`+=` 在 tuple 里的 list、浅拷贝、`__eq__` 无 `__hash__` 做键、dict 插入序）逐段预测输出并解释机制 |
| functions | `write-retry-decorator-live`：现场写 `@retry(times, exceptions, backoff)`，保留元数据、可注入 sleep、装饰方法时 `self` 正确；追问：叠加 `@lru_cache` 的顺序、闭包迟绑定 |
| iteration | `stream-a-10gb-log`：用生成器管道统计 10 GB 日志的每小时错误数，内存 O(1)；追问：`groupby` 需要排序吗、`tee` 的代价、上下文管理器保证文件关闭、生成器只能消费一次 |
| classes | `design-a-money-value-object`：写一个不可变 `Money` 类（`__eq__`/`__hash__`、`__add__`/`__radd__`、`__repr__`、dataclass frozen 与 `__slots__`），再用描述符给字段加校验；追问 MRO 与 `super()` |
| memory | `debug-the-growing-worker`：一个长驻 worker 的 RSS 每小时涨 200 MB；用 `tracemalloc` 两次快照比对定位、判断是泄漏还是 arena 不归还、`lru_cache`/闭包/循环引用三种嫌疑各怎么排除 |
| concurrency | `pick-the-executor`：三个任务（拉 500 个 URL、解析 5 GB CSV 做聚合、调用一个释放 GIL 的 NumPy 内核）各选线程/进程/asyncio 并说代价；追问 `x += 1` 为什么不安全、fork 在多线程里的危险 |
| asyncio | `fix-the-silent-async-script`：一段拉分页 API 的 asyncio 代码没有输出——找出漏 `await`、未 await 的 `gather`、异常留在 Task 里三个 bug，再加 `Semaphore` 限流与 `wait_for` 超时；追问取消语义 |
| runtime | `explain-the-traceback-and-the-import-cycle`：给一个循环导入报错与一个链式异常 traceback，解释 `sys.modules` 与 `__context__`/`__cause__`；再用 `dis` 解释为什么 `x in set` 比 `x in list` 快 |
| types | `type-a-decorator-and-a-protocol`：给 `retry` 装饰器加 `ParamSpec` 签名，给一个鸭子类型参数写 `Protocol`；追问 `Any` 的传染、`TYPE_CHECKING` 打破循环导入 |
| performance | `aggregate-50m-rows`：50M 行 CSV 按 key 求和：纯 Python 流式 → 分块 + 进程池 → pandas `chunksize`/`dtype` → DuckDB；每档说时间与内存量级、什么时候该换引擎 |
| engineering | `harden-a-payment-script`：一段用 float 算金额、裸 `except:`、`print` 日志、无测试的脚本，改成 `Decimal` + 异常层次 + `logging` + 注入时钟的 pytest |

## 硬规则
- 中文；不写过程话；参考答案里的每个数字要能在卡片或官方文档里找到，否则只写量级。
- wikilink 只指向真实卡片 id；写完跑 `uv run trellis --domain python validate`，最后一行 0 errors。
- 最终回复：文件列表、每个 drill 的评分点数、validate 最后一行。
