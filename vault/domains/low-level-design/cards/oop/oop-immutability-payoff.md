---
id: oop-immutability-payoff
node: oop.values
type: qa
---
## Q
说出把一个类型改成不可变之后，能被消灭掉的三类具体 bug。

## A
- **别名（aliasing）bug**：实例可以自由共享和返回 —— 不需要防御性拷贝。
- **被破坏的集合**：可以安全地做 `HashMap`/`HashSet` 的 key，因为插入之后 `hashCode` 不可能漂移。
- **数据竞争**：跨线程只读共享，不需要任何同步。

"修改"变成 `money.plus(x)` 返回一个新实例 —— 每条不变量只在构造函数里检查一次。
