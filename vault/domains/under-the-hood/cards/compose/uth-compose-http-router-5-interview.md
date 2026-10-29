---
id: uth-compose-http-router-5-interview
node: compose.http-router
type: qa
step: 5
---
## Q
**借到面试题上：带通配符的匹配**｜Gin · v1.11.0

面试题给一组带通配符的模式（`.` 匹配任意一个字符），问输入能否匹配。路由树的骨架怎样借过来？

## A
**背景。** 骨架不变：模式存进树，沿输入往下走。新问题只有一个：静态分支和通配分支都可能走得通，先走哪条？走不通怎么办？

**结构。** 两种答案：

- httprouter：注册时禁止两者并存，查找一条路走到底
- Gin 和 LC 211：都允许。先试精确分支，失败就退回岔路口再试通配分支。Gin 用 `skippedNodes` 栈记下岔路口，LC 211 用递归（DFS）自然退回

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 222">
<text x="170" y="16" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">请求 GET /files/new/edit</text>
<rect x="133.0" y="28" width="74" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1"/>
<text x="170" y="44.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">/files/</text>
<rect x="61.0" y="88" width="54" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1"/>
<text x="88" y="104.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">new/</text>
<rect x="227.0" y="88" width="50" height="24" rx="3" fill="none" style="stroke:var(--accent,#3b6fd4)" stroke-width="1.5" stroke-dasharray="4 3"/>
<text x="252" y="104.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">:id</text>
<rect x="60.0" y="148" width="56" height="24" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="88" y="164.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">list</text>
<rect x="224.0" y="148" width="56" height="24" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="252" y="164.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">/edit</text>
<line x1="150" y1="52" x2="100" y2="88" stroke="currentColor" stroke-width="1"/>
<line x1="190" y1="52" x2="240" y2="88" stroke="currentColor" stroke-width="1"/>
<line x1="88" y1="112" x2="88" y2="148" stroke="currentColor" stroke-width="1"/>
<line x1="252" y1="112" x2="252" y2="148" stroke="currentColor" stroke-width="1"/>
<text x="112" y="76" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">1</text>
<text x="228" y="76" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">2</text>
<path d="M 61 100 C 14 100, 24 40, 120 40" fill="none" style="stroke:var(--accent,#3b6fd4)" stroke-width="1" stroke-dasharray="4 3"/>
<line x1="120" y1="40" x2="125.0" y2="40.0" style="stroke:var(--accent,#3b6fd4)" stroke-width="1"/>
<polygon points="132,40 125.0,36.8 125.0,43.2" style="fill:var(--accent,#3b6fd4)"/>
<text x="62" y="72" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">退回</text>
<text x="88" y="192" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">1 先试静态分支</text>
<text x="88" y="208" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">edit != list, 走不通</text>
<text x="252" y="192" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">2 退回再试参数分支</text>
<text x="252" y="208" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">id = new, 命中</text>
</svg>
```

**细节。**

- 在 Gin v1.11.0 里注册 `/files/new/list` 与 `/files/:id/edit` 后，请求 `/files/new/edit` 先走静态分支，到 `list` 走不通，退回后由 `:id` 吃下 `new`，命中第二条路由
- 最坏情况每个岔路口都要试两条，查找不再严格随路径长度线性增长

**为什么。** 允许并存，路由写起来更自由；代价是最坏情况更慢，实现里多一个回退用的栈。

**例题：** LC 211 添加与搜索单词

设计 `WordDictionary`：`addWord(word)` 加入单词，`search(word)` 判断是否有单词与之匹配，其中 `'.'` 可以表示任意一个字母。单词长度 1 到 25，两个方法合计最多调用 10^4 次。例：加入 `bad`、`dad`、`mad` 后，`search("pad")` → `false`，`search("bad")` → `true`，`search(".ad")` → `true`，`search("b..")` → `true`。遇到 `.` 就对每个孩子递归，任一分支成功即成功。

```python
class WordDictionary:
    def __init__(self) -> None:
        self.root: dict[str, dict] = {}           # 字典树：键是字母，值是子结点；键 "$" 标记单词在此结束

    def addWord(self, word: str) -> None:
        node = self.root
        for ch in word:
            node = node.setdefault(ch, {})        # 有就取、没有就建，一步完成
        node["$"] = {}

    def search(self, word: str) -> bool:
        def dfs(node: dict[str, dict], i: int) -> bool:
            if i == len(word):
                return "$" in node
            ch = word[i]
            if ch == ".":                         # 通配符：除结束标记外，每个孩子都试一遍
                return any(dfs(child, i + 1) for key, child in node.items() if key != "$")
            return ch in node and dfs(node[ch], i + 1)

        return dfs(self.root, 0)
```
