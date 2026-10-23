---
id: hl-j01-array-component
node: java21.j01-record
type: qa
step: 23
---
## Q
为什么不要把数组放进 `record` 当组件？`new Leaky(new int[]{99,2,3}).equals(l)` 得到什么？

## A
`record` 的 `equals` 对数组组件用的是 `Object.equals`，即**引用比较**，所以两个数组内容一样也是 **`false`**。

再加上数组的内容可被外部修改（浅不可变），所以**别把数组放进 `record`**。改用 `List<Long>`（构造时 `List.copyOf`），或自己包一层。
