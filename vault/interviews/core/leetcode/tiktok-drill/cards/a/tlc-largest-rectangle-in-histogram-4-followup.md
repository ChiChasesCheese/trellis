---
id: tlc-largest-rectangle-in-histogram-4-followup
node: a.largest-rectangle-in-histogram
type: qa
step: 4
---
## Q
**LC 84 柱状图中最大的矩形**｜追问

面试官接着问：（1）在 `0/1` 矩阵里找面积最大的全 `1` 矩形（LC 85）；（2）除了面积，还要返回矩形的位置；（3）数据是流式的，一根一根到来，能边读边给出当前最大面积吗？

## A
1. **最大全 1 矩形**：逐行维护 `h[c]` = 以当前行为底、第 `c` 列向上连续 `1` 的个数，每行把 `h` 当柱状图再算一次面积，总时间 `O(m·n)`。更新一行的写法：
```python
def update_heights(h: list[int], row: str) -> list[int]:
    return [(old + 1) if cell == "1" else 0 for old, cell in zip(h, row)]
```
`update_heights([0,0,0], "101")` → `[1,0,1]`，再喂 `"111"` → `[2,1,2]`，喂 `"010"` → `[0,1,0]`。`zip` 把上一行的高度和当前行逐列配对。
2. **返回位置**：更新 `best` 时同时记录 `(left + 1, i - 1, height)`，即列范围和高度。注意元组比较要按面积，不要直接 `max` 元组。
3. **流式**：栈本身就能增量维护，每到一根新柱子做一次弹出结算，已弹出的面积累积进 `best`；栈里尚未结算的柱子还不知道右边界。要查询当前答案时，把它们当作在末尾结束，各算一次 `高 × (n - left - 1)`，`O(栈大小)`。

**Python 提醒**：`max(best, height * width)` 里 `height * width` 的结果是 Python 整数，不会溢出；Java / C++ 里 `10^5 × 10^4 = 10^9` 接近 `int` 上限，要用 `long`。
