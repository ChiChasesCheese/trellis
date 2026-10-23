---
id: hl-hc04-jump-pointer
node: problems.hc04-queue-mean-snapshot
type: qa
step: 10
---
## Q
祖先查询（level ancestor）里的 skew-binary 跳跃指针（jump pointer）怎么建、怎么查？比倍增（binary lifting）好在哪？

## A
目标：给节点 `v` 和深度 `d`，求 `v` 在深度 `d` 的祖先（根深度 0）。朴素沿父指针爬 O(深度)。

**建**（新节点 `n`，父 `p`，`j = jump[p]`，Eugene Myers 1983）：
```
如果 depth[p] - depth[j] == depth[j] - depth[jump[j]]
    jump[n] = jump[j]      // 两段跳合并成更长的一段
否则
    jump[n] = p
```
直觉：跳跃长度按 1、1、3、1、1、3、7… 这种「近似 2 的幂减 1」模式增长，长跳数量 log n 级。

**查**：
```java
while (depth[v] > d) v = depth[jump[v]] >= d ? jump[v] : parent[v];
```
能跳（跳完深度仍 ≥ d）就跳，否则走一步父指针。深度 16 → 深度 1 只要 7 步，朴素要 15 步。结果 O(log n)。

**对比倍增**：binary lifting 也行，但需要 `n log n` 的表；jump pointer 每节点只多存一个 `int`，更省内存。

`VersionedQueue` 数据布局：全放原始类型数组（SoA）：节点 `val/parent/jump/depth`，版本 `vTail/vHeadDepth/vHi/vLo`；节点 0 是哨兵根（`parent[0]=jump[0]=0`，深度 0），空队列版本 `EMPTY = 0` 的 tail 就是它；数组满了翻倍。节点只增不减，回收需引用计数或只保留最近 K 个版本。
