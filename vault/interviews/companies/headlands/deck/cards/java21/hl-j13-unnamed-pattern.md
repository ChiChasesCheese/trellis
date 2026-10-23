---
id: hl-j13-unnamed-pattern
node: java21.j13-unnamed-variables
type: qa
step: 7
---
## Q
什么是未命名模式（unnamed pattern）？在 record 解构里怎么用 `_` 跳过不关心的字段？编译器会为 `_` 位置调用访问器吗？

## A
`_` 单独作为「模式」：匹配任何东西，**不绑定变量**。

```java
case Fill(var id, _, _) -> id;         // 只取第一个字段
case Reject(var id, _) -> id;
case Placed(Order(_, Side s, _, var q)) when q >= 1000 -> ...   // 可嵌套
```
字节码只调用你**需要**的访问器（如 `id()`），不为 `_` 位置调用访问器。
