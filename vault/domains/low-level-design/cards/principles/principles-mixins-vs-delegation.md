---
id: principles-mixins-vs-delegation
node: principles.composition
type: qa
---
## Q
Mixins/traits (Java default methods, Scala/Rust traits, Python mixins, Go embedding) promise reuse without forwarding code. What do they actually cost?

## A
They are **inheritance with a wider slot** — the fragility mostly stays:

- **Java default methods**: no instance state, and the same-signature diamond forces an explicit `X.super.m()` override.
- **Python mixins**: reuse comes with the **MRO** — which sibling's method runs depends on the class's linearization order, so a base-class edit can silently reroute behavior.
- **Go embedding**: forwarding is automatic, but there is no virtual dispatch back to the outer type — the SELF problem in full.
- All of them still expose the mixin's members as part of your public surface.

Rule: use a trait/mixin for a **stateless capability** with no per-user variation (`Comparable`, `Serializable`-style). Anything with state or a lifecycle → delegate to a collaborator.

## Q zh
Mixin/trait（Java default method、Scala/Rust trait、Python mixin、Go embedding）承诺不写转发代码就能复用。它们实际的代价是什么？

## A zh
它们是**槽位更宽的继承** —— 脆弱性基本还在：

- **Java default method**：没有实例状态，而且同签名的菱形会强制你显式覆盖并写 `X.super.m()`。
- **Python mixin**：复用是和 **MRO** 绑在一起的 —— 到底跑哪个兄弟类的方法，取决于这个类的线性化顺序，所以改一下基类就可能悄无声息地改变行为走向。
- **Go embedding**：转发是自动的，但不存在回到外层类型的虚分派 —— 完整的 SELF 问题。
- 以上全部都会把 mixin 的成员暴露成你公开接口的一部分。

规则：只把 trait/mixin 用于**无状态的能力**，且各使用方之间没有差异（`Comparable`、`Serializable` 那一类）。凡是带状态或带生命周期的 → 委托给一个协作者。
