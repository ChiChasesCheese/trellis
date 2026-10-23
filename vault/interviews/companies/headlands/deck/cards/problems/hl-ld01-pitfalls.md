---
id: hl-ld01-pitfalls
node: problems.ld01-spsc-channel
type: qa
step: 13
---
## Q
SPSC 通道题的常见误区和隐藏测试的边界清单是什么？

## A
**误区**：
1. 以为 x86 上跑通就代表内存序对：x86 不重排 Store-Store，普通写常「碰巧」正确，ARM（Apple M、很多云服务器）上就错，按 release/acquire 写并在弱内存序机器上测；
2. `head == tail` 就是空：下标取模存储时也可能是满；用自由增长计数 + 差值；用 `%` 而不是掩码；容量不是 2 的幂不报错；
3. 把 PAD + 记录当整体判断能不能放进去：空环上死锁；
4. 先读 `tail` 再读 `closed`：漏最后几条；
5. 子进程只传 `java.class.path`；用 `Thread.sleep` 对时序；一端出错另一端空转永不退出；
6. 在堆上的 `byte[]` segment 上做原子访问：`Misaligned access`；
7. 继承链填充却把只读字段放在热字段后面：`buf/mask` 与 `head` 同行；
8. `create` 非法容量时先截断了已有文件。

**边界清单**：
- 容量 `0`、负数、非 2 的幂、`2³⁰ + 1`、`Integer.MIN_VALUE`；`MessageRing` 另有 `< 16`；容量 1 的 `LongRing`；
- 满了 `offer` 不覆盖；空了 `poll` 抛 / 返回 `null`；满 → 腾一个 → 回绕写入；
- `Long.MIN_VALUE`、`-1`、`0`、`Long.MAX_VALUE` 都是合法消息；百万次之后计数仍正确；`size()` 不为负、不超过容量；
- 消息：空消息、len=4、len=5、`len = maxPayload()`、`maxPayload()+1`（IAE）、含 `0xFF` / `0` 的二进制；
- 回绕：到末尾剩 8 字节；剩的不够放当前记录；PAD 已发布但真记录没挤进去；空环 + 最大消息 + tail 在任意位置；
- drained：空但没 finish ≠ drained；有消息没读完 ≠ drained；末尾残留 PAD 要越过才 drained；finish 后 offer 抛异常；
- 内存序：消费者不能读到上一轮的旧值；tail 不能先于数据可见；
- 性能：单线程 1000 万次 `offer+poll` < 2 s；两线程 1000 万条 `long` < 2 s；200 万条变长消息 < 2–3 s。

C++ 变体追问：`std::atomic<uint64_t>` + `memory_order_release/acquire`。
