---
id: hi-c-lld-introduction-n06-trip-sketch
node: lld.in-a-hurry.introduction.notes
type: qa
step: 6
---
## Q
**LLD 导论 · 一个典型的 LLD 产出长什么样**｜摘要 · 追问

LLD 面试最后留在白板上的代码，大致体现哪几种建模手法？以"行程（Trip）"为例。

## A
- **状态用枚举：** `TripState`（已请求、已派单、行驶中、已完成、已取消）而不是几个布尔值，这样不会出现互相矛盾的状态组合。
- **转换方法先校验当前状态：** 每个动作（派单、开始、完成）先检查当前状态，不合法就抛错，所以非法的状态转换根本进不来。
- **规则外置：** 计费交给传入的 `PricingCalculator`，`Trip` 自己不知道价格公式，换计价规则不用改 `Trip`。
- **终态保护：** 已完成的行程不能再取消，终态不可逆。
