---
id: hl-j06-guard-clause
node: java21.j06-instanceof-pattern
type: qa
step: 7
---
## Q
补全代码：用卫语句（guard clause）写 `firstChar(Object o)`：不是字符串返回 `"not a string"`，否则返回 `"first char of " + s + " is " + s.charAt(0)`。这种写法有什么好处？

## A
```java
static String firstChar(Object o) {
    if (!(o instanceof String s)) {
        return "not a string";
    }
    return "first char of " + s + " is " + s.charAt(0);    // s 在这里可用！
}
```
好处：少一层缩进，"出错情况先处理，正常路径往下写"。

前提：`if` 块**不能正常结束**（必须 `return` / `throw` / `break` / `continue`），否则 `if` 之后 `s` 不一定匹配，不可用。
