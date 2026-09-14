---
id: cc-model-state-implicit-entity-creation
node: model.entity-state
type: qa
---
## Q
A charge arrives for an account that was never declared in the setup block. Does your program create an account for it?

## A
**Whatever the statement says — and the statement almost always says something, because it is a hidden test.**

The three answers all appear in real specs: *count but never flag* (the entity exists in the tallies, but with no category it can never cross a threshold); *drop silently* (a transaction whose merchant is undeclared never creates one); *create with defaults*.

Write the choice at the one place an entity can come into existence — a `get_or_create` helper, or an explicit `if id not in accounts: return`. Scattering `defaultdict` access is how you accidentally pick "create with defaults" without deciding.

## Q zh
来了一笔扣款，其账户从未在配置块里声明过。你的程序会为它创建账户吗？

## A zh
**按题面说的做 —— 而题面几乎总会说，因为这就是一个隐藏测试。**

三种答案在真实题面里都出现过：**计数但永不标记**（实体存在于统计里，但没有类别就永远越不过阈值）；**静默丢弃**（商户未声明的交易绝不创建商户）；**用默认值创建**。

把这个选择写在实体唯一能诞生的地方 —— 一个 `get_or_create` 辅助函数，或一句明确的 `if id not in accounts: return`。到处散着 `defaultdict` 访问，就是你在没做决定的情况下意外选了"用默认值创建"。
