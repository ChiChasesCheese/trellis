---
id: hl-j01-shallow-immutability
node: java21.j01-record
type: qa
step: 22
---
## Q
为什么说 `record Leaky(int[] data)` 是"浅不可变"（shallow immutability）？怎么改成真正不可变？

## A
`record` 只保证**字段引用**不变，不保证引用指向的东西不变：
```java
record Leaky(int[] data) {}
Leaky l = new Leaky(new int[]{1, 2, 3});
l.data()[0] = 99;     // 合法！数组内容被改了
```
组件是 `ArrayList`、`Date`、`StringBuilder`、数组时都一样。

解决：构造时拷贝（`List.copyOf`），或直接用不可变类型（`List.of`、`String`、`long`）。数组组件也可以在构造器里 `data = data.clone()` 并重写访问器返回克隆，但更推荐直接换成不可变集合。
