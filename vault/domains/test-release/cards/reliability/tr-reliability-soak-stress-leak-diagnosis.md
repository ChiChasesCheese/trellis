---
id: tr-reliability-soak-stress-leak-diagnosis
node: reliability.soak-stress
type: qa
step: 4
---
## Q
长稳测试发现 Python 服务的内存持续上涨。怎样定位是哪里泄漏？如果涨的是加速卡内存呢？

## A
**第一步：确认是哪种内存在涨**。RSS 涨而 Python 对象没涨，可能是 C 扩展、内存碎片或加速卡驱动；Python 对象涨，才是 Python 层的引用没释放。

**Python 层**：
- **tracemalloc 快照对比**：启动时 `tracemalloc.start(25)`（记录 25 层调用栈），运行一段时间后取两次快照对比：

```python
snap1 = tracemalloc.take_snapshot()
# ... 继续运行 30 分钟负载 ...
snap2 = tracemalloc.take_snapshot()
for stat in snap2.compare_to(snap1, "traceback")[:5]:
    print(stat)
    print("\n".join(stat.traceback.format()))
```

增长最多的分配位置通常直接指向泄漏点，例如一个只增不删的字典。
- **memray**：`memray run -o out.bin server.py`，再用 `memray flamegraph out.bin` 生成火焰图，也能看到 C 扩展里的分配。
- **查看运行中的进程**：`py-spy dump --pid <pid>` 看每个线程正在做什么，确认是否有线程卡住并积压任务。

**文件描述符和连接**：`lsof -p <pid>` 列出打开的文件和套接字，按类型统计，看是哪类在增长（例如对同一个后端的 TCP 连接越来越多，说明连接没有复用或没有关闭）。

**加速卡内存**（以 PyTorch 为例）：
- `torch.cuda.memory_allocated()` 是已被张量（多维数组）占用的内存，`torch.cuda.memory_reserved()` 是框架向驱动申请并缓存的内存；
- 前者持续增长 → 有对象一直被引用（例如把每次结果存进了一个列表）；后者涨而前者不涨 → 缓存或碎片问题；
- `torch.cuda.memory_summary()` 打印分配器的详细统计。

**修复后**：用同样的长稳配置重跑，确认斜率回到 0。
