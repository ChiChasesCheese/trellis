---
id: uth-java-string-3-builder
node: java.string
type: qa
step: 3
---
## Q
**循环里 += 为什么慢**｜Java · OpenJDK 25

循环里用 `s += "x"` 拼接字符串，和 `StringBuilder.append` 差多少？`StringBuilder` 怎么扩容？

## A
**背景。** `String` 不可变：拼接不能在原来的字符串上改，只能新建一个，把旧内容全部复制过去再加上新的。循环 n 次，复制的总量是 1+2+…+n，即 O(n²)。

**结构。** `StringBuilder` 内部是一个可变的字符数组，只在里面追加；满了才扩容，复制摊到许多次追加上。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 210">
<text x="20" y="18" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">s += x  每次新建 复制全部旧内容</text>
<rect x="20" y="28" width="40" height="14" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<rect x="20" y="46" width="80" height="14" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<rect x="20" y="64" width="120" height="14" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<rect x="20" y="82" width="160" height="14" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="20" y="126" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">StringBuilder  只在数组里追加</text>
<rect x="20" y="136" width="19" height="24" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<rect x="39" y="136" width="19" height="24" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<rect x="58" y="136" width="19" height="24" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<rect x="77" y="136" width="19" height="24" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<rect x="96" y="136" width="19" height="24" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<rect x="115" y="136" width="19" height="24" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<rect x="134" y="136" width="19" height="24" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<rect x="153" y="136" width="19" height="24" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<rect x="172" y="136" width="19" height="24" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<rect x="191" y="136" width="19" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="210" y="136" width="19" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="229" y="136" width="19" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="248" y="136" width="19" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="267" y="136" width="19" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="286" y="136" width="19" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="305" y="136" width="19" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170" y="184" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">容量 16 满了才扩为 2n+2</text>
</svg>
```

**细节。**

- 本机实测 `+=`：2 万次 39 毫秒，4 万次 86 毫秒，8 万次 233 毫秒；`append` 都不到 1 毫秒。
- `StringBuilder` 初始容量 16，满了扩为 `2n+2`，实测 `16 34 70 142 286 574`。
- 单个表达式的 `a + b + c` 不必担心：`javap` 实测编译成 `invokedynamic`，不是 `StringBuilder` 链。

**为什么。** 不可变换来线程安全和哈希缓存，代价是拼接要复制；缓冲区把复制摊成均摊 O(1)。

**例题：** LC 415 字符串相加

给两个字符串形式的非负整数 `num1`、`num2`，返回它们的和（字符串）；不能用大整数库，也不能直接转成整数。例：`"456"` 加 `"77"` 得 `"533"`。

```python
from itertools import zip_longest


def add_strings(num1: str, num2: str) -> str:
    digits: list[str] = []
    carry = 0
    # 从个位开始配对；短的那个用 "0" 补齐
    for a, b in zip_longest(reversed(num1), reversed(num2), fillvalue="0"):
        carry, d = divmod(int(a) + int(b) + carry, 10)    # 一步同时得到进位和当前位
        digits.append(str(d))
    if carry:
        digits.append("1")
    return "".join(reversed(digits))
```
