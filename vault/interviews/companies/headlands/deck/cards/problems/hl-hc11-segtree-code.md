---
id: hl-hc11-segtree-code
node: problems.hc11-order-interval-overlap
type: qa
step: 10
---
## Q
写出标记永久化线段树的 `rangeAdd` 和 `rangeMax`。哪两行最容易漏？

## A
```java
private void rangeAdd(int node, int nl, int nr, int l, int r, int delta) {
    if (l <= nl && nr <= r) { add[node] += delta; mx[node] += delta; return; }  // 整段覆盖：只记在这个结点
    int mid = (nl + nr) >>> 1;
    if (l <= mid) rangeAdd(2 * node, nl, mid, l, r, delta);
    if (r > mid)  rangeAdd(2 * node + 1, mid + 1, nr, l, r, delta);
    mx[node] = add[node] + Math.max(mx[2 * node], mx[2 * node + 1]);
}
private int rangeMax(int node, int nl, int nr, int l, int r) {
    if (l <= nl && nr <= r) return mx[node];
    int mid = (nl + nr) >>> 1;
    int best = Integer.MIN_VALUE;
    if (l <= mid) best = Math.max(best, rangeMax(2 * node, nl, mid, l, r));
    if (r > mid)  best = Math.max(best, rangeMax(2 * node + 1, mid + 1, nr, l, r));
    return best + add[node];     // 本结点还欠着的整体加数，孩子不知道
}
```
`(node, nl, nr)` 表示当前结点管下标区间 `[nl, nr]`，`(l, r)` 是操作区间。最容易漏：
1. `rangeMax` 末尾的 `+ add[node]`（删掉整体平移的标记就丢了）；
2. `rangeAdd` 末尾 `mx[node] = add[node] + …` 里的 `add[node]`。
中点用 `(nl + nr) >>> 1`；递归深度 ≤ ⌈log₂ size⌉ ≈ 20；每操作每层最多访问常数个结点，O(log m)。
