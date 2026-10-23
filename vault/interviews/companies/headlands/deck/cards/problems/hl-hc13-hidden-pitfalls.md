---
id: hl-hc13-hidden-pitfalls
node: problems.hc13-fixed-memory-pool
type: qa
step: 15
---
## Q
定长内存池题的常见误区和隐藏测试会打的坑有哪些？

## A
1. 打包 handle 忘了 `& 0xFFFFFFFFL`：`((long) generation << 32) | index` 在 `index` 为负时高 32 位全 1 把 generation 冲成 `0xFFFFFFFF`；
2. 重复归还只「忽略」不检查：`void free(int b) { next[b] = head; head = b; }` 连续 `free(3)` 两次得 `next[3] = 3`，之后 `allocate` 永远返回 3；
3. 以为 `volatile` 能修好 ABA：只解决可见性，要 tag；
4. `free` 先检查再修改没有原子化：`if (gens[i] == g) { gens[i] = g + 1; push(i); }` 两步之间可被插入，并发下两个线程都通过 if；要 `CAS(gens[i], g, g+1)`；
5. 复用槽位忘了清零：上一个主人的 `px`、`qty` 泄漏；
6. 池要多线程用却用 `Arena.ofConfined()`：别的线程 `WrongThreadException`，应 `ofShared()`；
7. 把 `available()` 当并发中的精确值：`inUse` 和 `head` 的更新不是同一个原子操作，要当近似值，静止后才断言精确；
8. 只测 50/50 随机借还，漏掉 O(n) 扫描；
9. `close()` 重复调用抛异常；`put(h, null)` 应抛 NPE；陈旧 handle 的 `get` 读到新主人的数据；
10. `FreeResult` 用 `int` 常量而非 enum；`free` 不检查状态（同一块进链表两次）。

C++ 额外陷阱：
- 默认移动构造：被移动的池带着旧的 `head_`，下一次 `allocate` 读 `next_[head_]` 越界，要手写移动让被移动的池是合法的空池；
- `std::aligned_alloc(64, 96)` 的 size 不是 alignment 整数倍，行为不合规，要向上取整到 128；
- 只 `malloc` 不构造对象就读写：对象生命周期没开始，用 placement new；
- `Slot` 要 `static_assert(std::is_trivially_destructible_v<Slot>)`：arena 用 `std::free` 释放，不会逐个调析构；
- 有符号 `int` 直接和 `size_t` 比较；`int` 版本号回绕是 UB；
- `compare_exchange_weak` 没放进循环；tag 和 head 拆成两个原子变量。
