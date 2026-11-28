---
id: lct-learn-list-tree-backtracking-2-7
node: list-tree-backtracking.2.7
type: qa
step: 1
---
## Q
**链表、二叉树与回溯 › 二叉树 › 回溯**｜学习卡

套路是什么？

## A
**一句话。** 二叉树上的回溯：用一个共享路径沿途「进门加入、出门弹出」，到叶子满足条件时拷贝一份路径记入答案。

下图：一条共享的 `path` 随 DFS 进出变化，任何时刻都等于根到当前节点的路径。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 180">
<line x1="72.0" y1="32.3" x2="53.0" y2="56.7" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="89.2" y1="31.2" x2="115.8" y2="57.8" stroke-width="1.2" stroke="currentColor"/>
<line x1="45.0" y1="80.0" x2="45.0" y2="99.0" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="38.7" y1="123.4" x2="26.3" y2="145.6" stroke-width="1.2" style="stroke:var(--dim,#6b7280)" stroke-dasharray="4 3"/>
<line x1="52.2" y1="122.8" x2="67.8" y2="146.2" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<circle cx="80" cy="22" r="13" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="80" y="26" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">5</text>
<circle cx="45" cy="67" r="13" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="45" y="71" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">4</text>
<circle cx="125" cy="67" r="13" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="125" y="71" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">8</text>
<circle cx="45" cy="112" r="13" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="45" y="116" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">11</text>
<circle cx="20" cy="157" r="13" fill="none" style="stroke:var(--dim,#6b7280)" stroke-width="1.2"/>
<text x="20" y="161" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">7</text>
<circle cx="75" cy="157" r="13" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="75" y="161" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">2</text>
<text x="165" y="30" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">target = 22</text>
<text x="165" y="58" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">path</text>
<rect x="200" y="44" width="30" height="28" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="215.0" y="62.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">5</text>
<rect x="230" y="44" width="30" height="28" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="245.0" y="62.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">4</text>
<rect x="260" y="44" width="30" height="28" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="275.0" y="62.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">11</text>
<rect x="290" y="44" width="30" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="305.0" y="62.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<text x="165" y="98" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">进门 append，出门 pop</text>
<text x="165" y="118" text-anchor="start" font-size="11" font-family="sans-serif" fill="currentColor">到叶子且 rest == 0：</text>
<text x="165" y="134" text-anchor="start" font-size="11" font-family="sans-serif" fill="currentColor">记 path[:] 的拷贝</text>
<text x="165" y="160" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">7 那条路已 pop 出去</text>
</svg>

```python
def path_sum(root, target):
    res, path = [], []

    def dfs(node, rest):
        if node is None:
            return
        path.append(node.val)        # 选：进入节点
        rest -= node.val
        if not node.left and not node.right and rest == 0:
            res.append(path[:])      # 拷贝，path 之后还会变
        dfs(node.left, rest)
        dfs(node.right, rest)
        path.pop()                   # 撤销：恢复现场

    dfs(root, target)
    return res
```

**要点。**
- 为什么对？：`path` 在进入子树前后保持一致（加一个、弹一个），所以兄弟子树看到的是同样的前缀；剩余值作为参数传递，自动随栈恢复，不用手动撤销。
- 只要判断是否存在怎么改？：改成有返回值，叶子处返回 `rest == 0`，其余返回左右子树的 `or`。

**易错点。**
- 记录答案不拷贝：`res.append(path)` 存的是同一个列表，最后全变成空。
- 在非叶子节点判断：`[1,2]` 目标 `1` 时，节点 `1` 不是叶子，不能算一条路径。
- 提前 `return` 跳过 `pop`：在叶子处直接返回会让路径多一个元素。

**对应题目。** LC 113 路径总和 II
