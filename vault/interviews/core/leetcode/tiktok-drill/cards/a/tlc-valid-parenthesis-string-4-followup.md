---
id: tlc-valid-parenthesis-string-4-followup
node: a.valid-parenthesis-string
type: qa
step: 4
---
## Q
**LC 678 有效的括号字符串**｜追问

面试官接着问：（1）不用区间，用栈怎么做，能不能还原出星号的具体取法？（2）还有没有别的线性写法？（3）如果括号有 `()`、`[]`、`{}` 三种，这个方法还成立吗？

## A
1. **两个栈存下标**：一个栈放 `'('` 的下标，一个栈放 `'*'` 的下标。遇到 `')'`：优先弹 `'('`，没有再弹 `'*'`（当 `'('` 用），都没有就失败。扫完后，剩下的 `'('` 必须和它**右边**的 `'*'` 配对（星号当 `')'`），从栈顶往下依次比较下标，`'('` 的下标大于 `'*'` 的下标就失败；最后不能有 `'('` 剩下。因为栈里存的是下标，所以能还原出每个星号变成了什么：

```python
def check_valid_string_stacks(s: str) -> bool:
    left: list[int] = []
    star: list[int] = []
    for i, ch in enumerate(s):
        if ch == '(':
            left.append(i)
        elif ch == '*':
            star.append(i)
        elif left:
            left.pop()
        elif star:
            star.pop()
        else:
            return False
    while left and star:
        if left.pop() > star.pop():
            return False
    return not left
```

2. **双向扫描**：从左到右把所有星号都当 `'('`，计数不能为负（检查 `')'` 是否多出）；再从右到左把所有星号都当 `')'`，计数不能为负（检查 `'('` 是否多出）。两遍都通过就有效。`O(n)` 时间，`O(1)` 空间。
3. **多种括号**：区间贪心不再成立，因为括号的类型要对上，未配对的东西不再是一个数字，而是一个栈的内容。这时退回到带记忆的回溯，或区间 DP（`n <= 100` 时 `O(n^3)`）。

**Python 提醒**：当栈用的 `list` 只在尾部操作（`append` / `pop()`）才是 `O(1)`；`pop(0)` 要整体前移，是 `O(n)`，需要队列时用 `collections.deque`。
