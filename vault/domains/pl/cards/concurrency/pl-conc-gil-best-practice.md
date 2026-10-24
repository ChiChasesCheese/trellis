---
id: pl-conc-gil-best-practice
node: concurrency.gil
type: qa
step: 8
---
## Q
有 GIL 的前提下，资深 Python 工程师怎样为 I/O 密集和 CPU 密集任务选并发方案？评估自由线程构建时要看什么？

## A
**按负载选工具**：
1. **I/O 密集**（网络、磁盘）：线程池或 `asyncio` 都行。GIL 在阻塞调用时释放，线程完全有效。任务数很多（上万）选 `asyncio`，任务少且用同步库选 `ThreadPoolExecutor`。
2. **CPU 密集的数值计算**：不要自己写 Python 循环，直接用 NumPy、pandas、PyTorch 等向量化库；它们的内核在 C/Rust 里，释放 GIL，并常自带多线程。
3. **CPU 密集的纯 Python 逻辑**：`ProcessPoolExecutor`/`multiprocessing`，按“大块任务”切分，使序列化和进程开销被摊薄；传数据用共享内存（`multiprocessing.shared_memory`）或让子进程自己读文件，而不是大对象来回传。
4. **混合**：I/O 用 asyncio，CPU 部分用 `loop.run_in_executor` 交给进程池。

**怎么判断热点该不该并行**：先用 `cProfile` 或采样分析器找出时间花在哪里；很多时候换算法或换成向量化的收益比并行大一个数量级。

**评估自由线程构建（3.13t / 3.14t）**：
- 先看依赖：关键的 C 扩展是否声明支持自由线程（否则导入时会重新启用 GIL）。
- 把代码里“恰好靠 GIL 才正确”的地方找出来：共享字典、计数器、先检查后操作，都要显式加锁。
- 在真实负载上测单线程退化和多线程收益，而不是只看微基准。
- 渐进采用：先在测试环境和独立服务上试，不要一步替换全部。

什么时候打破：数据量极小、开销远小于进程启动成本时，单线程顺序执行就是最优方案。
