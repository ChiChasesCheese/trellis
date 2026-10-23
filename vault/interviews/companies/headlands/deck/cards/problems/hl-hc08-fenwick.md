---
id: hl-hc08-fenwick
node: problems.hc08-order-sequence-api
type: qa
step: 4
---
## Q
树状数组（Fenwick tree）的 `tree[i]` 存什么？写出 `prefix(i)` 和 `add(i, delta)`，并手算 `a = [3,1,4,1,5,9,2,6]` 的 `prefix(7)`。

## A
**规则**：`tree[i]` 存 `a` 在区间 **(i − lowbit(i), i]** 上的和，即以 i 结尾、长度 lowbit(i) 的一段。`a = [3,1,4,1,5,9,2,6]`：`tree = [3, 4, 4, 9, 5, 14, 2, 31]`（`tree[4]` = 3+1+4+1，`tree[6]` = 5+9，`tree[8]` = 全部）。

```java
long prefix(int i) {
    long r = 0;
    for (; i > 0; i -= i & -i) r += tree[i];     // 抹掉最低位的 1
    return r;
}
void add(int i, long delta) {
    for (; i <= n; i += i & -i) tree[i] += delta; // 跳到下一个管着 i 的格子
}
```
`prefix(7)`：`tree[7]=2`（管 (6,7]），`7 - 1 = 6`，`tree[6]=14`（管 (4,6]），`6 - 2 = 4`，`tree[4]=9`，`4 - 4 = 0` 结束：2+14+9 = **25** ✓。步数是 7 = 111₂ 中 1 的个数 3。

`add(3, +10)`：更新 `tree[3]`，`3+1=4` 更新 `tree[4]`，`4+4=8` 更新 `tree[8]`，`8+8=16 > 8` 停。

练习：`a = [2,7,1,8,2,8]` → `tree = [2, 9, 1, 18, 2, 10]`，`prefix(5) = tree[5]+tree[4] = 20`；`add(2,+5)` 更新 `tree[2]`、`tree[4]`（`2+2=4`，`4+4=8>6`）。区间和：`rangeSum(l, r) = prefix(r) - prefix(l-1)`。

**线性建树**（O(n)，比逐个 add 的 O(n log n) 快）：先填 `tree[i]` 原值，再从小到大遍历 i，把 `tree[i]` 加到父节点 `tree[i + lowbit(i)]`：`for i in 1..cap: p = i + (i & -i); if (p <= cap) { cnt[p] += cnt[i]; sum[p] += sum[i]; }`。从小到大保证 `tree[i]` 加到父节点时已收齐自己的孩子。

Fenwick 的限制：运算须有逆元（求和可以，最大值不行）。
