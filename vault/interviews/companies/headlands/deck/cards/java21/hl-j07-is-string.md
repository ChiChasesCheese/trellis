---
id: hl-j07-is-string
node: java21.j07-text-blocks
type: qa
step: 4
---
## Q
文本块是一种新类型吗？和等价的旧写法字符串用 `equals` 和 `==` 比较各得什么？为什么？

## A
文本块**不是新类型**，就是 `java.lang.String`。

等价内容的文本块与旧写法 `"{\n  \"symbol\": \"AAPL\",\n  \"qty\": 100\n}\n"`：
- `equals` → `true`；
- `==` 也是 **`true`**：文本块是**编译期常量**，和普通字面量一样进常量池（constant pool），内容相同共用一份（`javap` 看两次 `ldc` 指向同一项）。
