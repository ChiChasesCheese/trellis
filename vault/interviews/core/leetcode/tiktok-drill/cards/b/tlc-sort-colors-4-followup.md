---
id: tlc-sort-colors-4-followup
node: b.sort-colors
type: qa
step: 4
---
## Q
**LC 75 颜色分类**｜追问

面试官接着问：（1）两趟的计数排序怎么写，什么时候用它？（2）颜色有 `k` 种怎么办？（3）要求稳定怎么办？

## A
1. **计数排序**：数出每种颜色的个数，再用切片赋值按顺序写回。扫两遍但逻辑最简单，不容易出错，是不要求一趟时的稳妥选择：

```python
def sort_colors_count(nums: list[int]) -> None:
    counts = [0, 0, 0]
    for x in nums:
        counts[x] += 1
    i = 0
    for color, k in enumerate(counts):
        nums[i:i + k] = [color] * k            # 切片赋值，长度相同，原地改写
        i += k
```

2. **`k` 种颜色**：计数排序推广，`counts` 长度 `k`，`O(n + k)` 时间；若 `k` 很大且要求原地，可以对每种颜色做一轮三路划分，`O(nk)`，或者用 `O(n log n)` 的原地排序。
3. **稳定**：三指针交换会打乱相同颜色的相对顺序。颜色只是整数时无所谓；如果元素是带颜色标签的对象，需要稳定就分三个列表按出现顺序收集，再拼接，代价是 `O(n)` 额外空间。

**Python 提醒**：切片赋值 `nums[i:i + k] = [color] * k` 在右侧长度与切片长度相同时是原地覆盖；长度不同会改变列表长度，容易出 bug。`counts[x] += 1` 要求 `x` 在 `0..2`，输入保证这点。
