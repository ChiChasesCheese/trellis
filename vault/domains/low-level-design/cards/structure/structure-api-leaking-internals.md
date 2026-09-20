---
id: structure-api-leaking-internals
node: structure.api
type: qa
---
## Q
```java
public List<Item> getItems() { return this.items; }  // 内部列表
```
返回内部集合创建的两个故障模式是什么，方法应该返回什么?

## A
- **不变式绕过**: 调用者可以直接 `add`/`remove`，跳过类在其自己的变体中做的验证（总数漂移、容量检查跳过）。
- **并发洞**: 调用者迭代活的列表，当所有者改变它时 — `ConcurrentModificationException` 或无声的腐蚀，在任何锁类持有之外。

返回 `List.copyOf(items)`（快照）或 `Collections.unmodifiableList(items)`（活的只读视图 — 选择副本如果调用者可能在你改变时迭代）。封装不是字段被 `private`；它是**没有到可变内部的外部引用**。
