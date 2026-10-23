---
id: hl-javaq-d-q15-intern
node: java-questions.d-memory
type: qa
step: 18
---
## Q
字符串字面量、编译期折叠的拼接、运行时拼接、`new String`、`intern()` 之间用 `==` 比较各给什么结果？为什么？

## A
- 字面量 `==` 编译期折叠的 `"hel" + "lo"`：**true**，折叠成同一个常量池对象。
- 字面量 `==` 运行时拼接：**false**，运行时拼接得到新对象。
- 字面量 `==` `new String(...)`：**false**。
- 字面量 `==` `s3.intern()`：**true**，`intern()` 返回常量池里的那一份。
- 只有**编译期常量变量**（`final String` 等）参与的 `+` 才会折叠。
- `hashCode` 缓存：5000 万字符的字符串，第一次约 31776 μs，第二次 0 μs。
