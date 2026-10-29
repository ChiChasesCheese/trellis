---
id: uth-devtools-editor-buffers-1-gap
node: devtools.editor-buffers
type: qa
step: 1
---
## Q
**Emacs 的缓冲区带一个“空洞”**｜Emacs · 30.1

在文本中间连续打字，为什么不用每次都挪动后面的内容？

## A
**背景。** 编辑器要在文本中间不断插入字符。文本放在普通数组里，每插一个字符，后面所有字符都要往后搬一格；每行一个对象，省了搬运，却多占内存、不利于缓存。间隙缓冲区（gap buffer）的办法：在数组里留一段空位，让它跟着光标走。

**结构。** 一块连续内存，光标处留一段空白（gap），文本被它分成前后两段。例：`he`、空位、`llo`，在光标处打一个字符，就是写进空位的第一格，不用搬任何字符。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 206">
<text x="35" y="24" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">空位留在光标处 在 he 和 llo 之间</text>
<rect x="35" y="32" width="30" height="26" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="50" y="50" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">h</text>
<rect x="65" y="32" width="30" height="26" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="80" y="50" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">e</text>
<rect x="95" y="32" width="30" height="26" rx="2" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<rect x="125" y="32" width="30" height="26" rx="2" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<rect x="155" y="32" width="30" height="26" rx="2" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<rect x="185" y="32" width="30" height="26" rx="2" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<rect x="215" y="32" width="30" height="26" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="230" y="50" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">l</text>
<rect x="245" y="32" width="30" height="26" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="260" y="50" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">l</text>
<rect x="275" y="32" width="30" height="26" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="290" y="50" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">o</text>
<text x="35" y="86" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">打 y 只是写进空位 O(1)</text>
<rect x="35" y="94" width="30" height="26" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="50" y="112" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">h</text>
<rect x="65" y="94" width="30" height="26" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="80" y="112" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">e</text>
<rect x="95" y="94" width="30" height="26" rx="2" fill="none" stroke="currentColor" stroke-width="1.8" style="stroke:var(--accent,#3b6fd4)"/>
<text x="110" y="112" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">y</text>
<rect x="125" y="94" width="30" height="26" rx="2" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<rect x="155" y="94" width="30" height="26" rx="2" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<rect x="185" y="94" width="30" height="26" rx="2" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<rect x="215" y="94" width="30" height="26" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="230" y="112" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">l</text>
<rect x="245" y="94" width="30" height="26" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="260" y="112" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">l</text>
<rect x="275" y="94" width="30" height="26" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="290" y="112" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">o</text>
<text x="35" y="148" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">光标跳到末尾 空位要搬过去</text>
<rect x="35" y="156" width="30" height="26" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="50" y="174" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">h</text>
<rect x="65" y="156" width="30" height="26" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="80" y="174" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">e</text>
<rect x="95" y="156" width="30" height="26" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="110" y="174" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">y</text>
<rect x="125" y="156" width="30" height="26" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="140" y="174" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">l</text>
<rect x="155" y="156" width="30" height="26" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170" y="174" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">l</text>
<rect x="185" y="156" width="30" height="26" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="200" y="174" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">o</text>
<rect x="215" y="156" width="30" height="26" rx="2" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<rect x="245" y="156" width="30" height="26" rx="2" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<rect x="275" y="156" width="30" height="26" rx="2" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<line x1="170" y1="62" x2="170" y2="81" fill="none" stroke="currentColor" stroke-width="1.8" style="stroke:var(--accent,#3b6fd4)"/>
<path d="M170.0,86.0 L166.7,79.2 L173.3,79.2 Z" stroke="none" style="fill:var(--accent,#3b6fd4)"/>
<rect x="125" y="156" width="30" height="26" rx="2" fill="none" stroke="currentColor" stroke-width="1.8" style="stroke:var(--accent,#3b6fd4)"/>
<rect x="155" y="156" width="30" height="26" rx="2" fill="none" stroke="currentColor" stroke-width="1.8" style="stroke:var(--accent,#3b6fd4)"/>
<rect x="185" y="156" width="30" height="26" rx="2" fill="none" stroke="currentColor" stroke-width="1.8" style="stroke:var(--accent,#3b6fd4)"/>
</svg>
```

**细节。**

- 在光标处插入就是写进空位，O(1)；删除就是让空位变大
- 光标跳到别处，要把空位搬过去（一次内存拷贝），代价与移动距离成正比
- 空位不够时，Emacs 一次多要 2000 字节（`GAP_BYTES_DFL`）

**为什么。** 编辑集中在光标附近，连续内存比“每行一个对象”或链表更省内存、更利于缓存；只有跳转后的第一次编辑才付搬迁代价。

**例题：** LC 232 用栈实现队列

只用两个栈实现先进先出队列：`push`、`pop`、`peek`、`empty`；进阶：每个操作均摊 O(1)。例：`push(1)`、`push(2)`、`peek()` → 1、`pop()` → 1、`empty()` → `false`。

```python
class MyQueue:
    def __init__(self) -> None:
        self.inbox: list[int] = []        # 只负责 push：新元素压在栈顶
        self.outbox: list[int] = []       # 只负责 pop / peek：栈顶就是队首

    def push(self, x: int) -> None:
        self.inbox.append(x)

    def _move(self) -> None:
        if not self.outbox:               # 只有 outbox 空了才倒，倒的时候整个 inbox 一次倒完
            while self.inbox:
                self.outbox.append(self.inbox.pop())

    def pop(self) -> int:
        self._move()
        return self.outbox.pop()

    def peek(self) -> int:
        self._move()
        return self.outbox[-1]

    def empty(self) -> bool:
        return not self.inbox and not self.outbox
```
