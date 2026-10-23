---
id: hl-hc08-two-trees-holes
node: problems.hc08-order-sequence-api
type: qa
step: 5
---
## Q
订单序列怎么用 Fenwick 实现？为什么要「下标只增不减、删除留洞」，为什么要两棵树 `cnt` 和 `sum`？

## A
**留洞**：put 时领递增的「插入下标」`nextIndex++`，永不变；删除只把 `qtyByIdx[i]` 改成 0，不挪动后面的订单。删除时往前挪会改变所有后续下标、破坏 `indexOf`，且 Fenwick 要重建；留洞只需把该下标值改 0。订单先后 = 下标先后，所以「队头到 X」= 下标 1..idx(X)。洞在两棵树里都是 0，不影响前缀和。

**两棵独立的树**：
- `sum[]`（long）按下标累加**数量** → `qtyUpTo(id) = prefixSum(indexOf(id))`；
- `cnt[]`（int）每张**活跃**订单在自己下标记 1 → `countUpTo(id) = prefixCnt(indexOf(id))`，也用来找第 k 张。
部分删除时订单还活着（count 不变）、数量减少，所以必须两棵树，不能共用。

操作：
- `put`：新下标 i，`addCnt(i, +1)`、`addSum(i, qty)`、`indexOf.put(id, i)`；
- 整单 `delete`：`addCnt(i, -1)`、`addSum(i, -qty)`，`indexOf.remove(id)`；
- **部分删除**：`addSum(i, -qty)`、`qtyByIdx[i] -= qty`，`cnt` **不动**；剩余为 0 才 `addCnt(i,-1)`。

状态：`capacity`（2 的幂）、`int[] cnt`、`long[] sum`、`long[] idByIdx`、`long[] qtyByIdx`（0 = 洞，`qtyByIdx[i] > 0` 当且仅当活跃）、`nextIndex = 1`、`HashMap<Long,Integer> indexOf`、`totalQty`。全部操作 O(log C)。

`HashMap<Long,Integer>` 把任意 `long` id 换成下标，平均 O(1)；装箱是可接受的简化（热路径要避免）。Fenwick 按插入下标建，不依赖 id 取值范围，不需要离散化。
