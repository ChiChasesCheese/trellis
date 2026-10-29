---
id: tlc-squares-of-a-sorted-array-4-followup
node: b.squares-of-a-sorted-array
type: qa
step: 4
---
## Q
**LC 977 有序数组的平方**｜追问

面试官接着问：（1）如果输入**没有**排好序？（2）把「平方」换成二次函数 `a*x*x + b*x + c`（LC 360）？（3）结果不想一次性放进内存，要惰性产出？分别怎么改。

## A
1. **未排序**：没有「山谷」结构可用，只能 `sorted(x * x for x in nums)`，`O(n log n)`。基于比较的排序下界是 `Ω(n log n)`，进阶的 `O(n)` 完全来自输入有序。
2. **二次函数**：抛物线 `f` 的对称轴把 `nums` 分成单调的两段，最值仍在两端。`a >= 0` 开口向上，两端大、中间小，和平方一样从后往前取较大；`a < 0` 开口向下，两端小、中间大，从前往后取较小：

```python
def sort_transformed_array(nums: list[int], a: int, b: int, c: int) -> list[int]:
    def f(x: int) -> int:
        return a * x * x + b * x + c

    n = len(nums)
    result = [0] * n
    left, right = 0, n - 1
    if a >= 0:
        for pos in range(n - 1, -1, -1):
            if f(nums[left]) > f(nums[right]):
                result[pos] = f(nums[left]); left += 1
            else:
                result[pos] = f(nums[right]); right -= 1
    else:
        for pos in range(n):
            if f(nums[left]) < f(nums[right]):
                result[pos] = f(nums[left]); left += 1
            else:
                result[pos] = f(nums[right]); right -= 1
    return result
```

3. **惰性输出**：先 `k = bisect_left(nums, 0)` 找到分界，负半边用 `reversed(nums[:k])` 取平方，非负半边取平方，交给 `heapq.merge` 做两路归并；它返回迭代器，一次只产出一个元素。

**Python 提醒**：`sorted(x * x for x in nums)` 在这个输入上其实也很快，因为 Timsort 会识别「先降后升」的两段已有序序列并只做一次归并，但这是实现细节，面试里要说的仍是双指针的 `O(n)`。
