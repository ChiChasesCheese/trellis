---
id: tlc-maximum-height-by-stacking-cuboids-4-followup
node: p3.maximum-height-by-stacking-cuboids
type: qa
step: 4
---
## Q
**LC 1691 堆叠长方体的最大高度**｜追问

面试官接着问：（1）不只要最大高度，还要输出具体堆叠了哪些长方体、自底向上的顺序？（2）如果规定必须**严格**更小才能叠上去？（3）`n` 变成 `10^5` 怎么办？

## A
1. **输出方案**：多存一个 `prev[i]`，更新 `dp[i]` 时记下是从哪个 `j` 转移来的；最后取 `dp` 最大的 `i` 沿 `prev` 回溯，得到的顺序就是从底到顶。
```python
def max_height_path(cuboids: list[list[int]]) -> tuple[int, list[list[int]]]:
    boxes = sorted(sorted(c) for c in cuboids)
    dp = [b[2] for b in boxes]
    prev = [-1] * len(boxes)
    for i, box in enumerate(boxes):
        for j in range(i):
            if all(a <= b for a, b in zip(boxes[j], box)) and dp[j] + box[2] > dp[i]:
                dp[i], prev[i] = dp[j] + box[2], j
    i = max(range(len(boxes)), key=dp.__getitem__)
    best, path = dp[i], []
    while i != -1:
        path.append(boxes[i])
        i = prev[i]
    return best, path                                # path[0] 是最底下的箱子
```
示例 1 返回 `(190, [[37, 53, 95], [20, 45, 50], [12, 23, 45]])`（每个箱子是升序后的朝向，最后一个数是高）。
2. **严格小于**：把比较里的 `a <= b` 改成 `a < b`，朝向规范化和排序都不变（相等的箱子互相放不上去）。
3. **`n = 10^5`**：`O(n^2)` 不行。去掉第一维靠排序，剩下两维是二维偏序的最大权链：按第二维离散化，用树状数组（Fenwick tree）维护「第三维 `<= x` 的最大 `dp`」，这是 CDQ 分治加树状数组的 `O(n log^2 n)` 题型，面试里说出思路即可。

**Python 提醒**：`path.append(boxes[i])` 存的是引用，不是拷贝；若之后要修改路径里的箱子，先 `list(boxes[i])`。
