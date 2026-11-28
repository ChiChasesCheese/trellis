---
id: lct-learn-data-structures-7-1
node: data-structures.7.1
type: qa
step: 1
---
## Q
**常用数据结构 › 并查集 › 基础**｜学习卡

套路是什么？

## A
**一句话。** 并查集把元素分成不相交的集合，每个集合推一个代表元：`find` 找代表元（路径压缩），`merge` 小挂大并把块数减一；「同一组」就是 `find(a) == find(b)`，只能合并不能拆。

下图：每个集合是一棵指向根的树；合并时把小树的根挂到大树的根下。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 185">
<text x="80" y="18" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">merge 前</text>
<circle cx="50" cy="45" r="13" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="50" y="49" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<circle cx="30" cy="100" r="13" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="30" y="104" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<circle cx="70" cy="100" r="13" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="70" y="104" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<line x1="34.442659820127155" y1="87.78268549465032" x2="45.557340179872845" y2="57.21731450534968" stroke-width="1.2" stroke="currentColor"/>
<polygon points="45.6,57.2 46.2,64.2 40.6,62.1" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="65.55734017987284" y1="87.78268549465032" x2="54.442659820127155" y2="57.21731450534968" stroke-width="1.2" stroke="currentColor"/>
<polygon points="54.4,57.2 59.4,62.1 53.8,64.2" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="50" y="130" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">size 3</text>
<circle cx="120" cy="45" r="13" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="120" y="49" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<circle cx="120" cy="100" r="13" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="120" y="104" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">4</text>
<line x1="120.0" y1="87.0" x2="120.0" y2="58.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="120.0,58.0 123.0,64.3 117.0,64.3" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="120" y="130" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">size 2</text>
<line x1="150" y1="75" x2="185" y2="75" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="185.0,75.0 178.7,78.0 178.7,72.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="167" y="66" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">merge(4,1)</text>
<text x="265" y="18" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">merge 后：小挂大</text>
<circle cx="265" cy="40" r="13" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="265" y="44" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<circle cx="215" cy="95" r="13" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="215" y="99" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<circle cx="260" cy="95" r="13" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="260" y="99" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<circle cx="310" cy="95" r="13" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="310" y="99" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<circle cx="310" cy="150" r="13" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="310" y="154" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">4</text>
<line x1="223.74474632195205" y1="85.38077904585273" x2="256.25525367804795" y2="49.619220954147266" stroke-width="1.2" stroke="currentColor"/>
<polygon points="256.3,49.6 254.2,56.3 249.8,52.3" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="261.17696469855275" y1="82.05338831591985" x2="263.82303530144725" y2="52.94661168408015" stroke-width="1.2" stroke="currentColor"/>
<polygon points="263.8,52.9 266.2,59.5 260.3,59.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="301.7679087266556" y1="84.93855511035683" x2="273.2320912733444" y2="50.06144488964318" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="273.2,50.1 279.6,53.1 274.9,56.9" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<line x1="310.0" y1="137.0" x2="310.0" y2="108.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="310.0,108.0 313.0,114.3 307.0,114.3" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="170" y="178" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">箭头指向父节点；find 一路走到根（代表元），cc 减一</text>
</svg>

```python
class UnionFind:
    def __init__(self, n):
        self.fa = list(range(n))     # 每个元素自成一个集合
        self.size = [1] * n          # 只在代表元上有效
        self.cc = n                  # 连通块数
    def find(self, x):               # 路径压缩
        if self.fa[x] != x:
            self.fa[x] = self.find(self.fa[x])
        return self.fa[x]
    def merge(self, a, b):           # 返回是否真的合并
        x, y = self.find(a), self.find(b)
        if x == y:
            return False             # 已在一起：这条边成环
        if self.size[x] > self.size[y]:
            x, y = y, x              # 小挂大
        self.fa[x] = y
        self.size[y] += self.size[x]
        self.cc -= 1                 # 成功合并，块数减一
        return True
```

**要点。**
- 为什么对？：`fa` 是森林，每棵树一个集合，根相同当且仅当同组；路径压缩只缩短链，不改变谁和谁同树。压缩加小挂大均摊 `O(α(n))`，小挂大还保证树深至多 `log n`，所以递归 `find` 不会栈溢出。
- LC 684 怎么改？：按顺序加边，第一条 `merge` 返回 `False` 的边就闭合了环，也是环里最后出现的边；点编号从 `1` 起要多开一位。
- LC 721 怎么改？：账户当元素，每个邮箱只记第一次出现的账户，后面遇到再 `merge`；最后按 `find` 的根给邮箱分组、排序、贴上名字。

**易错点。**
- 用 `fa[a] == fa[b]` 判同组：比较的是父亲不是根；`merge(1,2)`、`merge(3,4)`、`merge(2,4)` 后 `1` 与 `3` 同组，但 `fa[1] = 2`、`fa[3] = 4`。
- `merge` 失败时仍 `cc -= 1`，或直接 `fa[a] = b` 不先找根。
- LC 721 用名字当元素：`[["John","a@x"],["John","b@x"]]` 是两个人，应得 `2` 个账户。

**对应题目。** LC 721 账户合并、LC 684 冗余连接（Redundant Connection）
