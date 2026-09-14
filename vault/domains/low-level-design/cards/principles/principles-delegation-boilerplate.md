---
id: principles-delegation-boilerplate
node: principles.composition
type: qa
---
## Q
"Just use composition" — name the two real costs of replacing inheritance with delegation, and how each is mitigated.

## A
- **Forwarding boilerplate**: to keep the wrapped type's interface you hand-write N one-line methods, and each new interface method must be added to every wrapper. Mitigation: a reusable `ForwardingX` base your wrappers extend (Effective Java's skeletal forwarding class), IDE-generated delegates, Kotlin `class A(b: B) : B by b`, Lombok `@Delegate`.
- **Lost self-reference (the SELF problem)**: the inner object calls *its own* methods, not the wrapper's — so a counting/logging decorator misses calls the wrapped object makes internally, and the inner object passing `this` to a callback leaks the undecorated object.

The second cost is fundamental, not syntax; but note it's the same self-use that makes inheritance fragile — composition at least makes it visible.

## Q zh
什么时候你会看到委托而不是继承，什么时候 Extract Class 会引入样板代码？

## A zh
当 A 委托给 B 时——B 的公共接口完全被 A "代理" 到那些委托方法中。这不是组合，而是代理对象，通常是因为继承会带来不必要的复杂性或紧耦合。

Extract Class 可能会导致样板代码，当：
- 新类只是持有从原始类转移的字段，但没有实现新的行为
- 原始类需要获取器和设置器来访问新类的字段

