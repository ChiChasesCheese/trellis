---
id: craft-derived-not-stored-5-across-problems-and-scales
node: craft.patterns.derived-not-stored
type: qa
step: 5
---
## Q
**派生而非存储 · 海战棋、网约车、租车、配送员薪酬、订座里的同一个原则**｜模式

这些问题里，沉没、起点时间、车的位置、应付薪酬、座位号，都没有存成字段。它们共享什么判断？放大到数据库和事件溯源，这个原则的名字是什么？

## A
**要点。** 都是：只存**事实**（被击中的格子、状态变化的记录、行程、事件时间戳），把可以由事实算出的值写成方法或属性。事实只有一份，且不会因为某条路径的疏漏而与派生值不一致。

```python
# battleship-game：沉没由格子和命中集合算出
return len(self.hits) == len(self.cells)
# ride-sharing：开始时间读状态轨迹，"不另存一个字段，就不会有两份真相"
return next((c.at for c in self._history if c.current is TripState.IN_PROGRESS), None)
# dasher-payout：应付金额由事件时间戳现算，更正一个时间戳，钱自动跟着对
total = sum((seg.amount_exact for seg in self._segments(delivery_id)), Fraction(0))
# LeetCode 362 Hit Counter：存时间戳，点击数按窗口现算
return len(self.ts) - bisect_right(self.ts, t - 300)
```

**见于。** battleship-game、ride-sharing、car-rental、dasher-payout、airline。

**不变的。** 事实有一个所有者；派生值是事实的函数。**变化的。** 派生值的参数（有的只依赖事实，有的还依赖时间，像 `location_at(moment)` 和滑动窗口）；以及是否值得缓存。

**信号。** 你正要加一个字段，名字像 `is_xxx`、`current_xxx`、`total_xxx`、`last_xxx`；或者需求里出现「更正」「悔棋」「改签」「提前预约」，说明事实会被改，派生值必须跟着变。

**尺度对照。** 力扣：存时间戳，窗口计数现算。低层设计：属性、时间的函数、受控的缓存。分布式：数据库范式化与生成列（generated column，列由别的列算出）；事件溯源（event sourcing）里状态是事件流的折叠，物化视图（materialized view）是有意缓存的派生，用刷新机制保证它最终追上事实。变化：单机里「缓存与事实同步」靠同一个临界区；分布式里它变成最终一致，物化视图落后事实一段时间，调用方要能容忍，也要有办法从事实重建它。
