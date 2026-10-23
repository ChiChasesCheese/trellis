---
id: hl-j06-after-if
node: java21.j06-instanceof-pattern
type: qa
step: 18
---
## Q
下面哪种写法能在 `if` 之后使用 `s`？为什么？

```java
// A
if (o instanceof String s) { return 1; }
return s.length();
// B
if (!(o instanceof String s)) { System.out.println("no"); }
System.out.println(s);
```

## A
两种都**不能**：
- **A**：`s` 只在 `if` 块内可用，`if` 之后不一定匹配，`return s.length()` 编译错误。
- **B**：`if` 块只打印、能正常走完，之后不一定匹配，`s` 仍不可用。

要在 `if` 之后用 `s`，必须写成 `if (!(o instanceof String s)) { return/throw/continue; }`，保证没匹配的路径**不能正常结束**。
