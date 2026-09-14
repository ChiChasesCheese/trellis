---
id: cc-toolbox-graph-implicit-edges
node: toolbox.graph-repr
type: qa
---
## Q
10^5 accounts each carry a device id; accounts sharing a device are connected. Building the edge list explicitly is 10^10 edges. What do you build instead?

## A
**A bipartite graph through the shared attribute, instead of the clique it implies.** Make the attribute value a node and connect each record to it: *n* records sharing a device become *n* edges, not `n(n−1)/2`.

- Traversal through such a node reaches every record that shares the value — same reachability, linear size.
- If the attribute must not appear in the output, keep a `value -> first record seen` map and add one edge from each later record to that first one: same components, `n − 1` edges, nothing to filter out ([[cc-toolbox-union-find-shared-key-edges]]).
- The same collapse works for "same hour", "same merchant", "same prefix" — any cue phrased as "share an attribute" is a clique waiting to blow up.
- Type the attribute node by field so the same value in two different fields does not merge two groups ([[cc-toolbox-hash-tuple-keys]]).

## Q zh
10^5 个账户各带一个设备 id；共享设备的账户相连。显式构造边列表是 10^10 条边。那该构造什么？

## A zh
**用共享属性做成二分图，而不是它隐含的团。** 把属性值当成节点，把每条记录连到它上面：共享同一设备的 *n* 条记录变成 *n* 条边，而不是 `n(n−1)/2`。

- 经由这样的节点做遍历能到达所有共享该值的记录 —— 可达性相同，规模线性。
- 如果这个属性不能出现在输出里，就维护 `值 -> 首次见到的记录` 映射，让之后的每条记录只连一条边到那条首记录：连通块相同，边只有 `n − 1` 条，也没有东西要过滤（[[cc-toolbox-union-find-shared-key-edges]]）。
- 同样的坍缩适用于「同一小时」「同一商户」「同一前缀」—— 任何以「共享某属性」表述的线索都是一个随时会爆炸的团。
- 属性节点要按字段带类型，这样同一个值出现在两个不同字段时不会把两个群合并（[[cc-toolbox-hash-tuple-keys]]）。
