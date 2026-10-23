---
id: hl-j03-dominance
node: java21.j03-pattern-switch
type: qa
step: 6
---
## Q
`switch` 模式匹配里的"支配"（dominance）是什么？下面的写法会报什么错？

```java
case Object x -> "obj";
case String s -> "str";
```

## A
从上到下第一个匹配生效，所以**范围大的分支不能写在范围小的前面**。若标签 A 能匹配的值**包含**标签 B 的全部（A 是 B 的父类型且 A 无守卫），则 A **支配**（dominates）B，B 必须写在 A 前面。

这段代码编译错误：`this case label is dominated by a preceding case label`——`String s` 永远走不到。

口诀：**先具体、后一般；带守卫在前、不带在后；`default` 最后。**
