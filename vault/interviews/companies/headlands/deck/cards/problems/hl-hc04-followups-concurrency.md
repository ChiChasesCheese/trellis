---
id: hl-hc04-followups-concurrency
node: problems.hc04-queue-mean-snapshot
type: qa
step: 18
---
## Q
追问：快照要存 O(n) 吗？多个读者怎么保证一致？写者也有多个怎么办？

## A
- **快照怎么存**：先说最笨的 O(n)/版本；再说路径复制（persistent）；最后我的做法——元素放进一棵树，版本只是三个数，push O(1)，pop O(log n)。内存只增不减，要回收需引用计数或只保留最近 K 个版本。
- **多个读者怎么一致**：先问读者要什么一致——`(sum, size)` 一起；再想能否变成一个值：不可变快照 + 一次发布（release/acquire 或 `volatile`）；对比 `synchronized` / `ReentrantReadWriteLock`（读写互斥）、`StampedLock.tryOptimisticRead`（读完校验 stamp，失败重读，适合写少读多）、两个 `volatile`（撕裂）。口述：「状态打成不可变对象，写者原子换引用，读者永远看到完整的某个时刻。」关键词：happens-before、release/acquire、不可变对象的安全发布。
- **写者也多个**：要么串行化（投递到单线程执行器），要么 `AtomicReference<Stat>` + CAS 循环：读当前 Stat，算新 Stat，`compareAndSet`，失败重试。但 FIFO 的 push/pop 有顺序，先问清楚语义。
- **C++ 怎么写**：`std::vector<int64_t>` 或 `std::deque`；总和 `__int128`；发布用 `std::atomic<std::shared_ptr<const Stat>>`（C++20，并非所有标准库都实现），或 `atomic<Stat*>` + hazard pointer / epoch 回收。
