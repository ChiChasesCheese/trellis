---
id: patterns-misuse-traps
node: patterns.selection
type: qa
---
## Q
Name the signature misuse of each: singleton, observer, mediator, visitor.

## A
- **Singleton** → global mutable state in disguise: hidden dependencies, shared state across tests, hard-coded concretes.
- **Observer** → invisible control flow: cascading notifications where nobody can trace why a change happened; update storms and ordering bugs (and leaks from forgotten unsubscribes).
- **Mediator** → the god object: all interaction logic drains into one class until the mediator *is* the coupling you tried to remove.
- **Visitor** → rigidity: applied to a hierarchy that still grows, so every new element type breaks every visitor.

Common thread: each pattern trades one kind of coupling for another — the misuse is ignoring what you paid.

## Q zh
列出三个模式在初级设计中最常被滥用的方式。

## A zh
1. **Singleton 作为全局状态容器**：「嘿，我们都需要访问配置/日志记录器」→ Singleton。实际上这就是多线程下的测试恶梦和隐藏耦合。改用依赖注入。

2. **过度工厂**：每个类都得到 `Factory`，即使从不有多个实现。工厂是用来**解耦创建**的，不是用来规范化的。如果只有一个实现，构造函数就够了。

3. **Decorator 滥竽充数为 Strategy**：「我们用 Decorator 处理日志」（好），但然后用它处理「我可以用三种算法之一处理这个」（不好——改用 Strategy）。混淆会导致嵌套层级混乱。
