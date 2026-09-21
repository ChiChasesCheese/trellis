# 速记卡 · Python 内功（R1 编码段会被穿插问的 20 张）

> 每张：**一句结论 → 机制 → 一个例子 → 什么时候不用**。对应题库 `loop/rounds/02_python_internals/questions.md`。面试语言英文，卡片中文 + 英文关键词。

1. **GIL**：CPython 一次只跑一个线程的字节码；I/O 等待时释放；NumPy/pandas 的 C 内核可释放。→ CPU-bound 用 `ProcessPoolExecutor`，I/O-bound 用线程或 asyncio。
2. **asyncio**：单线程 event loop；`async def` 造 coroutine 对象，`await` 处让出；`asyncio.run()` 起 loop；`gather` 并发、`Semaphore` 限流、`wait_for` 超时。忘 `await` = 拿到 coroutine 没执行（"missing output" 原题）。
3. **线程 vs 进程 vs async**：I/O + 阻塞库 → 线程；CPU → 进程（要能 pickle）；I/O + async 库 → asyncio。混用：`loop.run_in_executor`。
4. **Race condition**：`x += 1` 三条字节码；`threading.Lock`；更好：无共享状态、队列收敛到一个线程。
5. **装饰器**：`@d` 等价 `f = d(f)`；参数化 = 三层嵌套；`functools.wraps` 保留 `__name__/__doc__/__wrapped__`；类装饰器带状态；叠加顺序自下而上应用、自上而下执行。
6. **生成器**：`yield` 惰性、O(1) 内存、可无限；`next/send/close`；生成器表达式 vs 列表推导；`yield from` 委托。
7. **上下文管理器**：`__enter__/__exit__(exc_type, exc, tb)`，返回 True 吞异常；`@contextlib.contextmanager` 用 `try/finally` 包 `yield`。
8. **list vs tuple**：可变/不可变；tuple 可哈希、更省内存、表示"记录"；list 表示"会变的序列"。
9. **dict/set**：开放寻址哈希表；3.7+ 保插入序；`__hash__` 与 `__eq__` 契约；键必须不可变；平均 O(1)、最坏 O(n)。
10. **内存管理**：引用计数即时释放 + 分代 GC 清环；arena 不还 OS；泄漏：全局缓存、闭包捕获、循环引用 + `__del__`；工具 `tracemalloc`、`gc.get_referrers`；长驻进程：分块处理、定期重启 worker、`__slots__`。
11. **可变默认参数**：`def f(a, acc=[])` 共享同一对象；用 `None` 哨兵。
12. **浅拷贝 vs 深拷贝**：切片/`copy.copy` 一层；嵌套要 `deepcopy`；`a = b` 只是别名。
13. **`is` vs `==`**：身份 vs 值；小整数 [-5, 256] 与短字符串驻留是实现细节，不要依赖。
14. **排序**：Timsort 稳定；多键用 tuple key；`reverse=True` 保持稳定；`key` 比 `cmp_to_key` 快。
15. **异常**：EAFP；自定义异常层次；`except Exception` 不要裸 `except:`；`finally` 总执行；链式 `raise … from e`。
16. **dataclass / NamedTuple / `__slots__`**：可变记录 / 不可变轻量 / 省内存禁动态属性；`frozen=True` 可哈希；`__post_init__` 校验。
17. **金额**：绝不 float 累加；整数分或 `Decimal` + 明确 `ROUND_HALF_UP`；`Decimal(str(x))` 不是 `Decimal(x)`。
18. **pandas 大表**：`read_csv(chunksize, usecols, dtype)`；`category` 省内存；groupby 每块再合并；`merge_asof` 做行情对齐；`validate=` 抓重复键；向量化替代 `apply`。
19. **`concurrent.futures`**：`submit` → Future；`map` 保序；`as_completed` 先完成先出；`max_workers`；异常在 `.result()` 时抛。
20. **Java HashMap（一手电面题）**：桶数组 + 链表；Java 8 桶内 ≥ 8 且表 ≥ 64 → 红黑树；负载因子 0.75 扩容 2×；`hashCode/equals` 契约；线程安全用 `ConcurrentHashMap`（CAS + 桶锁）。
