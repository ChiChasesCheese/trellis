---
id: storage-rolling-upgrade-compat
node: storage.encoding
type: qa
---
## Q
Why does a rolling deploy force you to maintain *both* backward and forward compatibility at once — and why does data in a database raise the bar further?

## A
During the rollout old and new instances run side by side, and messages/RPCs flow both ways: new code reads what old code wrote (**backward**), and old code reads what new code wrote (**forward**). Break either and you can only deploy with downtime — and rollback breaks too.

Databases are stricter because **data outlives code**: a row written five years ago is still read by today's code (backward compat across *years* of schema versions), and after adding a column, old rows simply lack it — readers must handle the default, since rewriting the whole dataset is usually prohibitive.

## Q zh
为什么滚动部署强制你同时维护向后**和**向前兼容——为什么数据库中的数据进一步提高了标准？

## A zh
在推出期间旧和新实例并排运行，消息/RPC 双向流动：新代码读旧代码写的（**向后**），旧代码读新代码写的（**向前**）。打破任何一个，你只能以停机部署——回滚也破裂。

数据库更严格因为**数据超越代码**：五年前写的行仍被今天的代码读（跨**多年** schema 版本的向后兼容），加列后，旧行简单地缺乏它——读端必须处理默认值，因为重写整个数据集通常禁止。
