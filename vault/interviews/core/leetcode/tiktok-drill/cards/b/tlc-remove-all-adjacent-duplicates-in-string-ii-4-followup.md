---
id: tlc-remove-all-adjacent-duplicates-in-string-ii-4-followup
node: b.remove-all-adjacent-duplicates-in-string-ii
type: qa
step: 4
---
## Q
**LC 1209 删除字符串中的所有相邻重复项 II**｜追问

面试官接着问：（1）能不能不用栈，在字符数组上原地处理？（2）要统计一共做了多少次删除？（3）输入是字符流，一个一个到来？

## A
1. **原地双指针**：把字符数组当栈用，写指针 `w` 就是栈顶位置，另用一个计数数组 `counts[w]` 记录“以 `chars[w]` 结尾的连续相同字符个数”。凑够 `k` 个时，写指针回退 `k` 位（再加一就是回退 `k - 1` 位）。

```python
def remove_duplicates_inplace(s: str, k: int) -> str:
    chars = list(s)
    counts = [0] * len(chars)
    w = 0                                   # 写指针：chars[:w] 是当前的结果
    for r in range(len(chars)):
        chars[w] = chars[r]
        counts[w] = counts[w - 1] + 1 if w and chars[w - 1] == chars[w] else 1
        if counts[w] == k:
            w -= k                          # 这 k 个整段删除；下面的 w += 1 把指针放到删除位置
        w += 1
    return "".join(chars[:w])
```

   `("deeedbbcccbdaa", 3)` → `'aa'`，`("pbbcggttciiippooaais", 2)` → `'ps'`。额外空间仍是 `O(n)`（计数数组），但没有元组，常数更小。
2. **统计删除次数**：栈解法里每次整项弹出就加一；也可以用 `(n - len(result)) // k` 直接算，因为每次删除恰好去掉 `k` 个字符。
3. **流式输入**：栈就是全部状态，每来一个字符做同样的更新，均摊 `O(1)`；任何时刻栈还原出的字符串就是“到现在为止”的答案。

**Python 提醒**：`counts[w - 1]` 在 `w = 0` 时会读到列表末尾（负下标），所以必须先判断 `w`，上面写成 `counts[w - 1] + 1 if w and … else 1`。字符串不可变，原地只能操作 `list(s)`，最后再 `"".join(…)`。
