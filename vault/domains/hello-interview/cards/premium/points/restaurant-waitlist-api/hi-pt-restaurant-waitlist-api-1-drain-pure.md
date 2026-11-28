---
id: hi-pt-restaurant-waitlist-api-1-drain-pure
node: qb.lld.restaurant-waitlist-api.points
type: qa
step: 1
---
## Q
**餐厅候位 API · 规则集中的纯函数**｜必会 · 出自：餐厅候位 API › 深入 1

入座、结束用餐、等位估计都要回答"此刻谁坐哪张桌"。这条规则写在哪里，怎么保证预测和现实一致？

## A
**做法。** 写成一个不读实例状态的纯函数 `_drain(queue, free, sizes)`：就地修改传进来的队伍和空闲桌，返回 `(人, 桌号)` 列表。真实操作传真状态，估计传副本。

**为什么。** 规则只写一遍，预测与现实就不会各说各话；写进方法里，估计就得复制一份，两份迟早不一致（函数式核心，命令式外壳）。
