---
id: lct-learn-list-tree-backtracking-4-5
node: list-tree-backtracking.4.5
type: qa
step: 1
---
## Q
**链表、二叉树与回溯 › 回溯 › 有重复元素的回溯**｜学习卡

套路是什么？

## A
**一句话。** 输入有重复元素而答案要去重：先排序让相等元素相邻，再在搜索树的同一层只让相等元素里的第一个出现一次，更深一层相等元素仍可接着用，所以「选多个相同的数」不会丢。

下图：nums = [1,2,2] 排序后，同一层里第二个 2 被跳过；更深一层仍可接着选 2，所以 [1,2,2]、[2,2] 不丢。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 190">
<line x1="137.3" y1="27.9" x2="82.7" y2="62.1" stroke-width="1.2" stroke="currentColor"/>
<line x1="155.6" y1="33.9" x2="164.4" y2="56.1" stroke-width="1.2" stroke="currentColor"/>
<line x1="163.7" y1="26.2" x2="246.3" y2="63.8" stroke-width="1.2" style="stroke:var(--dim,#6b7280)" stroke-dasharray="4 3"/>
<line x1="62.3" y1="82.9" x2="47.7" y2="107.1" stroke-width="1.2" stroke="currentColor"/>
<line x1="79.4" y1="81.7" x2="100.6" y2="108.3" stroke-width="1.2" style="stroke:var(--dim,#6b7280)" stroke-dasharray="4 3"/>
<line x1="40.0" y1="135.0" x2="40.0" y2="150.0" stroke-width="1.2" stroke="currentColor"/>
<line x1="170.0" y1="85.0" x2="170.0" y2="105.0" stroke-width="1.2" stroke="currentColor"/>
<circle cx="150" cy="20" r="15" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="150" y="24" text-anchor="middle" font-size="10" font-family="sans-serif" fill="currentColor">{}</text>
<circle cx="70" cy="70" r="15" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="70" y="74" text-anchor="middle" font-size="10" font-family="sans-serif" fill="currentColor">1</text>
<circle cx="170" cy="70" r="15" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="170" y="74" text-anchor="middle" font-size="10" font-family="sans-serif" fill="currentColor">2</text>
<circle cx="260" cy="70" r="15" fill="none" style="stroke:var(--dim,#6b7280)" stroke-width="1.2"/>
<text x="260" y="74" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">2</text>
<circle cx="40" cy="120" r="15" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="40" y="124" text-anchor="middle" font-size="10" font-family="sans-serif" fill="currentColor">12</text>
<circle cx="110" cy="120" r="15" fill="none" style="stroke:var(--dim,#6b7280)" stroke-width="1.2"/>
<text x="110" y="124" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">12</text>
<circle cx="40" cy="165" r="15" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="40" y="169" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">122</text>
<circle cx="170" cy="120" r="15" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="170" y="124" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">22</text>
<text x="285" y="74" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">✗</text>
<text x="135" y="124" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">✗</text>
<text x="250" y="110" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">同一层相同的数</text>
<text x="250" y="126" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">只选第一个</text>
<text x="250" y="150" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">下一层仍可再选 2</text>
</svg>

```python
def subsets_with_dup(nums):          # LC 90
    nums = sorted(nums)              # 相同的数挨在一起
    ans, path = [], []
    def dfs(start):
        ans.append(path[:])          # 每个节点本身就是一个子集
        for i in range(start, len(nums)):
            if i > start and nums[i] == nums[i - 1]:
                continue             # 同一层里相同的数只选第一个
            path.append(nums[i])
            dfs(i + 1)               # 下一层可接着选相同的数
            path.pop()
    dfs(0)
    return ans
```

**要点。**
- 为什么是 `i > start` 而不是 `i > 0`？：重复的成因是相等元素里「选哪几个」本无区别；规定典范顺序，从一段相等元素里选 `c` 个就选最前面 `c` 个。`i == start` 是本层第一个选项没被试过，深一层的 `start = i + 1` 同理，所以连续选两个相同的数得以保留。
- LC 47 怎么改？：排序加 `on_path`，若 `j > 0` 且 `nums[j] == nums[j-1]` 且 `not on_path[j-1]` 就跳过，相等元素必须按下标顺序使用。
- LC 40 怎么改？：同模板加剩余和 `remain`，到 `0` 收集，`nums[i] > remain` 就 `break`，每个数只用一次所以递归 `i + 1`。
- LC 301 怎么改？：先扫一遍算出最少要删的 `(`、`)` 个数当额度，枚举删哪个字符并从位置 `i` 继续往后删，连续相同括号只删第一个，额度用完且有效才收集。

**易错点。**
- 条件写成 `i > 0`：`[1,2,2]` 只得 `[[],[1],[1,2],[2]]`，漏掉 `[1,2,2]` 与 `[2,2]`，应有 `6` 个。
- 忘了排序：`[2,1,2]` 生成 `8` 个，只有 `6` 个不同。
- 全排列 II 写成 `j > 0 and nums[j] == nums[j-1]` 而不看前一个是否已用：`[1,1,2]` 一个结果也没有，应有 `3` 个。

**对应题目。** LC 40 组合总和 II、LC 47 全排列 II、LC 301 删除无效的括号、LC 90 子集 II
