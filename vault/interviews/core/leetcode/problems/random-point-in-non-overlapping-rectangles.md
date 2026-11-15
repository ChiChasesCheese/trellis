---
slug: random-point-in-non-overlapping-rectangles
---
## Q
**LC 497 非重叠矩形中的随机点**｜Medium

给若干互不重叠的轴对齐矩形，每个由左下角和右上角的整点 `[a, b, x, y]` 给出（边界上的整点也算）。设计 `pick()`：在所有矩形覆盖的整点中等概率随机返回一个。

## A
**一句话。** 先按整点数给矩形加权，用前缀和加二分选出矩形，再在矩形里均匀选点，整体就是均匀的。

```python
class Solution:
    def __init__(self, rects):
        self.rects = rects
        self.pre, tot = [], 0           # 整点数的前缀和
        for a, b, x, y in rects:
            tot += (x - a + 1) * (y - b + 1)
            self.pre.append(tot)

    def pick(self):
        k = random.randint(1, self.pre[-1])   # 第 k 个整点
        i = bisect_left(self.pre, k)          # 它落在哪个矩形
        a, b, x, y = self.rects[i]
        return [random.randint(a, x), random.randint(b, y)]
```

**复杂度。** 时间 `pick` 为 `O(log n)`，预处理 `O(n)`，空间 `O(n)`。

**易错点。**
- 先等概率选矩形再选点：大矩形里的点概率变小，要按整点数加权。
- 面积写成 `(x-a)*(y-b)`：边界整点也算，宽高各要加一。
- 用 `bisect_right`：`k` 恰等于某个前缀和时会落到下一个矩形。

**追问。**
- 为什么这样是均匀的？：选中矩形的概率是 `点数/总点数`，矩形内每个点概率 `1/点数`，乘起来每个点都是 `1/总点数`。
- 矩形有重叠就不行了？：会重复计数，要先把区域切成互不重叠的块或做拒绝采样。

**同模式。** LC 528 按权重随机选择、LC 478 在圆内随机生成点、LC 398 随机数索引、LC 382 链表随机节点
