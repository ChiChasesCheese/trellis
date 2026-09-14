---
id: oop-immutability-payoff
node: oop.values
type: qa
---
## Q
Name three concrete bug classes that making a type immutable eliminates.

## A
- **Aliasing bugs**: instances can be shared and returned freely — no defensive copies.
- **Corrupted collections**: safe as `HashMap`/`HashSet` keys, since `hashCode` cannot drift after insertion.
- **Data races**: read-only sharing across threads needs no synchronization.

"Mutation" becomes `money.plus(x)` returning a new instance — every invariant is checked once, in the constructor.

## Q zh
说出把一个类型改成不可变之后，能被消灭掉的三类具体 bug。

## A zh
- **别名（aliasing）bug**：实例可以自由共享和返回 —— 不需要防御性拷贝。
- **被破坏的集合**：可以安全地做 `HashMap`/`HashSet` 的 key，因为插入之后 `hashCode` 不可能漂移。
- **数据竞争**：跨线程只读共享，不需要任何同步。

"修改"变成 `money.plus(x)` 返回一个新实例 —— 每条不变量只在构造函数里检查一次。
