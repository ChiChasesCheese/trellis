---
slug: validate-stack-sequences
---
## Q
**LC 946 验证栈序列**｜Medium

`pushed`、`popped` 是同一组互不相同数值的两个排列。判断能否从空栈出发，按 `pushed` 的顺序入栈，并穿插出栈，得到恰好是 `popped` 的出栈顺序。

## A
**一句话。** 直接模拟：每入一个元素，只要栈顶等于当前要弹出的元素就立刻弹，最后栈为空则合法。

```python
def validate_stack_sequences(pushed, popped):
    st, j = [], 0
    for x in pushed:
        st.append(x)
        while st and st[-1] == popped[j]:   # 能弹就立刻弹
            st.pop()
            j += 1
    return not st
```

**复杂度。** 时间 `O(n)`，空间 `O(n)`。

**易错点。**
- 只在栈顶匹配时弹一次：弹出后新的栈顶可能还匹配，要用 `while`。
- 不弹的时候也等：能弹时晚弹没有好处，早弹不会错，贪心成立。

**追问。**
- 为什么「能弹就弹」不会错？：栈顶元素是下一个要弹的，现在不弹就必须等到它被压住前弹出，不可能。
- 不用额外栈行吗？：复用 `pushed` 数组的前缀当栈，空间 `O(1)`。

**同模式。** LC 20 有效的括号、LC 155 最小栈、LC 71 简化路径
