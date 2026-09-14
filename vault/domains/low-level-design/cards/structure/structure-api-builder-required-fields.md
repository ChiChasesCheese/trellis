---
id: structure-api-builder-required-fields
node: structure.api
type: qa
---
## Q
When does a fluent builder beat constructors/setters, and where do you enforce required fields and invariants with a builder?

## A
- Builder wins when a type has **several optional parameters** (telescoping-constructor smell) or you want an **immutable** object assembled step by step. Two params, all required → just use a constructor.
- **Required fields go in the builder's constructor** (can't even start without them); optional ones are fluent methods.
- **Cross-field invariants are validated once, in `build()`** (e.g. `start < end`), so an invalid object can never exist.

Bonus: the built class gets a private constructor taking the builder — no setters, so every instance is valid and thread-safe to share.


## Q zh
什么时候流式构造器胜过构造函数/setter，以及你在哪里用构造器执行必需字段和不变式?

## A zh
- 构造器赢当一个类型有**多个可选参数**（伸缩构造器味道）或你想要一个**不可变**对象逐步组装。两个参数，所有必需 → 就用一个构造函数。
- **必需字段进入构造器的构造函数**(甚至不能不它们就开始)；可选的是流式方法。
- **跨字段不变式验证一次，在 `build()`**(例如 `start < end`)，所以一个无效的对象永远不能存在。

额外: 构建的类得到一个私有构造函数接受构造器 — 没有 setter，所以每个实例是有效的和线程安全的共享。
