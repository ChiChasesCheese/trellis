---
id: hl-j03-null-bytecode
node: java21.j03-pattern-switch
type: qa
step: 14
---
## Q
模式匹配 `switch` 的 NPE 行为在字节码里是怎么实现的？写和不写 `case null` 各怎么处理？

## A
- **没写 `case null`**：编译器在最前面插入 `Objects.requireNonNull(selector)`，所以选择器为 `null` 时抛 NPE。
- **写了 `case null`**：不插 `requireNonNull`，让 `typeSwitch` 返回的 `-1` 直接跳到你写的 `null` 分支。

这就是为什么没写 `case null` 时 `default` 也救不了 `null`：NPE 在到达分派之前就抛了。
