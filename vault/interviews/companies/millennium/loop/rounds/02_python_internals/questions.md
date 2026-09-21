# Python / Java 内功口头题库（40 题）—— R1 编码段穿插 + onsite "Python 基础突袭"

> 来源：一手 —— LeetCode Discuss 7423863（asyncio、multithreading/multiprocessing、pandas、decorators、generators、context managers）· 1p3a 1029420（onsite 突袭 Python 基础）· 1p3a 660546（Java HashMap 冲突）· 1p3a 1124751（异步）· devclub-iitd（favorite data structure）；聚合 —— InterviewQuery（list vs tuple、内存管理、thread-safe singleton）、TechPrep、Glassdoor 摘要。练：`python3 loop/mock.py bq py -n 5 -m 2`。每题答 **≤ 60 s：结论 → 机制 → 一个例子 → 什么时候不用**。
> 速记卡：`../../../study/20-cards/python_internals.md`。

## A · 并发（一手最多）

| # | 题 | 60 s 答案骨架 |
|---|---|---|
| 1 | Explain how `asyncio` works. What is a coroutine? | 单线程事件循环；`async def` 返回 coroutine 对象，`await` 在 I/O 处让出控制权；适合 I/O-bound 高并发；CPU-bound 会卡住 loop（用 `run_in_executor`） |
| 2 | Why did my async HTTP code produce no output?（PracHub 2025-10 原题） | 典型：忘了 `await`（得到 coroutine 未执行）· 没 `asyncio.run()` · `gather` 没被 await · 异常被吞（`return_exceptions=True`）· 事件循环在 Jupyter 里已在跑 |
| 3 | Threads vs processes vs asyncio — when each? | I/O-bound + 阻塞库 → 线程；CPU-bound → 进程（绕 GIL）；I/O-bound + async 库 → asyncio；例：pandas groupby 分块 → `ProcessPoolExecutor` |
| 4 | What is the GIL? | CPython 一次只让一个线程执行字节码；I/O 时释放；C 扩展（NumPy）内部可释放；3.13 有 free-threaded 实验版 |
| 5 | How would you aggregate a CSV with millions of rows by key?（LC 7423863 R3） | 流式 `csv` + dict 累加 O(n)/O(k)；或 `pd.read_csv(chunksize)` 每块 groupby 再合并；CPU 瓶颈 → 多进程 map-reduce；再大 → DuckDB/SQL 引擎 |
| 6 | How do you make a singleton thread-safe? | 模块级实例最简单；类内 `__new__` + `threading.Lock` 双检；或 `functools.lru_cache` 的工厂 |
| 7 | `asyncio.Semaphore` 用来做什么？ | 限并发（例：分页拉取最多 5 个 in-flight）；与 `gather` 组合 |
| 8 | Race condition example in Python and fix | `counter += 1` 非原子；`Lock`；或用队列把状态收敛到一个线程 |
| 9 | `concurrent.futures` 两个 executor 的区别 | Thread vs Process；`map` 保序、`as_completed` 先完成先出；进程池要求可 pickle |
| 10 | What happens if a coroutine raises inside `gather`? | 默认第一个异常传播、其它继续跑；`return_exceptions=True` 收集 |

## B · 语言机制

| # | 题 | 60 s 答案骨架 |
|---|---|---|
| 11 | List vs tuple — when each?（InterviewQuery/Glassdoor） | 可变 vs 不可变；tuple 可哈希（dict key）、更省内存、语义"记录"；list 语义"集合会变" |
| 12 | How does a decorator work? Why `functools.wraps`? | 高阶函数替换名字绑定；`@x` = `f = x(f)`；`wraps` 保留 `__name__`/`__doc__`/签名，否则调试与 pickling 坏 |
| 13 | Parametrized decorator | 三层：`def retry(times): def deco(f): def wrapper(*a, **k)` |
| 14 | Generator vs list; `yield` 的作用 | 惰性、O(1) 内存、可无限；`send/close`；生成器表达式 |
| 15 | Context manager: `__enter__/__exit__` and `contextlib.contextmanager` | 资源保证释放；`__exit__` 收到异常三元组可吞掉；例：计时器、临时目录 |
| 16 | Memory management in a long-running Python process（InterviewQuery） | 引用计数 + 分代 GC 处理环；内存不还给 OS（arena）；泄漏来源：全局缓存、闭包、循环引用 + `__del__`；工具 `tracemalloc`、`objgraph`；分块处理、`__slots__` |
| 17 | `is` vs `==`; small-int caching | 身份 vs 相等；-5..256 缓存；不要用 `is` 比字符串 |
| 18 | Mutable default argument bug | `def f(x, acc=[])` 共享；用 `None` 哨兵 |
| 19 | `__slots__` 什么时候用 | 大量小对象省内存、禁止动态属性 |
| 20 | Shallow vs deep copy | `copy.copy` 一层；嵌套结构要 `deepcopy`；切片是浅拷贝 |
| 21 | `dict` 实现与 `set` | 开放寻址哈希表；3.7+ 保序；平均 O(1)，最坏 O(n)；哈希碰撞 |
| 22 | `sorted` stability & key | Timsort 稳定；多键 tie-break 用 tuple key；`reverse` 不破坏稳定 |
| 23 | Exceptions: EAFP vs LBYL | Python 惯用 try/except；自定义异常继承层次；不要裸 `except:` |
| 24 | Type hints 有什么用 | 静态检查（mypy）、IDE、文档；运行时不强制；`dataclass` + hints |
| 25 | `dataclass` vs `NamedTuple` vs dict | 可变/不可变/无结构；`frozen=True`；`__post_init__` 校验 |

