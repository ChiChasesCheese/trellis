# 速记卡 · Python 运行时与数据处理（PracHub 报告过的 3 道概念题）

> 来源：`../../catalog/raw/ai_round_sweep_2026-10-07.md` S-7（PracHub 题库 `question-reported-*`，无日期，[中]）。每题：结论 · 机制 · 怎么查 · 怎么改 · 追问。

## 1. GIL 对多线程数据摄入的影响，怎么绕开

- **结论**：CPython 的 GIL 让同一时刻只有一个线程执行 Python 字节码。I/O 密集（网络、磁盘、等待 API）的摄入用线程依然有效，因为阻塞 I/O 时会释放 GIL；CPU 密集（解析 JSON、正则、哈希、转换）用多线程几乎没有加速，还会多出切换开销。
- **怎么判断**：先测再改。`py-spy top --pid <pid>` 看时间花在哪；CPU 利用率卡在约一个核 = 被 GIL 限住。
- **怎么绕开**（按代价从低到高）：
  1. I/O 部分：线程池或 `asyncio`（大量并发连接时 `asyncio` 更省）。
  2. CPU 部分：`multiprocessing` / `ProcessPoolExecutor`，按批次分发，避免逐条 pickle 的开销。
  3. 会释放 GIL 的原生库：`orjson` / `simdjson` 解析、NumPy / pandas / pyarrow 的向量化操作。
  4. 架构上横向扩：多个 worker 进程消费同一个队列（Kafka 分区、SQS）。
  5. Python 3.13+ 的 free-threaded 构建（`python3.13t`）：还算实验性，生产里先说出风险。
- **追问**："为什么不全用多进程？" → 进程间要序列化、内存翻倍、启动慢；I/O 部分线程更便宜。"线程安全还要管吗？" → 要。GIL 只保证单条字节码是原子的，`counter += 1` 这类读-改-写依然会丢更新。

## 2. 大规模 JSON 解析时的内存泄漏，怎么排查

- **先分清**：真泄漏（引用一直被持有、内存只涨不降）、还是峰值过高（一次性 `json.load` 一个 2 GB 文件）、还是碎片（RSS 不回落，但对象数量是稳定的）。
- **怎么查**：
  1. 先建反馈回路（T8）：用一个固定大小的输入文件循环处理 N 次，记录每轮的 RSS（`psutil` / `resource.getrusage`），确认它是单调上涨的。
  2. `tracemalloc`：在第 1 轮和第 N 轮各取快照，`snapshot.compare_to(prev, "lineno")` 的前几行就是一直在增长的分配点。
  3. `gc.get_objects()` 按类型计数，或用 `objgraph.show_growth()`；再用 `objgraph.show_backrefs` 找是谁在持有引用。
  4. 常见元凶：模块级缓存或 dict 只增不删（`lru_cache` 没设上限、memo 字典）、日志或异常对象挂着大 payload、闭包和回调保留了引用、循环引用里有 `__del__`、C 扩展本身泄漏。
- **怎么改**：
  - 峰值问题：流式解析，用 `ijson` 按元素迭代，或改成 JSON Lines 逐行处理；分批写出，不把整个结果攒在内存里。
  - 真泄漏：删掉持有引用的那一处（缓存设上限或用 `weakref`），然后加回归检查：处理 N 轮后 RSS 增长要低于阈值。
  - 兜底：worker 处理固定数量的任务后自动重启（`maxtasksperchild`），并说清楚这只是缓解，不是修复。
- **追问**："RSS 不降是不是泄漏？" → 不一定。CPython 的内存分配器会把内存留在进程里复用；要看对象数量和 `tracemalloc` 是否持续增长。

## 3. 用 Spark 分析历史通信模式，怎么定位并解决数据倾斜

- **作业结构**：读分区好的事件表（Parquet，按日期分区）→ 只投影需要的列、尽早过滤 → 按 `(tenant, sender, recipient)` 聚合出通信边（次数、首次 / 最近时间）→ join 用户和组织维表 → 写出按租户、日期分区的结果。
- **怎么发现倾斜**：Spark UI 里同一个 stage 的 task 时长分布极不均（max 远大于 median）、个别 task 的 shuffle read 特别大、spill 到磁盘，作业卡在最后几个 task。用 `groupBy(key).count().orderBy(desc)` 找出热点键，通常是群发地址、系统邮箱、超大租户。
- **怎么解决**：
  1. 先开 AQE（`spark.sql.adaptive.enabled` + `skewJoin.enabled`），让 Spark 自动拆分倾斜的分区。
  2. 小表 join 用 broadcast join，大表就不用 shuffle。
  3. 热点键加盐（salting）：在键后面拼一个随机后缀 0..N 先做局部聚合，再去掉后缀做二次聚合；join 时小表侧把每个键复制 N 份。
  4. 把热点键单独拿出来走一条路径，最后再 union 回去。
  5. 能用 `reduceByKey` / 在 map 端先聚合的，就不要用 `groupByKey` 把整组数据搬过 shuffle。
- **追问**："怎么验证修好了？" → 看同一个 stage 的 task 时长分布、shuffle read 的最大值和中位数之比、总耗时，前后对比。"增量怎么做？" → 按日期分区只处理新分区，聚合结果和历史结果合并；迟到的数据用水位线（watermark）或者回补窗口处理。
