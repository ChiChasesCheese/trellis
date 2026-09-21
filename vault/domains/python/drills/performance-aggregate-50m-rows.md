---
nodes: [performance.profiling, performance.pandas-at-scale, performance.numpy-vectorization, performance.compiling, performance.containers]
tags: [drill, interview]
---
# Drill：5000 万行 CSV 按 key 求和，四档实现逐级升级

一份 5000 万行的 CSV，每行 `key,value`，要按 `key` 求 `value` 的总和。机器内存有限，装不下整份 DataFrame 的宽类型版本。依次给出四档实现，每档说清楚：大致的时间/内存量级、相对上一档的改进点、什么信号说明该往下一档换。

**限制与要求**
- 四档必须依次说：纯 Python 流式 → 分块 + 进程池 → pandas `chunksize`/`dtype` → DuckDB；不许跳档。
- 每档给出的时间/内存量级必须有出处（卡片或官方文档），说不出出处只能说「量级上更快/更省」，不许编具体数字。
- 每档要说明「什么信号出现时该换下一档」，不能只说「这个更快所以直接用」。
- 15 分钟内说完四档。

**分关要求**
- 第 1 关：纯 Python 流式实现，说内存复杂度。
- 第 2 关：分块 + 进程池，说为什么能加速、代价是什么。
- 第 3 关：pandas `chunksize`/`dtype`/`category`，说峰值内存为什么更低。
- 第 4 关：DuckDB，说什么信号说明该换引擎；追问——先测量用什么工具，为什么不能只凭感觉判断哪一档更快。

**评分点（强答案会命中）**
- 先测量再优化：`cProfile` 这类确定性剖析器计时精度受系统时钟滴答限制，典型量级在毫秒级，调用次数极多的小函数用它测会累积误差，应改用 `timeit` 做批量微基准；`py-spy` 这类采样剖析器不用插桩、开销低到可以直接挂生产进程，但只能给相对热点分布 [[profiling-cprofile-clock-tick-limit]] [[profiling-deterministic-vs-sampling]]
- 纯 Python 流式版本用 `dict` 而不是 `list` 做 key 到累计值的映射，`x in set/dict` 平均 O(1)，`x in list` 是 O(n) 线性扫描，选错容器会让整个聚合退化成 O(n²) [[containers-in-list-vs-set]]
- `pd.read_csv(chunksize=N)` 返回分块读取器，典型用法是每块先做局部聚合、再合并各块结果，是单机版 map-reduce，内存占用只跟 `chunksize` 和最终聚合结果的大小有关，与总行数无关 [[pandas-chunking-map-reduce]]
- `dtype=`/`usecols=` 要在 `read_csv` 阶段就指定，而不是读完整表再 `astype`/删列：默认按启发式猜类型会把数值列猜成 8 字节的 `int64`/`float64`，读完整表再缩小类型也救不回已经出现过的内存峰值 [[pandas-dtype-usecols-at-read-time]]
- 取值范围小的字符串 key 转成 `category` dtype 是字典编码，只存一份唯一值列表，每行存一个小整数编码而不是各自一份 Python 字符串对象，`groupby` 按这列分组时比较的是小整数，比逐字符比较字符串更省内存也更快 [[pandas-category-dtype-groupby]]
- 可向量化的数值计算，NumPy 向量化相对等价的纯 Python `for` 循环通常快一到两个数量级，差距主要来自省掉了 Python 解释器逐元素调度的固定开销 [[numpy-vectorization-order-of-magnitude]]
- 数据本身装不进内存（DuckDB 可以直接对磁盘上的 Parquet/CSV 做核外查询）、需要多核并行、或者工作负载主要是可下推优化的过滤/分组聚合时，该考虑换 DuckDB/Polars 而不是继续在 pandas 里调优 [[pandas-when-to-move-to-polars-duckdb]]
- 把过滤、分组、join 这类关系代数操作交给 DuckDB 的 SQL 去做，往往比自己手写 Python 循环调优更划算，因为查询引擎已经把向量化执行、多线程、基于统计信息的优化器实现得很成熟 [[compiling-push-down-to-duckdb-sql]]

**参考答案**
第 1 关：纯 Python 流式——逐行读文件，用一个 `dict[key] = 累计value`，读完即得结果。内存只跟「不同 key 的数量」成正比，跟总行数无关（额外的行内解析变量是 O(1)）；如果 key 不去重直接放 `list` 查找会退化成 O(n²)，必须用 dict/hash 结构。这一档量级上是最慢的，因为每一行都要经过 Python 解释器逐条字节码处理，没有任何向量化或批处理。

第 2 关：分块 + 进程池——把文件按字节偏移或行数切成若干块，每个进程各自跑第 1 关的流式聚合得到局部 `dict`，主进程把所有局部结果 merge 成最终结果。相对第 1 关的改进是利用了多核（纯 Python 计算不释放 GIL，多线程做不到这一点，只有多进程能真并行）；代价是每个子进程的局部聚合结果要能 pickle 传回主进程（好在通常只是一个不大的字典，代价可控），以及切块要注意不能把同一行切断。

第 3 关：pandas `chunksize`/`dtype`——用 `pd.read_csv(path, chunksize=N, dtype={"key": "category", "value": "float32"}, usecols=["key", "value"])`，每个 chunk 内部 `groupby("key")["value"].sum()` 做局部聚合，多个 chunk 的局部结果再 `concat` 后整体 `groupby` 一次得到最终结果。峰值内存更低的原因有两层：`chunksize` 让任意时刻只有一块数据在内存里，跟第 2 关的分块思路一致；`dtype`/`usecols` 在读取阶段就避免了「先猜宽类型、读完整列再缩小」这个会先吃满一次峰值的过程，`category` 类型进一步把重复字符串压成小整数编码。

第 4 关：如果 5000 万行还在增长、或者机器内存连一个 chunk 都装不下、或者除了这一个聚合还有多个查询要跑在同一份数据上，就是该换 DuckDB 的信号——`duckdb.sql("SELECT key, SUM(value) FROM read_csv('data.csv') GROUP BY key")` 可以直接对磁盘文件做核外查询，不需要先手工分块，聚合本身也是向量化执行，通常比继续手工调优 pandas 分块更省事也更快。判断该不该换档不能凭感觉：应该先用 `timeit`（对可重复的小操作）或 `py-spy`/`cProfile`（对整个流程）实际测出当前实现的耗时和瓶颈在哪一步，再决定往下一档投入时间是否划算。

**尝试记录**
| 日期 | 用时 | 卡在哪 | 下次 |
|---|---|---|---|
