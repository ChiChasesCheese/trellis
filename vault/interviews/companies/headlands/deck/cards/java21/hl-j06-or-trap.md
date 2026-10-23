---
id: hl-j06-or-trap
node: java21.j06-instanceof-pattern
type: qa
step: 17
---
## Q
`o instanceof String s || s.length() > 2` 为什么编译不过？想表达"不是 String 或是空串"该怎么写？

## A
`||` 右边在左边为**假**时才计算，此时 `o` 不是 `String`，`s` 没有绑定，所以 `cannot find symbol`。

正确写法：
```java
!(o instanceof String s) || s.isEmpty()
```
左边为假 = 匹配成功，所以 `||` 右边 `s` 一定有值。
