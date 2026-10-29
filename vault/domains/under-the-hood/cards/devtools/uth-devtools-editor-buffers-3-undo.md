---
id: uth-devtools-editor-buffers-3-undo
node: devtools.editor-buffers
type: qa
step: 3
---
## Q
**Vim 的撤销是一棵树**｜Vim · 9.1

撤销两步后做了一次新修改，被撤销的那两步是不是就丢了？

## A
**背景。** 撤销通常用两个栈：撤销时弹出一条改动压进重做栈；做新修改时清空重做栈。简单，但有个后果：撤销两步再做一次新修改，被撤销的那两步就永远丢了。Vim 不丢，它把历史存成一棵树。

**结构。** 每次修改是树上的一个状态；撤销是回到父节点；撤销后再改，就从那个节点长出一条新分支，旧分支原样保留。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 190">
<line x1="80" y1="43" x2="80" y2="67" fill="none" stroke="currentColor" stroke-width="1.2"/>
<line x1="80" y1="93" x2="80" y2="117" fill="none" stroke="currentColor" stroke-width="1.2"/>
<line x1="90" y1="40" x2="160" y2="70" fill="none" stroke="currentColor" stroke-width="1.2"/>
<circle cx="80" cy="30" r="13" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="80" y="34" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">0</text>
<circle cx="80" cy="80" r="13" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="80" y="84" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">1</text>
<circle cx="80" cy="130" r="13" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="80" y="134" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">2</text>
<circle cx="170" cy="80" r="13" stroke="currentColor" stroke-width="1.8" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170" y="84" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">3</text>
<text x="100" y="134" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">旧分支 仍然保留</text>
<text x="196" y="84" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--accent,#3b6fd4)">新修改 当前</text>
<text x="100" y="34" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">原文</text>
<text x="170" y="176" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">撤销 2 步再改 栈会丢掉 1 2 树保留</text>
</svg>
```

**细节。**

- 撤销几步再做新修改，被撤销的改动成为一条分支（`undo-branches`）
- `:undolist` 列出所有叶子；每次修改有递增的编号，`:undo N` 可以直接跳过去
- 撤销树还能存进 undo 文件，重开文件后依然可以撤销

**为什么。** 栈最简单，push 和 pop 都是 O(1)，但会悄悄丢掉重做历史；树把“不丢”的代价换成了存储和导航的复杂度。

**例题：** LC 1472 设计浏览器历史记录（同类：LC 155 最小栈）

实现 `BrowserHistory`：`visit(url)` 访问新页面并清空所有能前进到的记录；`back(steps)` 后退最多 `steps` 步；`forward(steps)` 前进最多 `steps` 步；越界就停在边界，并返回落点的 URL。

```python
class BrowserHistory:
    def __init__(self, homepage: str) -> None:
        self.history: list[str] = [homepage]
        self.cursor = 0

    def visit(self, url: str) -> None:
        del self.history[self.cursor + 1:]
        self.history.append(url)
        self.cursor += 1

    def back(self, steps: int) -> str:
        self.cursor = max(0, self.cursor - steps)
        return self.history[self.cursor]

    def forward(self, steps: int) -> str:
        self.cursor = min(len(self.history) - 1, self.cursor + steps)
        return self.history[self.cursor]
```
