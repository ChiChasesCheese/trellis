---
id: problems-ride-sharing-two-tables-not-state-classes
node: problems.marketplaces.ride-sharing
type: qa
step: 4
tags: [grown]
---
## Q
网约车的行程生命周期（REQUESTED → MATCHED → ARRIVED → IN_PROGRESS → COMPLETED，外加 CANCELLED）为什么用两张表而不是状态模式（State，每个状态一个类）？两张表分别管什么？

## A
两张模块级的表：

```python
ALLOWED_TRANSITIONS = {
    TripState.REQUESTED: frozenset({TripState.MATCHED, TripState.CANCELLED}),
    TripState.MATCHED: frozenset({TripState.ARRIVED, TripState.CANCELLED}),
    TripState.ARRIVED: frozenset({TripState.IN_PROGRESS, TripState.CANCELLED}),
    TripState.IN_PROGRESS: frozenset({TripState.COMPLETED}),
}
CANCELLABLE_BY = {
    TripState.REQUESTED: frozenset({Party.RIDER, Party.SYSTEM}),
    TripState.MATCHED: frozenset({Party.RIDER, Party.DRIVER, Party.SYSTEM}),
}
```

第一张管「能往哪走」，第二张管「谁有权走」——这是两件事，挤进一张表就会变成一堆特判。

判据：**状态之间只有「允许／不允许」的差别，用表；状态之间有行为和数据的差别，才用类。** 行程在每个状态下什么也不「做」，不像电梯在「上行」和「待机」时对同一个按钮有截然不同的响应。为一层纯粹的许可关系造六个类、写一堆「此状态下该动作非法」的空方法，是把两张十行的表摊成六个文件。表还能被程序读：画状态图、统计转移覆盖率、生成文档都只是遍历一次。

纪律：非法转移**抛异常，绝不静默忽略**；每次转移追加一条留痕（时刻、从哪到哪、谁干的、为什么），因为「这单几点被谁取消的」只能来自事中记录。
