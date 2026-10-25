---
id: tlc-minimum-remove-to-make-valid-parentheses-4-followup
node: b.minimum-remove-to-make-valid-parentheses
type: qa
step: 4
---
## Q
**LC 1249 移除无效的括号**｜追问

面试官接着问：（1）能不能不用栈，额外空间 `O(1)`（不算输出）？（2）只要最少删除的个数？（3）要列出**所有**最少删除的合法结果？

## A
1. **两遍扫描**：从左到右用计数器删掉多余的 `)`，再从右到左用计数器删掉多余的 `(`。

```python
def min_remove_two_pass(s: str) -> str:
    chars = list(s)
    bal = 0
    for i, ch in enumerate(chars):               # 左到右：删多余的 ")"
        if ch == "(":
            bal += 1
        elif ch == ")":
            if bal:
                bal -= 1
            else:
                chars[i] = ""
    bal = 0
    for i in range(len(chars) - 1, -1, -1):      # 右到左：删多余的 "("
        if chars[i] == ")":
            bal += 1
        elif chars[i] == "(":
            if bal:
                bal -= 1
            else:
                chars[i] = ""
    return "".join(chars)
```

   `"lee(t(c)o)de)"` → `'lee(t(c)o)de'`，`"(a(b(c)d"` → `'ab(c)d'`。第二遍从右往左看，一个 `(` 要有右边没被配走的 `)` 才保留，对称于第一遍。额外空间只有字符数组（输出本身）。
2. **只要个数**：不用拼结果，维护 `bal`（未配对 `(` 数）和 `extra`（多余 `)` 数），答案是 `extra + bal`，空间 `O(1)`。这是 LC 921 的做法。
3. **列出全部方案**（LC 301）：此时有选择，要搜索。从原串出发按层做 BFS，每层把当前每个字符串各删一个括号，用集合去重；第一次在某层里出现有效串，这一层的所有有效串就是答案。最坏指数级，但层数就是最少删除数，通常很小。

**Python 提醒**：字符串不可变，修改要先转 `list`；把字符置成空串 `""` 再 `join`，比 `pop` 或切片重建省事，也不会让后面的下标移位。
