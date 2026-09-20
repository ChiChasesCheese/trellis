---
id: problems-food-delivery-batch-one-inequality
node: problems.marketplaces.food-delivery
type: qa
step: 5
tags: [grown]
---
## Q
外卖要把两三单拼给同一位骑手。直觉上有三条约束（两家店要近、两单要差不多时候出餐、不能太耽误第一单）。为什么只留一条就够，留哪一条？

## A
只留「拼进来给**第一单**（锚单）增加的送达时延不超过上限」。路线固定为「锚店 → 第二家店 → 锚单地址 → 第二单地址」，那么：

```python
gap = other.ready_at - anchor.ready_at
added = max(travel(a, b), gap) + travel(b, drop) - travel(a, drop)
```

骑手在锚单出餐时拿到第一份，骑到第二家店要 `travel(a, b)`；若第二单还没出餐他还得等，所以这一段是两者取大。**两家店远，`travel(a, b)` 就大；出餐差得多，`gap` 就大——三条约束已经全在这一条不等式里了。**

多配一个旋钮就多一处要向产品解释的取舍，而且几个阈值之间还会互相打架（店很近但出餐差二十分钟，拼还是不拼？）。一个参数、一句能直接对顾客说的业务承诺（「拼单最多让你晚五分钟收到」）胜过三个需要调参的魔数。

配套纪律：锚单按出餐时间排序后取最早的，而且**必须先送到**，否则那句承诺无法兑现，也无法被测试断言。
