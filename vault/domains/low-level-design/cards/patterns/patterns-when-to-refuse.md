---
id: patterns-when-to-refuse
node: patterns.selection
type: qa
---
## Q
In an LLD round, what signals tell you to REFUSE a pattern, and what's the disciplined way to hold the door open for it?

## A
Refuse when:

- There's **one concrete case** and the second is hypothetical — an interface with a single implementation is speculative generality (YAGNI / rule of three: abstract on the ~3rd occurrence, not the 1st).
- The pattern adds **more classes than the logic it organizes** — a strategy interface + factory + 2 one-line strategies vs a 5-line `if`.
- You'd be pattern-dropping to impress: the interviewer grades whether the design fits, not vocabulary count.

Disciplined move: write the simple version, then **say out loud where the seam is** — "if a third pricing rule appears, this `if` becomes a `PricingStrategy`." Patterns are best introduced as *refactoring targets* when duplication actually arrives, not as upfront scaffolding.

## Q zh
你被要求为一个简单问题添加一个模式。何时说「不，不需要」？

## A zh
**拒绝条件**：

1. **模式解决不存在的问题**。例：添加 Singleton「为了标准化」，但没有多个实例或全局访问的实际需求。

2. **普通代码已经足够**。
   - 一个排序函数；不需要 Strategy。
   - 一个工厂方法；不需要 Factory Method 接口和子类。
   - 一个类 with `log()` 和 `save()` 方法；不需要 Decorator。

3. **模式会增加成本**：
   - 增加文件数量。
   - 使代码路径变长/间接。
   - 引入初级开发人员的学习曲线。

**黄金法则**：首先用普通代码写它。模式是**针对重复出现的问题的重构**，不是初始设计。
