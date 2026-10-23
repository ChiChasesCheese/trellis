---
id: hl-hc07-chaining-vs-open
node: problems.hc07-ticker-hash-map
type: qa
step: 4
---
## Q
链地址法（separate chaining）和开放寻址（open addressing）怎么选？`HashMap<String, Long>` 每个条目背后有多少对象、多少字节？

## A
**链地址法**（Java `HashMap`）：每个桶是链表头，冲突 key 串成链；每条目是 `Node` 对象（hash、key、value、next），**每条目一次堆分配**；装载因子默认 0.75，超过则桶数翻倍并重新分配；Java 8 起链长 ≥ 8（且桶数 ≥ 64）变红黑树，防恶意冲突拖成 O(n)。优点：实现和删除简单、能容忍高装载因子（α=1 平均链长也只有 1）、引用 / 迭代器稳定（C++ `unordered_map`）。

`HashMap<String, Long>` 每条目 **4 个堆对象**，沿指针层层跳：`table[桶]` → `Node` 32 B → key `String` 24 B → `byte[]` 24 B，另有 `Long` value 24 B。`"AAPL"` 的 `String` 共 48 B。预分配桶数组的 `HashMap` 在 200 万条目时每条（不含 key 对象）约 **64.4 B**，加 key 约 110 B，有用信息只有 8 字节 value 和 ≤ 8 字节 key。

**开放寻址**：所有条目放同一个数组，冲突时往后找下一个空格（线性探测，到末尾绕回）。优点：连续内存、缓存友好（往后一格通常在同一条缓存行）、无逐条目分配。代价：装载因子要低、删除要墓碑（或回移）、对哈希质量敏感。

口述：「读多写少、key 小、追求延迟选开放寻址；key 大、写多、删除多或要保证最坏情况，链地址（或树化）更稳。」

C++：短 `std::string`（≤ 15 字符）有 SSO 不分配，所以「装箱」不是主要问题，指针追逐才是；`unordered_map` 每条目一个节点、桶数组存指针、两次间接寻址；`reserve()` 避免 rehash；可换 `absl::flat_hash_map` / `boost::unordered_flat_map`。
