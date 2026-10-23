---
id: hl-omap-sweep-book
node: foundations.ordered-maps-trees
type: qa
step: 26
---
## Q
用 `TreeMap` 写一个撮合循环：asks 为 `{101=50, 103=20, 105=70, 110=10}`，买入 80 手，从最低卖价开始吃。买盘 `TreeMap` 应该怎么排序？

## A
```java
int need = 80;
while (need > 0 && !asks.isEmpty()) {
    Map.Entry<Integer, Integer> level = asks.firstEntry();  // 最优价 O(log n)
    int take = Math.min(need, level.getValue());
    need -= take;
    if (take == level.getValue()) asks.pollFirstEntry();    // 吃光，整档删除
    else asks.put(level.getKey(), level.getValue() - take); // 部分成交
}
```
成交 50@101、20@103、10@105，剩余 `{105=60, 110=10}`。

买盘（bids）最优价是**最高价**，所以买盘用 `new TreeMap<>(Comparator.reverseOrder())`，让 `firstEntry()` 返回最高价。
