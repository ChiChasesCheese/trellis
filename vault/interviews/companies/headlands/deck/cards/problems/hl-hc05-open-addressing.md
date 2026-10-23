---
id: hl-hc05-open-addressing
node: problems.hc05-market-order-book
type: qa
step: 15
---
## Q
开放寻址（open addressing）哈希表怎么按 id 查找和删除？为什么删除不能直接置 0，回移删除（backward shift）怎么做，比墓碑好在哪？

## A
自己用 `long[] keys`、`int[] vals`，冲突就往后一格找（线性探测），不装箱。`hash(id)` 乘黄金比例常数再折叠高位，打散连续 id；`find` 线性往后找，遇空槽（`keys[i] == 0`，所以 `id` 必须 > 0）即「没有」。

**删除最微妙**：直接置 0 会「切断」后面因冲突被挤后的 key 的探测链，`find` 找不到它们。

**回移删除**：把后面能挪的元素挪回空洞，不留墓碑。元素 j（理想位置 k）能挪到空洞 i 当且仅当 `((j - k) & mask) >= ((j - i) & mask)`，即 k 不在环形区间 (i, j] 内。

**对比墓碑**（tombstone）：墓碑会占用探测链，需要定期 rehash 清理，装载因子要把墓碑算进去；回移删除不留墓碑，探测链不会越来越长，代价是删除代码更复杂。

**`MAX_QTY = 2⁴⁰`、`capacity ≤ 2²²`**：价位总量最坏 2⁶² < 2⁶³，永不溢出 `long`，热路径不需要 `addExact`——「用输入上限换掉运行时检查」。`limit` 对 `qty ∉ 1..MAX_QTY` 返回 `REJECTED`。

C++ 补充：`TickBook::limit` 要先检查 `price >= max_ticks_` 再 `static_cast<int>`——`static_cast<int>(2³² + 5)` 是 5，本该拒绝的价格会变合法；所有范围检查在 64 位上做，通过后再收窄。回调用模板参数（任何可调用对象，内联），不用 `std::function`。
