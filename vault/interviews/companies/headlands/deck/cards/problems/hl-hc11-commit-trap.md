---
id: hl-hc11-commit-trap
node: problems.hc11-order-interval-overlap
type: qa
step: 7
---
## Q
在线版同一时间戳内先 place 后 cancel 会怎样污染「到现在为止的最大重叠」？封账（commit）怎么解决？

## A
`place(1,BUY,5,9)`、`place(2,BUY,5,9)`、`cancel(1,5)`，时间戳都是 5：place 1 后 live=1，place 2 后 live=2，cancel 1 后 live=1。订单 1 的有效区间是 `[5,5)`，空，从没活过，真正最大重叠是 1。若每次 `place` 后立即把最大值记成 2，就被瞬时的 2 污染。

**解法：封账**。一个时间戳**过去**之后（时钟前进到更大时间）才把它的最终活跃数记入 `committedMax`；当前时间戳的值只在查询时临时参与比较：

```java
// advance(to)：时钟从 lastTick 走到 to
if (live > committedMax) { committedMax = live; committedTime = lastTick; }   // 给过去的时间戳封账
... // 然后折叠到期订单
// peak()
return live > committedMax ? new Peak(live, lastTick) : new Peak(committedMax, committedTime);
```
严格 `>`：相等时较早（已封账）的获胜。只在时钟前进时封账就够：两个相邻事件时间戳之间活跃数只会下降（只有到期），所以全局最大值一定出现在某个有事件的时间戳的**最终**值上。

Part 2 样例走一遍（ALL 车道）：place 1@0 → peak (1,0)；place 2@2 → 封账 (1,0)，peak (2,2)；place 3@3 → (3,3)；place 4@4 → (4,4)；place 5@5 → (5,5)；`cancel 4 @5`（同时间戳）live=4，peak 回到 **(4,4)**——「追溯修正」，与 Part 2 批量版一致；`cancel 2 @6`：封账不更新，折叠 6 到期，撤 2，live=2，peak 仍 (4,4)。**可对每个前缀用批量版 `analyze` 对拍。**

在线练习：`place(1,BUY,3,10)`、`place(2,BUY,4,6)`、`cancel(1,5)`、`advanceTo(6)` → `liveNow()=0`，`peak()=(2,4)`，`liveAt(4)=2`，`liveAt(5)=1`。

其他 bug：撤单忘了撤掉 `expiries` 里原来的结束时间（到期再减一次，计数变负）；撤单时间 ≥ 计划结束仍算生效；先改状态后校验。
