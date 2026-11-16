---
id: lcp-actor-follow-notifications-state-and-invariant
node: lcproject.lcp-actor-follow-notifications
type: qa
step: 2
tags: [作答]
---
## Q
在 CastWatch 的关注与通知服务里，你要存哪些状态？每一块用什么结构？哪条不变量最要紧，什么写法会把它破坏？

## A
**评分点**
- 说出三块状态：关注索引（演员 → 关注者集合）、电影表（id → 片名加冻结的卡司集合）、收件箱（用户 → 按序追加的通知列表）
- 说出关注索引按演员建：新片上线只需对卡司求关注者并集，不用遍历全部用户，并集天然去重
- 说出最要紧的不变量：每部已登记的电影，对它登记那一刻的受众恰好一条通知，电影表和收件箱的写入不可分
- 说出集合清空就删掉，索引大小只和现存关注关系成正比；通知是 frozen 的不可变值
- 说出破坏方式：先写电影再算受众且中途失败；关注索引与电影表各用一把锁；存调用方传入的列表引用；返回内部列表

<details class="pt"><summary>参考答案</summary>

三块状态：`dict[演员, set[用户]]`、`dict[电影 id, (片名, frozenset 卡司)]`、`dict[用户, list[Notice]]`。按演员建索引，新片上线对卡司取并集即得受众，每人一次。核心不变量：每部登记的电影对登记时刻的受众恰好一条通知，所以"判重、算受众、写电影、写收件箱"同在一把锁里，先算后写。卡司入参立即复制成 `frozenset`，空集合立刻删除，读收件箱返回新列表。

</details>

**知识点：** 防御性拷贝（Defensive Copying）、复合操作（Compound Actions）、观察者与事件（Observer）
