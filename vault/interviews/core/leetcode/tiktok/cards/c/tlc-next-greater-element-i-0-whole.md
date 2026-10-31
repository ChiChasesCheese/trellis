---
id: tlc-next-greater-element-i-0-whole
node: c.next-greater-element-i
type: qa
---
## Q
**LC 496 下一个更大元素 I**｜Easy · LC TikTok 全时段热度 26/100 · CodeTop 国内累计 2 次 · 最近 2025-09-16（国内 CodeTop）

`nums1` 中数字 `x` 的**下一个更大元素**，是指 `x` 在 `nums2` 中对应位置**右侧**的第一个比 `x` 大的元素。给你两个没有重复元素的数组 `nums1` 和 `nums2`，`nums1` 是 `nums2` 的子集。对每个 `nums1[i]`，找出它在 `nums2` 中的下一个更大元素，不存在则为 `-1`，返回长度为 `nums1.length` 的数组。`1 <= nums1.length <= nums2.length <= 1000`，`0 <= nums1[i], nums2[i] <= 10^4`，`nums1` 和 `nums2` 中所有整数互不相同。例：`nums1 = [4,1,2], nums2 = [1,3,4,2]` → `[-1,3,-1]`；`nums1 = [2,4], nums2 = [1,2,3,4]` → `[3,-1]`。进阶：能否设计 `O(nums1.length + nums2.length)` 的解法？

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 对 `nums2` 做一趟单调栈（栈内递减），每个元素被弹出时遇到的当前数就是它的下一个更大元素，存进字典，再按 `nums1` 查表，`O(m + n)`。

**识别。** 「每个元素右边第一个比它大的」是单调栈的原型题；「`nums1` 是子集、值不重复」让字典查询成立。

**推导。** 暴力：对 `nums1` 的每个数在 `nums2` 里找到位置，再向右扫描，`O(mn)`。浪费：对 `nums2` 里每个数的「下一个更大元素」被重复求了。一趟扫描把它们全部算出：栈里放还没找到答案的数（自底向上递减），新来的数 `x` 比栈顶大，说明 `x` 就是栈顶的答案，弹出记录，直到栈顶不小于 `x`，再把 `x` 入栈。

```python
def next_greater_element(nums1: list[int], nums2: list[int]) -> list[int]:
    nxt: dict[int, int] = {}                     # nums2 中每个数 -> 它的下一个更大元素
    stack: list[int] = []                        # 还没找到答案的数，自底向上递减
    for x in nums2:
        while stack and stack[-1] < x:
            nxt[stack.pop()] = x                 # x 是栈顶右边第一个比它大的
        stack.append(x)
    return [nxt.get(x, -1) for x in nums1]       # 栈里剩下的没有答案，默认 -1
```

运行：`([4,1,2], [1,3,4,2])` → `[-1,3,-1]`，`([2,4], [1,2,3,4])` → `[3,-1]`；`([3,2], [3,2,1,4])` → `[4,4]`，`([5], [5])` → `[-1]`。

**复杂度。** 时间 `O(m + n)`，每个数入栈、出栈各一次；空间 `O(n)`。

**拓展优化。**
- 从右往左扫：栈里放右边「还可能成为答案」的数，当前数直接读栈顶，不需要先存字典再查（仍要字典，因为 `nums1` 按值查）。

```python
def next_greater_element_reverse(nums1: list[int], nums2: list[int]) -> list[int]:
    nxt: dict[int, int] = {}
    stack: list[int] = []
    for x in reversed(nums2):
        while stack and stack[-1] < x:
            stack.pop()                          # 比 x 小的数被 x 挡住，对左边的数已无用
        nxt[x] = stack[-1] if stack else -1      # 剩下的栈顶就是右边第一个更大的
        stack.append(x)
    return [nxt[x] for x in nums1]
```

**易错点。**
- 把 `while` 写成 `if`：只弹一个，`([3,2], [3,2,1,4])` 得到 `[-1,-1]`，正确是 `[4,4]`。
- 字典里取不到时报 `KeyError`：栈里剩下的数没有答案，要用 `nxt.get(x, -1)`。
- 栈里存下标但用值查字典：要么存值（元素互不相同），要么存下标并统一用下标取值，别混用。

**追问。**
- 循环数组（LC 503）：把数组遍历两遍（下标取模），第二遍只弹栈不入栈。
- 有重复元素：字典不能按值存，要存下标，答案数组按下标填写。

**同模式。** LC 503 下一个更大元素 II、LC 739 每日温度、LC 901 股票价格跨度、LC 84 柱状图中最大的矩形、LC 1019 链表中的下一个更大节点。
