---
id: hl-j03-when-not-switch
node: java21.j03-pattern-switch
type: qa
step: 26
---
## Q
哪三种场景不适合用模式匹配 `switch`？新增变体对公共库有什么影响？

## A
1. **变体 > 20 种且在热路径**：先实测；虚方法（每个 `record` 实现 `apply()`）可能更快，也更符合开闭原则。
2. **分派逻辑属于对象自己、多处复用**：写成接口方法，别在外面反复 `switch`。
3. **只有一个条件**：`if (o instanceof Foo f && ...)` 更直接。

兼容性：不重编译的旧 `switch` 遇到新变体会抛 `MatchException`，所以公共库的 `sealed` 层级加成员是**破坏性变更**。
