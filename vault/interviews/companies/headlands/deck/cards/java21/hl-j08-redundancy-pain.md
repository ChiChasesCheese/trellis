---
id: hl-j08-redundancy-pain
node: java21.j08-var
type: qa
step: 1
---
## Q
Java 8 声明局部变量必须写类型，有哪四个痛点？Java 7 的 `<>` 解决了哪一部分？

## A
`<>`（diamond）让右边省略一次泛型实参，但遍历时 `for (Map.Entry<String, List<Fill>> e : ...)` 仍要完整写一遍。

四个痛点：
1. **冗余**：`new HashMap<...>()` 已说明类型，左边再写一遍没有新信息；
2. **泛型越复杂越长**，如 `Map<String, Map<Side, List<Map.Entry<Long, String>>>>`；
3. **类型名遮挡变量名和意图**：有意义的 `bySymbol` 被挤到中间；
4. **有些类型根本写不出来**（匿名类自己的类型、交叉类型），只能向上转型，丢掉其中的成员。

`var`（Java 10）解决这些，Java 11 起可用于 lambda 形参。
