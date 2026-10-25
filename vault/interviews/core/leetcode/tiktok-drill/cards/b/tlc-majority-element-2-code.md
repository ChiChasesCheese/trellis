---
id: tlc-majority-element-2-code
node: b.majority-element
type: qa
step: 2
---
## Q
**LC 169 多数元素**｜写出 Python 实现

`nums` 长度为 `n`（`1` 到 `5 * 10^4`），值在 `[-10^9, 10^9]`，保证存在出现次数大于 `⌊n/2⌋` 的元素。返回它，要求 `O(n)` 时间、`O(1)` 空间。

## A
**思路。** 候选人 `candidate` 与计数 `count`。扫描每个元素：如果计数已经是 `0`，把当前元素设为候选人；然后相同加一、不同减一。扫描结束时候选人就是多数元素。

```python
def majority_element(nums: list[int]) -> int:
    candidate, count = nums[0], 0
    for x in nums:
        if count == 0:                     # 票数抵消光了：换一个新候选人
            candidate = x
        count += 1 if x == candidate else -1
    return candidate
```

运行：`[3,2,3]` → `3`，`[2,2,1,1,1,2,2]` → `2`，`[5]` → `5`；`25001` 个 `1` 与 `24999` 个 `2` 打乱后 → `1`。

**复杂度。** 时间 `O(n)`，一次扫描；空间 `O(1)`，两个变量。

**写法要点。** `count += 1 if x == candidate else -1` 把"同则加、异则减"写成一个表达式；换人和计数写在同一轮里——换成新候选人之后 `x == candidate` 成立，自然加一；`candidate` 的初值无关紧要，写 `nums[0]` 只是让类型检查满意；`Counter(nums).most_common(1)[0][0]` 更短，但用的是 `O(n)` 空间，不满足进阶。