## C · 数据 / pandas / SQL（贴 LEaD JD）

| # | 题 | 60 s 答案骨架 |
|---|---|---|
| 26 | pandas groupby 的内存陷阱 | 整表读入 ×2–3 倍内存；`usecols`、`dtype`、`category`、`chunksize`；或 DuckDB |
| 27 | `merge` 的 how / validate | inner/left/outer；`validate="one_to_one"` 抓重复键；as-of join 用 `merge_asof`（行情对齐） |
| 28 | Vectorize vs `apply` | `apply` 是 Python 循环；用 NumPy 向量化或 `np.where` |
| 29 | Explain a window function（SQL） | `ROW_NUMBER() OVER (PARTITION BY … ORDER BY …)`：每 trader 最新一笔 |
| 30 | `NOT IN` with NULL | 有 NULL 时整个谓词 UNKNOWN → 无行；用 `NOT EXISTS` |
| 31 | Idempotent pipeline — how? | 幂等键 + `MERGE`/upsert；文件级去重；重跑安全（[[S1]] 三层幂等） |
| 32 | Floating point for money? | 不用；整数分 / `Decimal` + 明确舍入（[[S3]] 教训） |

## D · Java（简历列了；一手电面题）

| # | 题 | 60 s 答案骨架 |
|---|---|---|
| 33 | How does `HashMap` handle collisions? Java 8 change?（1p3a 660546 原题） | 桶 + 链表；Java 8 桶内 ≥ 8 且表 ≥ 64 时树化为红黑树 O(log n)；负载因子 0.75 扩容翻倍；`hashCode`/`equals` 契约 |
| 34 | `HashMap` vs `ConcurrentHashMap` vs `Collections.synchronizedMap` | 分段/CAS + 桶锁；迭代弱一致；全表锁 |
| 35 | `ArrayList` vs `LinkedList` | 几乎总用 ArrayList（缓存局部性）；LinkedList 只在迭代器中间插删 |
| 36 | Java memory model: `volatile` vs `synchronized` | 可见性 vs 原子性 + 互斥；happens-before |
| 37 | Spring Boot：`@Transactional` 失效的常见原因 | 自调用绕过代理；非 public；受检异常默认不回滚（实习 Kotlin/Spring 经历） |

## E · 通用口头题

| # | 题 | 60 s 答案骨架 |
|---|---|---|
| 38 | What's your favorite data structure and its trade-offs?（devclub-iitd 原题） | 哈希表：O(1) 均摊，代价是无序、内存、最坏 O(n)、不可范围查询 → 需要有序时用平衡树/跳表；讲一个真实用例（[[S1]] MERGE 键 / pc07 anagram 键） |
| 39 | How do you learn an unfamiliar large system?（Glassdoor 原题；LEaD 轮岗核心） | 从入口与数据流读起（请求怎么进、数据落哪）→ 跑一遍测试与本地环境 → 看最近的 incident/PR → 画一张图给 owner 确认；例：[[S8]] 7 分钟 RCA 靠的是先看 Terraform 状态与日志 |
| 40 | An app crashes in production — walk me through your RCA（Glassdoor 原题） | 止血（回滚/开关）→ 影响面（谁、多少）→ 时间线（变更、告警、日志）→ 假设与验证 → 根因 + 修复 + 防再发；例：[[S3]] / [[S9]] |
