---
id: uth-java-arraylist-arraydeque-3-vs-stack
node: java.arraylist-arraydeque
type: qa
step: 3
---
## Q
**栈和队列该用 Stack、LinkedList 还是 ArrayDeque**｜Java · OpenJDK 25

做栈或队列时，官方文档为什么推荐 `ArrayDeque`？它为什么不允许放 `null`？

## A
**背景。** 栈（后进先出）和队列（先进先出）只动两端，不需要中间随机访问。Java 里有三个现成的选择，差别在内存布局和加锁。

**结构。** `Stack` 继承 `Vector`，方法都带 `synchronized`（加锁）；`LinkedList` 每个元素一个 `Node`（`item`、`next`、`prev`）；`ArrayDeque` 是一个连续数组。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 200">
<text x="20" y="22" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">ArrayDeque 一块连续数组</text>
<rect x="40" y="32" width="48" height="26" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<rect x="88" y="32" width="48" height="26" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<rect x="136" y="32" width="48" height="26" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<rect x="184" y="32" width="48" height="26" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<rect x="232" y="32" width="48" height="26" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="20" y="94" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">LinkedList 每个元素一个 Node</text>
<rect x="20" y="108" width="44" height="28" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="42" y="126" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Node</text>
<line x1="64" y1="122" x2="100" y2="122" stroke-width="1.2" stroke="currentColor"/>
<polygon points="100.0,122.0 96.0,124.0 96.0,120.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<polygon points="64.0,122.0 68.0,120.0 68.0,124.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="100" y="108" width="44" height="28" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="122" y="126" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Node</text>
<line x1="144" y1="122" x2="180" y2="122" stroke-width="1.2" stroke="currentColor"/>
<polygon points="180.0,122.0 176.0,124.0 176.0,120.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<polygon points="144.0,122.0 148.0,120.0 148.0,124.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="180" y="108" width="44" height="28" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="202" y="126" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Node</text>
<line x1="224" y1="122" x2="260" y2="122" stroke-width="1.2" stroke="currentColor"/>
<polygon points="260.0,122.0 256.0,124.0 256.0,120.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<polygon points="224.0,122.0 228.0,120.0 228.0,124.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="260" y="108" width="44" height="28" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="282" y="126" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Node</text>
<text x="170" y="174" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">Stack 每次调用还要 synchronized</text>
</svg>
```

**细节。**

- 文档原话：作栈时可能比 `Stack` 快，作队列时可能比 `LinkedList` 快。
- 数组不用逐个元素分配对象，遍历时内存连续、缓存友好；`Stack` 的每次调用还要加锁。
- `pollFirst` 靠「该槽为 `null`」判断空，所以 `addFirst(null)` 直接抛 `NullPointerException`。

**为什么。** 数组把分配成本摊到整块上，没有每个元素一个对象的开销。

**坑。** `Deque` 做栈要用 `push`、`pop`，别混用 `add`、`remove`，否则方向反了。

**例题：** LC 20 有效的括号

给只含 `()[]{}` 的字符串 `s`，判断括号是否有效：每个左括号都按正确顺序被同类型的右括号闭合。

```python
def is_valid(s: str) -> bool:
    pairs = {")": "(", "]": "[", "}": "{"}
    stack: list[str] = []
    for c in s:
        if c in pairs:
            if not stack or stack.pop() != pairs[c]:
                return False
        else:
            stack.append(c)
    return not stack
```
