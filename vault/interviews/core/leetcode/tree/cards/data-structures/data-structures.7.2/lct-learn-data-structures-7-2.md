---
id: lct-learn-data-structures-7-2
node: data-structures.7.2
type: qa
step: 1
---
## Q
**常用数据结构 › 并查集 › 进阶**｜学习卡

套路是什么？

## A
**一句话。** 进阶并查集的难点在建模：把条件翻译成点和连边（格子拆成小块、置换位置连环、虚拟点），必要时按权值排序合并或倒序把删除变成加入，让只能合并的并查集回答连通性。

下图：难点在把条件翻译成点和边；建好图后并查集本身不变。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 225">
<polygon points="114.0,20.0 123.0,7.5 217.0,7.5 226.0,20.0 217.0,32.5 123.0,32.5" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170" y="24.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">题目条件是什么？</text>
<rect x="17.6" y="57.0" width="84.9" height="70" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="60" y="73.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">相邻 / 相等</text>
<text x="60" y="88.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">位置该去哪</text>
<text x="60" y="103.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">直接连边</text>
<text x="60" y="118.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">可加虚拟点</text>
<rect x="132.0" y="64.5" width="76" height="55" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170" y="81.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">按阈值放宽</text>
<text x="170" y="96.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">边按权排序</text>
<text x="170" y="111.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">依次合并</text>
<rect x="242.0" y="64.5" width="76" height="55" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="280" y="81.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">只删不加</text>
<text x="280" y="96.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">倒序处理</text>
<text x="280" y="111.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">删除变加入</text>
<rect x="76.7" y="170.0" width="186.6" height="40" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="170" y="186.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">find 判连通 / cc 数块数</text>
<text x="170" y="201.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">如置换环：交换次数 = n - cc</text>
<path d="M 114.0 20.0 L 60.0 20.0 L 60.0 57.0" fill="none" stroke-width="1.2" stroke="currentColor"/>
<polygon points="60.0,57.0 57.0,50.7 63.0,50.7" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<path d="M 170.0 32.5 L 170.0 64.5" fill="none" stroke-width="1.2" stroke="currentColor"/>
<polygon points="170.0,64.5 167.0,58.2 173.0,58.2" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<path d="M 226.0 20.0 L 280.0 20.0 L 280.0 64.5" fill="none" stroke-width="1.2" stroke="currentColor"/>
<polygon points="280.0,64.5 277.0,58.2 283.0,58.2" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<path d="M 60.0 127.0 L 60.0 150.0 L 110.0 150.0 L 110.0 174.0" fill="none" stroke-width="1.2" stroke="currentColor"/>
<polygon points="110.0,174.0 107.0,167.7 113.0,167.7" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<path d="M 170.0 119.5 L 170.0 174.0" fill="none" stroke-width="1.2" stroke="currentColor"/>
<polygon points="170.0,174.0 167.0,167.7 173.0,167.7" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<path d="M 280.0 119.5 L 280.0 150.0 L 230.0 150.0 L 230.0 174.0" fill="none" stroke-width="1.2" stroke="currentColor"/>
<polygon points="230.0,174.0 227.0,167.7 233.0,167.7" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
</svg>

```python
class UnionFind:
    def __init__(self, n):
        self.fa, self.cc = list(range(n)), n   # cc：连通块数
    def find(self, x):
        if self.fa[x] != x:
            self.fa[x] = self.find(self.fa[x])
        return self.fa[x]
    def merge(self, a, b):
        x, y = self.find(a), self.find(b)
        if x != y:
            self.fa[x] = y
            self.cc -= 1
def min_swaps(nums):                 # LC 3551：置换环 = 连通块
    n = len(nums)
    key = lambda i: (sum(map(int, str(nums[i]))), nums[i])
    order = sorted(range(n), key=key)    # 排序后第 k 位的原下标
    uf = UnionFind(n)
    for k, i in enumerate(order):
        uf.merge(i, k)               # 位置 i 的元素该去 k：同一个环
    return n - uf.cc                 # 长 L 的环要 L - 1 次交换
```

**要点。**
- 为什么置换环答案是 `n - cc`？：每个位置一条出边一条入边，分解成不相交的环（就位的是自环）；长 `L` 的环 `L - 1` 次交换排好，每次交换至多让环数加一，终态 `n` 个自环，故至少 `n - cc` 次。
- LC 959 怎么建模？：一格拆成上 `0`、右 `1`、下 `2`、左 `3` 四块，下标 `b = 4 * (i * n + j)`；`/` 合并 `(b, b+3)(b+1, b+2)`，`\` 合并 `(b, b+1)(b+2, b+3)`，空格四块全合并；再合并右块与右邻格的左块 `(b+1, b+7)`、下块与下邻格的上块 `(b+2, b+4n)`；区域数就是 `cc`。
- 阈值类（LC 778 等）怎么做？：连通性对阈值单调，格子按高度排序依次「开放」，只与已开放的邻格合并，第一次起点终点连通的高度就是答案，和 Kruskal 同一思路；要「删除」就倒序加入。

**易错点。**
- LC 959 斜杠规则对调：`[" /", "/ "]` 应得 `2`，对调后得 `3`；漏掉与邻格的合并：`[" /", "  "]` 应得 `1`。Python 里反斜杠要写 `"\\"`。
- LC 3551 排序键漏掉数值作第二关键字：`[18,43,34,16]` 应得 `2`，漏了得 `3`。
- LC 778 合并邻格不检查 `grid[x][y] <= t`：`[[0,2],[1,3]]` 应得 `3`，漏检查得 `1`。

**对应题目。** LC 3551 数位和排序需要的最小交换次数、LC 959 由斜杠划分区域
