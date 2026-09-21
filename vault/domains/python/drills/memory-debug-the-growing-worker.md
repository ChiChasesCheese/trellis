---
nodes: [memory.leaks-tracemalloc, memory.allocator, memory.cyclic-gc, memory.refcounting, functions.functools]
tags: [drill, interview]
---
# Drill：长驻 worker 的 RSS 每小时涨 200 MB，怎么定位

一个长驻的 Python worker 进程，RSS（常驻内存）以每小时约 200 MB 的速度持续上涨，几天后触发 OOM 被杀。进程里同时存在三种可疑代码：一个没设上限的全局缓存、若干闭包持有对上一次请求对象的引用、以及一批互相引用的对象图。

**限制与要求**
- 先说「怎么定位」的方法论，再讨论「哪种嫌疑最可能」，不许一上来就猜结论。
- 必须说出具体命令/API（不能只说「用剖析工具查一下」）。
- 区分「真泄漏」和「pymalloc 不还内存给操作系统」这两种表面相似但成因不同的现象。
- 每种嫌疑要给出一个「怎么证明是它/怎么排除它」的具体操作。

**分关要求**
- 第 1 关（约 5 分钟）：只用 `tracemalloc`，说出定位分配点的完整流程。
- 第 2 关（约 5 分钟）：三种嫌疑（全局缓存/`lru_cache`、闭包持有大对象、循环引用）各给排除或确认的具体做法。
- 第 3 关（约 3 分钟）：追问——如果 `tracemalloc` 显示内存增长已经停止（分配量不再上升），但 RSS 还是没降，接下来该往哪个方向查？

**评分点（强答案会命中）**
- 在怀疑泄漏的操作前后各拍一次快照，用 `snapshot2.compare_to(snapshot1, 'lineno')` 看两次之间新增了多少内存、多少个内存块，按分配位置排序，而不是只看单次快照的 Top N [[tracemalloc-diff-snapshots-finds-leak]]
- 用 `snapshot.filter_traces(...)` 先把 `<frozen importlib._bootstrap>`、`<unknown>` 这类解释器自身开销过滤掉，避免掩盖业务代码的真实热点；越早启动 `tracemalloc`（如 `-X tracemalloc`）能追踪到的分配越完整，但默认只保留 1 帧调用栈，要看清完整调用链需要显式加大保存帧数（如 `tracemalloc.start(25)`） [[tracemalloc-filter-noise-out]] [[tracemalloc-start-early-and-frame-cost]] [[tracemalloc-traceback-pinpoints-allocation-site]]
- 长驻进程常见泄漏来源：没有上限或过期策略的全局缓存（含 `lru_cache`）、闭包或回调一直持有大对象引用、循环引用配合 `__del__` 只能等循环 GC 触发才释放，以及 C 扩展自己管理、Python 侧看不见的内存 [[leak-sources-cache-closure-cycle-del]]
- `lru_cache` 缓存条目会一直持有参数和返回值的引用直到被淘汰或 `cache_clear()`；`maxsize=None` 时可以无限增长，长期运行的服务会越占越多内存 [[lru-cache-memory-leak-risk]]
- 一个自引用容器（`container.append(container)`）`del` 外部变量后引用计数降不到 0，单靠引用计数无法清理，必须等循环垃圾回收器扫描不可达环 [[refcount-cannot-clear-self-cycle]]
- 循环 GC 用「试减引用」找不可达环：给每个容器对象一份 `gc_ref` 副本，减去内部引用后仍大于 0 的说明来自待扫描集合之外，一定可达；默认分代阈值 `(2000, 10, 10)`（3.13 起，之前 700）决定第 0/1/2 代何时触发 [[gc-trial-subtraction]] [[gc-generations-thresholds]]
- pymalloc 只有一个约 1 MiB 的 arena 里所有 pool 都空闲才会归还给操作系统；长驻进程分配释放交织，很容易出现每个 arena 都零散挂着一两个存活对象的碎片化局面，RSS 不降不代表真的有泄漏 [[pymalloc-arena-not-freed]] [[pymalloc-fragmentation-mitigation]]

**参考答案**
第 1 关：`tracemalloc.start(25)` 尽早启动（保留 25 帧调用栈），在业务处理若干批请求前后各 `tracemalloc.take_snapshot()` 一次；用 `snapshot2.compare_to(snapshot1, 'lineno').filter_traces([...])`（先滤掉 `<frozen importlib._bootstrap>`、`<unknown>`）得到按新增内存量排序的分配位置列表，取 Top 几行去对应源码。

第 2 关：
- 全局缓存/`lru_cache`：检查是否有 `maxsize=None` 或者压根没用 `lru_cache` 装饰、自己手写字典缓存却没有淘汰逻辑；对可疑函数调用 `.cache_info()` 看 `currsize` 是否随时间单调上涨，确认后加 `maxsize` 或换成有 TTL 的缓存。
- 闭包持有大对象：`tracemalloc` 的分配点如果落在「构造闭包/注册回调」那一行，说明是持有问题；用 `gc.get_referrers(obj)` 找出是谁还在引用这个大对象，常见根因是把某次请求的上下文对象存进了长生命周期的回调列表里忘了清理。
- 循环引用：`tracemalloc` 上涨但对应对象理论上该被引用计数立刻释放时，用 `gc.collect()` 前后对比 `gc.get_objects()` 数量，或直接看 `gc.garbage`（旧式终结器）；确认是循环引用后，检查是否可以去掉不必要的双向引用或改用 `weakref`。

第 3 关：这时候不该再往「代码逻辑泄漏」的方向查——`tracemalloc` 显示 Python 侧的分配已经稳定，说明活跃对象数量没有继续增长；接下来应该怀疑是 pymalloc 的 arena 碎片化：`del` 掉的对象释放的内存分散在很多个 arena 里，只要每个 arena 还挂着一两个存活对象就整块不归还操作系统。这种情况通常不是 bug，工程上常用「定期重启 worker」或「避免长期持有大量生命周期参差不齐的小对象」来缓解，而不是继续排查代码逻辑。

**尝试记录**
| 日期 | 用时 | 卡在哪 | 下次 |
|---|---|---|---|
