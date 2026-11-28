---
id: lct-learn-list-tree-backtracking-4-1
node: list-tree-backtracking.4.1
type: qa
step: 1
---
## Q
**链表、二叉树与回溯 › 回溯 › 子集型回溯**｜学习卡

套路是什么？

## A
**一句话。** 回溯是搜索树上的 DFS：共享一个 `path`，进分支时加元素，回来时撤销；子集型有两个等价视角，输入视角对每个元素「选或不选」，答案视角枚举「下一个选哪个」且只往后选，每个子集恰好出现一次。

下图：答案视角（`dfs_b`）的搜索树，nums = [1,2,3]；每个节点都记一次答案，只往后选所以不重复。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 182">
<line x1="157.8" y1="28.8" x2="92.2" y2="65.2" stroke-width="1.2" stroke="currentColor"/>
<line x1="175.2" y1="35.0" x2="184.8" y2="59.0" stroke-width="1.2" stroke="currentColor"/>
<line x1="182.7" y1="27.8" x2="267.3" y2="66.2" stroke-width="1.2" stroke="currentColor"/>
<line x1="72.8" y1="84.0" x2="57.2" y2="110.0" stroke-width="1.2" stroke="currentColor"/>
<line x1="87.2" y1="84.0" x2="102.8" y2="110.0" stroke-width="1.2" stroke="currentColor"/>
<line x1="190.0" y1="86.0" x2="190.0" y2="108.0" stroke-width="1.2" stroke="currentColor"/>
<line x1="50.0" y1="136.0" x2="50.0" y2="148.0" stroke-width="1.2" stroke="currentColor"/>
<circle cx="170" cy="22" r="14" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="170" y="26" text-anchor="middle" font-size="10" font-family="sans-serif" fill="currentColor">{}</text>
<circle cx="80" cy="72" r="14" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="80" y="76" text-anchor="middle" font-size="10" font-family="sans-serif" fill="currentColor">1</text>
<circle cx="190" cy="72" r="14" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="190" y="76" text-anchor="middle" font-size="10" font-family="sans-serif" fill="currentColor">2</text>
<circle cx="280" cy="72" r="14" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="280" y="76" text-anchor="middle" font-size="10" font-family="sans-serif" fill="currentColor">3</text>
<circle cx="50" cy="122" r="14" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="50" y="126" text-anchor="middle" font-size="10" font-family="sans-serif" fill="currentColor">12</text>
<circle cx="110" cy="122" r="14" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="110" y="126" text-anchor="middle" font-size="10" font-family="sans-serif" fill="currentColor">13</text>
<circle cx="190" cy="122" r="14" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="190" y="126" text-anchor="middle" font-size="10" font-family="sans-serif" fill="currentColor">23</text>
<circle cx="50" cy="162" r="14" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="50" y="166" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">123</text>
<text x="235" y="120" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">只往后选</text>
<text x="235" y="136" text-anchor="start" font-size="11" font-family="sans-serif" fill="currentColor">每个节点 = 一个子集</text>
<text x="235" y="152" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">共 2³ = 8 个</text>
</svg>

```python
def subsets(nums):                   # LC 78
    ans, path = [], []
    def dfs_a(i):                    # 写法一：选或不选
        if i == len(nums):
            ans.append(path[:])      # 叶子是一个子集；要拷贝
            return
        dfs_a(i + 1)                 # 不选
        path.append(nums[i])         # 选
        dfs_a(i + 1)
        path.pop()                   # 恢复现场
    def dfs_b(i):                    # 写法二：枚举选哪个
        ans.append(path[:])          # 每个节点都是一个子集
        for j in range(i, len(nums)):
            path.append(nums[j])
            dfs_b(j + 1)             # 只往后选：不重复
            path.pop()
    dfs_b(0)                         # 换成 dfs_a(0) 结果相同
    return ans
```

**要点。**
- 为什么对？：写法一的搜索树深度 `n`，根到叶子的路径唯一对应一个子集；写法二把写法一里「连续若干个不选」折叠成 `for` 循环，下标递增的挑选顺序固定，所以不重不漏；`path` 是共享对象，所以收集要拷贝、离开要恢复。
- LC 39 怎么改？：答案视角，递归传 `j` 而不是 `j + 1`（同一个数可再选），循环从 `i` 起（不出现顺序不同的重复），先排序，`candidates[j] > left` 就 `break`，`left == 0` 时收集。
- LC 784 怎么改？：输入视角，每个字母「原样 / `swapcase`」二选一，数字只有一种，翻转后要翻回来。
- LC 1239 怎么改？：状态是字母掩码，选串前检查 `used & m == 0`，每个节点更新最大长度；自身有重复字母的串要先剔除。

**易错点。**
- 收集时不拷贝：`[1,2]` 应得 `[[],[1],[2],[1,2]]`，`ans.append(path)` 得到四个空列表。
- LC 39 传 `j + 1`：`[2,3,6,7]`、`target = 7` 应得 `[[2,2,3],[7]]`，会得 `[[7]]`；没排序就 `break`：`[3,2]`、`target = 2` 会漏掉 `[2]`。
- LC 1239 不剔除自带重复字母的串：`["aa","bb"]` 应得 `0`。

**对应题目。** LC 39 组合总和、LC 784 字母大小写全排列、LC 1239 串联字符串的最大长度、LC 78 子集
