---
id: hl-omap-range-sum-code
node: foundations.ordered-maps-trees
type: qa
step: 40
---
## Q
给定价位表 `NavigableMap<Integer,Integer> book`，写一个方法返回价格在 [lo, hi] 内的总数量，复杂度是多少？

## A
```java
static long volumeBetween(NavigableMap<Integer, Integer> book, int lo, int hi) {
    long sum = 0;
    for (int qty : book.subMap(lo, true, hi, true).values()) sum += qty;
    return sum;
}
```
对 `{101=50, 103=20, 105=70, 110=10}`，区间 [102, 105] 返回 90。复杂度 **O(log n + k)**，k 是区间内价位数：O(log n) 找起点，之后顺序遍历 k 个。查询非常频繁时维护前缀和（Fenwick 树）达到 O(log n)。
