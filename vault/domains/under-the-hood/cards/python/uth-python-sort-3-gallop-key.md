---
id: uth-python-sort-3-gallop-key
node: python.sort
type: qa
step: 3
---
## Q
**归并时的 galloping 与 key 函数**｜Python · CPython 3.14

两段各 10 万的有序数据，后一段全比前一段小，归并要比较 20 万次吗？`sorted(a, key=f)` 里 `f` 被调用几次？

## A
**结构。** 归并时一边连续赢 `MIN_GALLOP = 7` 次，就切到 galloping 模式：用指数加二分查找（跳 1、3、7、15…）找边界，再整块拷贝。

**细节。**

- 实测总比较数 200042，一个 20 万有序段是 199999，只多 43 次。
- `key` 对每个元素只调用一次（1000 个元素调用 1000 次）。
- 排序稳定：`sorted(data, key=lambda t: t[1])` 保持同键元素原来的先后。

**为什么。** 数据有大块结构时，逐个比较是浪费；稳定性让你能先按次要键、再按主键排两遍。

**对应 LeetCode：** LC 88 合并两个有序数组 · LC 4 寻找两个正序数组的中位数
