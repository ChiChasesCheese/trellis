---
id: hl-javaq-f-q33-say60
node: java-questions.f-concurrency
type: qa
step: 38
---
## Q
用英文 60 秒回答：What is safe publication? Why is double-checked locking broken without `volatile`? What do `final` fields guarantee?

## A
结构：安全发布 = 用 happens-before 边发布引用及其字段 → DCL 的重排问题与 volatile 修复 → 更简单的 holder 或枚举 → final 字段的冻结保证，前提是 this 不逃逸。

> "Safe publication means making an object's reference visible to another thread in a way that also makes its fields visible, using a happens-before edge: a volatile field, a final field, a static initializer, a lock, or a concurrent collection. Double-checked locking without `volatile` is broken because the reference write can be reordered before the constructor's writes, so another thread can see a non-null but half-built object; marking the field volatile fixes it, but a holder class or enum is simpler. `final` fields get a special guarantee: once the constructor finishes, any thread that sees the reference sees the final fields correctly, which is why immutable objects and records are safe to hand across threads as long as `this` doesn't escape during construction."
