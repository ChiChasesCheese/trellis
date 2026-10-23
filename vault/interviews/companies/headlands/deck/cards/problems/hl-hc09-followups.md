---
id: hl-hc09-followups
node: problems.hc09-top-trades-by-notional
type: qa
step: 16
---
## Q
追问：窗口很大、ticker 非常多时 `TreeSet` 太慢怎么办？数据放不进内存怎么办？一块失败了其余怎么办？

## A
- **`TreeSet` 常数太大**：先测量。(1) k 很小时只维护「候选集」（top-k 加缓冲区），用堆加惰性删除；(2) ticker 映射成 int，总额用 `long[]` 存，`TreeSet` 里放 `long` 编码（总额高位 + 编号低位）减少对象；(3) 按 ticker 哈希分 S 片，每片一个 `TreeSet`，`top()` 做 S 路 k 路归并。确实是瓶颈再做。C++：懒删除堆均摊 O(log n) 但空间随更新数涨，`set` 精确空间 O(m)，m 很小时直接扫 `unordered_map` 也行。
- **100 亿条放不进内存**：流式分块读取；按 `hash(ticker) % S` 分片写盘（同一 ticker 必在同一片），每片聚合后 top-k，再合并 S 个 top-k（ticker 不跨片，全局 top-k 一定在各片 top-k 的并集里）；Part 1 的堆本来就是流式；也可外部归并（接 K 路合并题）。
- **一块失败了其余怎么办 / 线程会泄漏吗**：`ShutdownOnFailure` 关闭 scope、中断其余；try 块结束前所有子线程一定结束；中断是协作式的，循环要定期检查 `isInterrupted()`。`ExecutorService + Future.get()` 一个失败不取消其他。
- **n 很大 k 很小还能更快吗**：随机顺序下堆满后期望只有 O(k log(n/k)) 个元素进堆，其余一次 `long` 比较被拒，接近 O(n)。
- **`nth_element` 什么时候比堆好**（C++）：数据全在内存、k 很大（接近 n），线性选择不关心 k；堆的优势是流式和 O(k) 空间。
- **窗口 top-k 能更快吗**：懒删除堆 vs `TreeSet`；`jthread` 析构自动 `join`（`std::thread` 在可 join 状态析构 = `terminate`）并内置 `stop_token`。
- 并行为什么不用共享哈希表：热点 ticker 上锁争用、伪共享、扩展性差。
