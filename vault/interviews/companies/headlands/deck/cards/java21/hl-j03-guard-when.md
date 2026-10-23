---
id: hl-j03-guard-when
node: java21.j03-pattern-switch
type: qa
step: 5
---
## Q
`switch` 模式匹配里的守卫（guard）`when` 怎么写？一个分支"匹配"的完整条件是什么，守卫为假时怎么办？

## A
```java
return switch (o) {
    case Integer i when i < 0 -> "negative";
    case Integer i when i < 10 -> "small";
    case Integer i -> "big";
    ...
};
```
`when` 后跟布尔表达式。分支匹配 = **类型匹配 并且 守卫为真**；守卫为假则**继续试后面的分支**（含同类型的下一个）。守卫里可用刚绑定的变量（如 `i < 0`）。
