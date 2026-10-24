---
id: tlc-insert-delete-getrandom-o1-3-why
node: b.insert-delete-getrandom-o1
type: qa
step: 3
---
## Q
**LC 380 O(1) 时间插入、删除和获取随机元素**｜正确性

`items` 与 `pos` 之间保持什么不变量？为什么删除时用末尾元素补位不会破坏 `getRandom` 的等概率？删除正好是末尾元素时，哪一种写法会出错？

## A
**不变量。** 任何时刻：`items` 里没有重复值；`pos` 的键集合恰好等于 `items` 的元素集合；对每个值 `v`，`items[pos[v]] == v`。三条同时成立，两个结构才是同一个集合的两种视图。

**为什么补位不破坏等概率。** `getRandom` 用 `random.choice(items)`，在 `len(items)` 个位置上均匀选，每个位置恰好对应一个不同的元素。补位只是改变了元素在数组里的位置，没有增加或减少元素，每个元素仍然占一个位置，概率仍然是 `1/n`；集合本来就不要求顺序。

**为什么要弹出末尾后才判断。** 先 `last = items.pop()`，数组长度减一；如果被删元素原来的下标 `i` 等于新的长度，说明它就是刚弹出的末尾，已经删完了，不需要再补位。

**反例：无条件补位。** 去掉 `if i < len(self.items)` 判断，直接 `self.items[i] = last; self.pos[last] = i`：
- `insert(1)`、`insert(2)`，数组 `[1, 2]`；`remove(2)`：`i = 1`，`last = 2`，弹出后数组是 `[1]`，再执行 `self.items[1] = 2` 抛 `IndexError: list assignment index out of range`。
- `insert(1)`、`insert(2)`、`remove(1)`：`i = 0`，`last = 2`，弹出后 `[1]`，补位得到 `[2]`，`pos = {2: 0}`，这条是对的；只有「删除末尾」才暴露问题，所以要专门测试。
