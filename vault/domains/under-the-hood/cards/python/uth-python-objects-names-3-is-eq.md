---
id: uth-python-objects-names-3-is-eq
node: python.objects-names
type: qa
step: 3
---
## Q
**is 和 == 差在哪**｜Python · CPython 3.14

`a == b` 和 `a is b` 各自在比什么？为什么判断 `None` 要写 `x is None`？写 `x is 1` 为什么编译器还会警告？

## A
**背景。** 名字只是标签，于是有两个不同的问题：两个名字是不是贴在同一个对象上？两个对象的内容是不是一样？

**结构。** `is` 比较两个名字指向的是不是同一个对象，就是一次指针比较（CPython 里 `Py_Is(x, y)` 就是 `(x) == (y)`），任何类都不能改写它。`==` 会去调 `type(a).__eq__(a, b)`，类想怎么定义「相等」都行。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 180">
<text x="85" y="20" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">a = [1]  b = a</text>
<text x="255" y="20" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">a = [1]  b = [1]</text>
<rect x="10" y="36" width="28" height="22" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="24" y="51" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">a</text>
<rect x="10" y="84" width="28" height="22" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="24" y="99" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">b</text>
<rect x="100" y="54" width="40" height="28" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="120" y="72" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">[1]</text>
<line x1="38" y1="47" x2="98" y2="62" stroke-width="1.2" stroke="currentColor"/>
<polygon points="98.0,62.0 91.5,63.5 92.9,57.6" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="38" y1="95" x2="98" y2="74" stroke-width="1.2" stroke="currentColor"/>
<polygon points="98.0,74.0 93.3,78.8 91.3,73.2" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="180" y="36" width="28" height="22" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="194" y="51" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">a</text>
<rect x="180" y="84" width="28" height="22" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="194" y="99" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">b</text>
<rect x="280" y="36" width="40" height="28" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="300" y="54" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">[1]</text>
<rect x="280" y="84" width="40" height="28" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="300" y="102" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">[1]</text>
<line x1="208" y1="47" x2="278" y2="50" stroke-width="1.2" stroke="currentColor"/>
<polygon points="278.0,50.0 271.9,52.7 272.1,46.7" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="208" y1="95" x2="278" y2="98" stroke-width="1.2" stroke="currentColor"/>
<polygon points="278.0,98.0 271.9,100.7 272.1,94.7" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="85" y="142" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">is 真   == 真</text>
<text x="255" y="142" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">is 假   == 真</text>
<line x1="170" y1="28" x2="170" y2="130" stroke-width="1.2" stroke="currentColor" stroke-dasharray="4 3"/>
<text x="170" y="170" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">is 比地址  == 比内容</text>
</svg>
```

**细节。**

- 不写 `__eq__` 的类，`==` 默认也退化成比身份。
- `None` 全局只有一个对象，`x is None` 永远可靠；`x == None` 要经过 `x.__eq__`，自定义类可以让它返回任何结果。
- 3.8 起，`x is 1` 这类写法在编译时给出 `SyntaxWarning: "is" with 'int' literal`。

**坑。** 比较值永远用 `==`，`is` 只留给 `None`，以及确实要问「是不是同一个对象」的地方。

**例题：** LC 160 相交链表

给两个单链表的头节点 `headA`、`headB`，找出并返回两个链表相交的起始节点；不相交返回 `null`。链表无环，返回后必须保持原结构，`m, n <= 3 * 10^4`。

```python
def get_intersection_node(head_a: ListNode | None, head_b: ListNode | None) -> ListNode | None:
    a, b = head_a, head_b
    while a is not b:                   # 比的是节点本身（地址），不是值
        a = a.next if a else head_b     # 走到头就换到另一条链表的表头
        b = b.next if b else head_a
    return a                            # 相交节点；不相交时 a、b 同时为 None
```
