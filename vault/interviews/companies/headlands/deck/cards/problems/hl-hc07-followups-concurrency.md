---
id: hl-hc07-followups-concurrency
node: problems.hc07-ticker-hash-map
type: qa
step: 19
---
## Q
追问：多线程更新同一张 ticker 表怎么办？key 不止 8 个字符怎么办？完美哈希一定更快吗？

## A
- **多线程更新**：每线程一张表（单写者）+ 定期合并（完美哈希下就是逐下标相加）；或分片加锁；或 `LongAdder` / `VarHandle.getAndAdd`（`MethodHandles.arrayElementVarHandle`）原子累加——完美哈希下 value 数组固定、不 resize，**很自然**；热点冲突多时改每线程一张再合并。C++：`std::atomic_ref<long long>`（C++20）对元素原子累加；热点分片、避免 false sharing（把计数器按 64 字节对齐，把不同线程写的数据放不同缓存行）。
- **key 不止 8 个字符 / 含 `.` 和数字（`BRK.B`、期权代码）**：扩字符集（6 比特 × 10 个字母 = 60 比特）、128 位 key（两个 `long`）、或字符串哈希（FNV-1a / xxHash）+ 字节比较；热路径避免 `new String` / `std::string` 构造。
- **完美哈希一定更快吗**：不一定。构造耗时、查询读多个数组；收益是最坏情况确定、内存紧凑、可缓存下标。口述：「完美哈希给的是确定性和紧凑，不是魔法加速；真加速来自缓存下标后直接数组访问。」
- **堆外比堆内快吗**：没有；好处是 GC 不可见、布局可控，代价是手动 `close`、无自动扩容。
- **为什么 resize 要翻倍、容量为什么 2 的幂**：翻倍使总搬运 < 2n 摊还 O(1)；`&` 代替 `%`。
- C++ 对齐：16 字节槽位不会跨缓存行，一次探测只触碰一条缓存行；64 字节对齐 + 4 槽 / 行。短字符串 SSO：`string` 对象本身 24–32 字节，比较先比长度再 `memcmp`。
