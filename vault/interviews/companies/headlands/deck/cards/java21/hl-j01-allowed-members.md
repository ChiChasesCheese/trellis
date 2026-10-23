---
id: hl-j01-allowed-members
node: java21.j01-record
type: qa
step: 6
---
## Q
`record` 的主体里可以放哪四类东西？

## A
1. **静态字段、静态方法、静态嵌套类型**：可以，如 `static final long MAX_QTY = 1_000_000;`。
2. **实例方法**：可以，和普通类一样，如 `long notionalTicks() { return Math.multiplyExact(priceTicks, qty); }`。
3. **额外的构造器**：可以，但第一句必须是 `this(...)`，如 `Order(long id, ..., long priceTicks) { this(id, ..., priceTicks, 1); }`。
4. **实现接口**：可以，如 `record Fill(...) implements Comparable<Fill> { ... }`。

不能放的东西见下一张卡。
