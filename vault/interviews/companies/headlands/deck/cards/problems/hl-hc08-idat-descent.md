---
id: hl-hc08-idat-descent
node: problems.hc08-order-sequence-api
type: qa
step: 6
---
## Q
`idAt(k)`（第 k 张活跃订单）怎么在 Fenwick 的 `cnt` 树上 O(log n) 做二分下降？为什么容量要是 2 的幂？

## A
```java
int pos = 0, rem = k;
for (int pw = capacity; pw > 0; pw >>= 1) {
    int nxt = pos + pw;
    if (nxt <= capacity && cnt[nxt] < rem) { pos = nxt; rem -= cnt[nxt]; }
}
return idByIdx[pos + 1];
```
`cnt` 树里 `tree[pos + 2^j]` 恰是 `(pos, pos + 2^j]` 里的活跃订单数。从大步长到小步长：若这一整块里的活跃数 `< rem`，就整块跳过（`pos = nxt; rem -= cnt[nxt]`），否则第 k 张在块内，不跳。每步确定答案二进制的一位，O(log n)。这就是 Fenwick 树上的 lower_bound。

手算：8 个下标，下标 3 是洞，`cnt = [1,1,0,1,1,1,1,1]`，树 `t1=1,t2=2,t3=0,t4=3,t5=1,t6=2,t7=1,t8=7`，找第 4 张：步长 8：`t8=7 < 4`? 否；步长 4：`t4=3 < 4` 是 → `pos=4, rem=1`；步长 2：`t6=2 < 1`? 否；步长 1：`t5=1 < 1`? 否。结果下标 `pos+1 = 5`。核对：活跃下标 1,2,4,5…，第 4 个是 5 ✓。

**数组大小须是 2 的幂**，步长才能从最高位对齐；容量不是 2 的幂时直接套二分下降会步长对不齐，越界或取错。前置检查 `1 ≤ k ≤ size` 保证答案存在；越界抛 `IndexOutOfBoundsException("index out of range")`。

对应「后缀」或「价格区间」查询：后缀 = 总量 − 前缀；区间 = 两个前缀相减；价格区间要按价格建树（离散化价格）。
