---
id: uth-gaps-tree-dfs-4-json-depth
node: gaps.tree-dfs
type: qa
step: 4
---
## Q
**JSON 嵌套太深会怎样**｜Go · encoding/json 1.24

一个 `[[[[…]]]]` 嵌套一百万层的 JSON 交给 Go 的 `encoding/json`，会发生什么？它怎样不被撑爆？

## A
**背景。** 嵌套数据是树，最顺手的写法是递归：遇到 `[` 进一层函数调用，遇到 `]` 返回。每层调用占调用栈，对方发一个很深的 JSON 就能把程序弄崩。

**结构。** Go 的扫描器（scanner）用切片 `parseState` 当显式栈，记录当前嵌套在哪几层括号里：遇到 `[` 或 `{` 压一格，遇到 `]` 或 `}` 弹一格。压栈时检查长度，超过 `maxNestingDepth = 10000` 就报错 `exceeded max depth`。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 206">
<line x1="96" y1="40" x2="324" y2="40" fill="none" stroke="currentColor" stroke-width="1.8" stroke-dasharray="4 3" style="stroke:var(--accent,#3b6fd4)"/>
<text x="210" y="32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--accent,#3b6fd4)">超过 10000 层: exceeded max depth</text>
<rect x="120" y="52" width="80" height="22" rx="3" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3" style="stroke:var(--dim,#6b7280)"/>
<text x="160" y="67" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">...</text>
<rect x="120" y="78" width="80" height="22" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="160" y="93" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">[</text>
<rect x="120" y="104" width="80" height="22" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="160" y="119" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">[</text>
<rect x="120" y="130" width="80" height="22" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="160" y="145" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">{</text>
<rect x="120" y="156" width="80" height="22" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="160" y="171" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">[</text>
<text x="160" y="196" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">parseState</text>
<text x="10" y="108" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">遇到 [ 或 {</text>
<text x="10" y="126" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--accent,#3b6fd4)">压一格</text>
<line x1="92" y1="89" x2="110" y2="89" fill="none" stroke="currentColor" stroke-width="1.8" style="stroke:var(--accent,#3b6fd4)"/>
<path d="M116,89 L110,92 L110,86 Z" stroke="none" style="fill:var(--accent,#3b6fd4)"/>
<text x="212" y="160" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">遇到 ] 或 }</text>
<text x="212" y="178" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--accent,#3b6fd4)">弹一格</text>
</svg>
```

**细节。**

- 源码注释写明上限是为了防止栈溢出，RFC 也允许解析器限制嵌套深度
- 把 JSON 填进结构体的解码器是递归的（`d.value` → `d.array` → `d.value`），所以要先拦住深度

**为什么。** 递归写起来最短，所以保留；用上限换安全，报错好过整个进程崩掉。

**例题：** LC 394 字符串解码（同类：LC 341 展平嵌套列表迭代器）

编码规则 `k[encoded_string]` 表示方括号里的内容重复 `k` 次，可以嵌套。返回解码后的字符串。`s` 由小写字母、数字和 `[]` 组成，`1 <= s.length <= 30`。例：`"3[a2[c]]"` → `"accaccacc"`。下面的解答用栈代替递归。

```python
def decode_string(s: str) -> str:
    stack: list[tuple[str, int]] = []     # (进入 [ 之前已拼好的前缀, 这一层的重复次数)
    cur, num = "", 0
    for ch in s:
        if ch.isdigit():
            num = num * 10 + int(ch)      # 次数可能是多位数
        elif ch == "[":
            stack.append((cur, num))
            cur, num = "", 0              # 进入新的一层，从空串重新拼
        elif ch == "]":
            prev, times = stack.pop()
            cur = prev + cur * times      # 把这一层重复 times 次接到前缀后面
        else:
            cur += ch
    return cur
```
