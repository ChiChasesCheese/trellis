---
id: lct-learn-list-tree-backtracking-2-15
node: list-tree-backtracking.2.15
type: qa
step: 1
---
## Q
**链表、二叉树与回溯 › 二叉树 › N 叉树**｜学习卡

套路是什么？

## A
**一句话。** N 叉树做法同二叉树，只是把「递归左右」换成「对 `children` 循环」；序列化时把「孩子个数」和值一起写进去，读时先读个数再读那么多棵子树，不需要任何分隔符。

下图：每个节点写成「值, 孩子个数」两格，按先序排开。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 165">
<line x1="71.1" y1="31.5" x2="43.9" y2="60.5" stroke-width="1.2" stroke="currentColor"/>
<line x1="80.0" y1="35.0" x2="80.0" y2="57.0" stroke-width="1.2" stroke="currentColor"/>
<line x1="88.9" y1="31.5" x2="116.1" y2="60.5" stroke-width="1.2" stroke="currentColor"/>
<line x1="31.1" y1="82.4" x2="23.9" y2="105.6" stroke-width="1.2" stroke="currentColor"/>
<line x1="40.0" y1="82.0" x2="50.0" y2="106.0" stroke-width="1.2" stroke="currentColor"/>
<circle cx="80" cy="22" r="13" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="80" y="26" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">1</text>
<circle cx="35" cy="70" r="13" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="35" y="74" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<circle cx="80" cy="70" r="13" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="80" y="74" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<circle cx="125" cy="70" r="13" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="125" y="74" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">4</text>
<circle cx="20" cy="118" r="13" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="20" y="122" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">5</text>
<circle cx="55" cy="118" r="13" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="55" y="122" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">6</text>
<rect x="10" y="140" width="26" height="22" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="23.0" y="155.0" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">1</text>
<rect x="36" y="140" width="26" height="22" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="49.0" y="155.0" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">3</text>
<rect x="62" y="140" width="26" height="22" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="75.0" y="155.0" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">3</text>
<rect x="88" y="140" width="26" height="22" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="101.0" y="155.0" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">2</text>
<rect x="114" y="140" width="26" height="22" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="127.0" y="155.0" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">5</text>
<rect x="140" y="140" width="26" height="22" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="153.0" y="155.0" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">0</text>
<rect x="166" y="140" width="26" height="22" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="179.0" y="155.0" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">6</text>
<rect x="192" y="140" width="26" height="22" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="205.0" y="155.0" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">0</text>
<rect x="218" y="140" width="26" height="22" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="231.0" y="155.0" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">2</text>
<rect x="244" y="140" width="26" height="22" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="257.0" y="155.0" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">0</text>
<rect x="270" y="140" width="26" height="22" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="283.0" y="155.0" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">4</text>
<rect x="296" y="140" width="26" height="22" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="309.0" y="155.0" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">0</text>
<line x1="12" y1="136" x2="60" y2="136" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<line x1="64" y1="136" x2="112" y2="136" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<line x1="116" y1="136" x2="164" y2="136" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<line x1="168" y1="136" x2="216" y2="136" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<line x1="220" y1="136" x2="268" y2="136" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<line x1="272" y1="136" x2="320" y2="136" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<text x="160" y="30" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">先序写 (值, 孩子个数)</text>
<text x="160" y="50" text-anchor="start" font-size="11" font-family="sans-serif" fill="currentColor">读：先读个数 k，</text>
<text x="160" y="66" text-anchor="start" font-size="11" font-family="sans-serif" fill="currentColor">再递归读 k 棵子树</text>
<text x="160" y="92" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">个数自带边界，不要分隔符</text>
</svg>

```python
def serialize(root):                 # LC 428：写 值, 孩子个数
    out = []
    def dfs(node):
        out.append(node.val)
        out.append(len(node.children))   # 个数自带边界
        for child in node.children:
            dfs(child)               # 先序
    if root:
        dfs(root)
    return ' '.join(map(str, out))

def deserialize(data):
    it = iter(map(int, data.split()))
    def build():
        val, k = next(it), next(it)  # 先读个数，再读 k 棵子树
        return Node(val, [build() for _ in range(k)])
    return build() if data else None
```

**要点。**
- 为什么对？：`build` 每读一对 `(值, k)` 就恰好调用 `k` 次自己，每棵子树恰好用完自己那段，所以无歧义；二叉树里 `#` 占位起的是同一个作用，`O(n)`。
- 层序、深度怎么改？：层序把两个 `if` 换成 `q.extend(node.children)`；深度、直径对所有孩子的返回值取最大或最大的两个。
- LC 427 怎么改？：区域递归，边长 `size` 切成四个 `size / 2` 的象限；合并放在后序，仅当四个孩子都是叶子且值相同才合并成叶子，`size == 1` 直接是叶子。

**易错点。**
- 只写值不写孩子个数：`1 -> [3,2,4]`、`3 -> [5,6]` 写成 `1 3 5 6 2 4` 读不回；应写 `1 3 3 2 5 0 6 0 2 0 4 0`。
- 空树：序列化成空串，反序列化空串要返回 `None`，否则 `next(it)` 抛 `StopIteration`。
- LC 427 合并时只比较 `val`：内部节点的 `val` 任意，必须先确认四个孩子都是叶子。

**对应题目。** LC 427 建立四叉树、LC 428 序列化和反序列化 N 叉树
