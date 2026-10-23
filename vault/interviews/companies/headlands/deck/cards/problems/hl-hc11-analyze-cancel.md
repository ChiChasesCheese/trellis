---
id: hl-hc11-analyze-cancel
node: problems.hc11-order-interval-overlap
type: qa
step: 5
---
## Q
Part 2 的 `analyze` 怎么处理买卖方向和撤单？为什么 `all.count` 不等于 `buy.count + sell.count`？

## A
撤单只是**修改区间**：`end` 改成 `min(end, cancelTime)`。步骤：
1. 第一遍扫事件：`Place` 存进 `HashMap<id, Place>`（`putIfAbsent`，重复 id 报 `IllegalArgumentException`）；`Cancel` 存进 `HashMap<id, 最早撤单时间>`（`merge(id, time, Math::min)`，同一 id 多次撤单**最早的生效**）；
2. 检查每个撤单 id 都有对应 `Place`（先收集后处理，所以事件顺序无所谓，撤单写在 Place 前面也行）；
3. 每个 Place 的有效区间 `[start, min(end, cancel))`；有效结束 `<= start`（撤单时间 ≤ start，开始前或开始瞬间）→ 这张单从没活过，跳过；撤单时间 `>= end` → 无影响；
4. 按方向分到三个车道 BUY、SELL、ALL，各自做 Part 1 的扫描。

```java
switch (e) {
    case Place p -> { if (places.putIfAbsent(p.id(), p) != null) throw new IllegalArgumentException("duplicate order id " + p.id()); }
    case Cancel(var id, var time) -> cancelAt.merge(id, time, Math::min);
}
Lane lane = switch (p.side()) { case BUY -> buy; case SELL -> sell; };
```
`OrderEvent` 是 sealed，switch 不写 `default`；新增 `Amend` 时没处理的 switch 编译报错；`Side` 加值时那行表达式编译失败。`Lane` 是私有小容器（两个 `long[]` 加计数，预分配 `places.size()`），避免 `ArrayList<Long>` 装箱。

**ALL 车道必须单独扫描**：买方峰值和卖方峰值可以出现在不同时刻，`all.count` ≠ `buy.count + sell.count`。样例：`Place(1,BUY,0,10) Place(2,BUY,2,8) Place(3,SELL,3,6) Place(4,SELL,4,12) Place(5,BUY,5,9) Cancel(2,6) Cancel(4,5)`，有效区间 1:[0,10) 2:[2,6) 3:[3,6) 4:[4,5) 5:[5,9)。buy=`Peak(3,5)`（t=5：订单 1、2、5）；sell=`Peak(2,4)`（订单 3、4）；all=`Peak(4,4)`（t=4：1,2,3,4；t=5：1,2,3,5 也是 4，取最早），3+2≠4。去掉两个 Cancel 则 all=`Peak(5,5)`——撤单改变了答案。

复杂度 O(n log n)：50 万 Place + 25 万 Cancel 约 85–125 ms。
