---
id: hl-j12-static-shortcuts
node: java21.j12-scoped-values
type: qa
step: 8
---
## Q
JDK 21 的 `ScopedValue.runWhere / callWhere / getWhere` 是什么？它们在后续版本命运如何？

## A
它们是 JDK 21 的静态快捷方式（只能单个绑定），等价于 `where(key, v).run/call/get(...)`，例如：

```java
String r2 = ScopedValue.getWhere(USER, "dave", () -> USER.get() + "!");
```
**JDK 24 起 `callWhere` / `runWhere` 被移除**，API 全部「流式」：使用已绑定值的唯一方式是 `Carrier.call` 和 `Carrier.run`。所以 `runWhere(...)`、`callWhere(...)` 在 24 起不能编译，要写成 `ScopedValue.where(KEY, v).run(...)` / `.call(...)`，后者在 JDK 25 仍是标准形式。
