---
id: method-extension-probe
node: method.evaluation
type: qa
---
## Q
The interviewer probes: "how would you add a new vehicle type / discount rule?" What separates a passing answer from a strong one?

## A
- **Passing**: correctly describing which code you'd edit.
- **Strong**: the change is *additive* — one new class or enum constant implementing an existing interface, registered in one place, zero edits to existing conditionals.

If your design would force shotgun edits, say so and name the refactor (extract a strategy interface) — owning the weakness scores better than defending it.


## Q zh
面试官探测："你会怎样添加一个新的车辆类型/折扣规则?"什么将通过答案与强答案分开?

## A zh
- **通过**: 正确描述你会编辑哪个代码。
- **强**: 改变是**加法的** — 一个新类或枚举常数实现现有接口，在一个地方注册，零编辑到现有条件语句。

如果你的设计会强制霰弹枪编辑，说出来并命名重构（提取策略接口）— 拥有弱点的得分比辩护它好。
