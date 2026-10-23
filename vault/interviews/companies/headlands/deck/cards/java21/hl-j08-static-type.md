---
id: hl-j08-static-type
node: java21.j08-var
type: qa
step: 11
---
## Q
`var list = new ArrayList<Fill>();` 的变量类型是 `List<Fill>` 还是 `ArrayList<Fill>`？想只依赖接口该怎么写？

## A
是 **`ArrayList<Fill>`**：推导的是"右边表达式的静态类型"，不是你心里想的类型。

想限制成接口（限制可调用方法、方便换实现）就**显式写**：
```java
List<Fill> list = new ArrayList<>();
```
这样表达了"只依赖 `List`"。
