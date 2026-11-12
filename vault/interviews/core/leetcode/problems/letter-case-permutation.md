---
slug: letter-case-permutation
---
## Q
**LC 784 字母大小写全排列**｜Easy

把字符串 `s` 中每个字母任意变大写或小写（数字不变），返回所有可能的字符串。

## A
**一句话。** 按位置回溯：每位保持原样，若是字母再多一个翻转大小写的分支。

```python
def letter_case_permutation(s):
    res = []
    path = list(s)                # 原地改，回溯时还原

    def dfs(i):
        if i == len(path):
            res.append("".join(path))
            return
        dfs(i + 1)                # 保持原样
        if path[i].isalpha():     # 字母才有第二个分支
            path[i] = path[i].swapcase()
            dfs(i + 1)
            path[i] = path[i].swapcase()

    dfs(0)
    return res
```

**复杂度。** 时间 `O(2^m · n)`（`m` 为字母数），空间 `O(n)`。

**易错点。**
- 数字也分两支：`"3z4"` 会得 8 个字符串（重复），应为 `2` 个。
- 叶子处 `res.append(path)` 不 `join`：存的是同一个列表引用，最后全变成一样。

**追问。**
- 不用递归？：`product(*[(c.lower(), c.upper()) if c.isalpha() else (c,) for c in s])`。
- 只要个数？：`2 ** 字母个数`。

**同模式。** LC 78 子集、LC 17 电话号码的字母组合、LC 22 括号生成、LC 1239 串联字符串的最大长度
