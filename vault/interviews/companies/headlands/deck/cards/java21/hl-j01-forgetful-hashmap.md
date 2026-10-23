---
id: hl-j01-forgetful-hashmap
node: java21.j01-record
type: qa
step: 3
---
## Q
一个值对象类忘了重写 `equals` / `hashCode`，用 `m.put(new Fill("AAPL",100), "first")` 之后，`m.get(new Fill("AAPL",100))` 得到什么？为什么？

## A
得到 **`null`**：内容一样的对象却查不到。

原因：`HashMap` 先用 `hashCode()` 选桶（bucket）。默认 `hashCode()` 基于**对象身份**，两个不同对象几乎必落在不同桶，根本走不到 `equals` 的比较。

这是运行时的悄悄错误，编译器不会提醒。`record` 自动生成配套的 `equals` / `hashCode`，不会漏。
