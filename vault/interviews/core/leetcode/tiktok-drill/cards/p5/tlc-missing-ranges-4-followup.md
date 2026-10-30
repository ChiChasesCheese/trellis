---
id: tlc-missing-ranges-4-followup
node: p5.missing-ranges
type: qa
step: 4
---
## Q
**LC 163 缺失的区间**｜追问

面试官接着问：（1）输出改成字符串，缺一个数写 `"2"`，缺多个写 `"4->49"`？（2）`nums` 大到读不进内存，只能边读边处理？（3）`nums` 里可能有重复数字？分别怎么改。

## A
1. **字符串输出**：只改写入的一行。`a, b = prev + 1, x - 1`，`ans.append(str(a) if a == b else f"{a}->{b}")`。判断条件和扫描逻辑不变。
2. **流式输入**：算法只依赖一个变量 `prev`，所以把参数换成任意可迭代对象即可，例如 `for x in chain(stream, (upper + 1,))`；空间仍是 `O(1)`，不需要整个数组。前提是输入已经有序。
3. **有重复**：重复值与 `prev` 的差为 `0`，`0 >= 2` 不成立，不产生区间，`prev` 照常更新，代码不用改。如果输入还没排好序，先 `sorted(set(nums))`，再套同一段扫描，时间变成 `O(n log n)`。

**Python 提醒**：不要写 `nums.append(upper + 1)` 来加哨兵，它会改动调用者传进来的列表；`nums + [upper + 1]` 则复制整个列表。`chain` 既不改原列表也不复制。
