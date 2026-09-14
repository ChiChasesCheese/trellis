---
id: cc-algorithms-strings-one-edit
node: algorithms.strings
type: qa
---
## Q
"Are these two strings exactly one edit apart?" Write the pass and name the trap.

## A
**Identical strings are `False`** — that is the most common wrong answer, and it includes two empty strings.

```python
if abs(len(a) - len(b)) > 1 or a == b:
    return False
if len(a) > len(b):
    a, b = b, a                       # a is now the shorter or equal one
for i in range(len(a)):
    if a[i] != b[i]:
        return a[i+1:] == b[i+1:] if len(a) == len(b) else a[i:] == b[i+1:]
return True                           # b has exactly one extra character at the end
```

- Find the first mismatch by **scanning**; do not assume the extra character is at the end. `"aa"` vs `"aaa"` and `"aa"` vs `"baa"` differ in where the insertion is.
- Equal lengths → a replace, so compare the tails after `i`. Different lengths → an insert, so compare `a[i:]` with `b[i+1:]`.
- Falling off the loop means every compared character matched, and the length check already limited the difference to one trailing character.
- A **transposition** of two characters is *two* edits under this definition unless the spec says otherwise — and swapping two equal characters is no edit at all.

## Q zh
「这两个字符串是否恰好相差一次编辑？」写出这一趟并指出陷阱。

## A zh
**完全相同的字符串返回 `False`** —— 这是最常见的错误答案，而且包括两个空串的情况。

```python
if abs(len(a) - len(b)) > 1 or a == b:
    return False
if len(a) > len(b):
    a, b = b, a                       # 现在 a 是较短或等长的那个
for i in range(len(a)):
    if a[i] != b[i]:
        return a[i+1:] == b[i+1:] if len(a) == len(b) else a[i:] == b[i+1:]
return True                           # b 末尾恰好多一个字符
```

- 用**扫描**找到第一个失配处；不要假设多出的字符在末尾。`"aa"` 对 `"aaa"` 与 `"aa"` 对 `"baa"` 的插入位置就不同。
- 长度相等 → 是替换，比较 `i` 之后的尾部。长度不等 → 是插入，比较 `a[i:]` 与 `b[i+1:]`。
- 循环跑完说明比较过的每个字符都相同，而长度检查已把差异限制为末尾一个字符。
- 除非 spec 另有规定，两个字符的**换位**在这个定义下算*两*次编辑 —— 而交换两个相同的字符则完全不算编辑。
