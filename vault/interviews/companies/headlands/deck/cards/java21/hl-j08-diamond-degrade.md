---
id: hl-j08-diamond-degrade
node: java21.j08-var
type: qa
step: 12
---
## Q
`var list = new ArrayList<>();` 的类型是什么？之后 `list.add(1); list.add("x");` 能编译吗？应该怎么写？

## A
类型是 **`ArrayList<Object>`**：右边的 `<>` 无类型信息可推，`var` 也没有左边的类型来提供，于是退化成 `Object`。两个 `add` 都合法，几乎总是 bug。

应写：
```java
var list = new ArrayList<Fill>();
List<Fill> list = new ArrayList<>();
```
同理 `var l = Collections.emptyList();` 得到 `List<Object>`，而 `List<String> l = Collections.emptyList();` 推出 `List<String>`。`var` **不提供目标类型**帮助推导。
