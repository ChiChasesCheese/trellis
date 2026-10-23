---
id: hl-cq-cs19-concurrency
node: cpp-questions.cheatsheet
type: qa
step: 19
---
## Q
一句话背诵：C++ 并发的要点——条件变量、多锁、release/acquire、`relaxed`、`volatile`、伪共享的数字。

## A
- `cv.wait(lk, pred)` 必须带谓词（虚假唤醒）；多锁用 `scoped_lock`。
- release / acquire 发布数据；`relaxed` 只给计数器。
- **`volatile` 不是原子**：4 线程 × 50 万次丢更新，得到 1,995,942 而不是 2,000,000；数据竞争是 UB。
- 伪共享：相邻计数器 **404 ms**，隔 64 字节 **30 ms**。
