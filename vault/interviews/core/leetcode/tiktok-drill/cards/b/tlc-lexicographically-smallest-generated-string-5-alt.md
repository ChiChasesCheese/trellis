---
id: tlc-lexicographically-smallest-generated-string-5-alt
node: b.lexicographically-smallest-generated-string
type: qa
step: 5
---
## Q
**LC 3474 字典序最小的生成字符串**｜另一种解法

不做「铺 `'T'`、填 `'a'`、修补 `'F'`」的贪心，直接按定义搜索怎么写？适用范围是什么？

## A
**思路。** 逐位回溯：从第 0 位起，按字母从小到大尝试每个候选字母；每写完一位，检查刚好写满的那个窗口是否与 `str1` 的要求一致。第一条走到末尾的路径就是字典序最小的答案。候选字母只需取 `'a'`、`'b'` 和 `str2` 里出现的字母。

```python
def generate_string_dfs(str1: str, str2: str) -> str:
    n, m = len(str1), len(str2)
    alphabet = sorted(set(str2) | {"a", "b"})    # 答案只会用到 'a'、'b' 和 str2 里的字母
    word: list[str] = []

    def window_ok(start: int) -> bool:           # 以 start 开头的窗口刚写完，检查它和 str1[start] 是否一致
        return ("".join(word[start : start + m]) == str2) == (str1[start] == "T")

    def dfs() -> bool:
        p = len(word)
        if p == n + m - 1:
            return True
        for ch in alphabet:                      # 从小到大试：第一条走通的路径就是字典序最小
            word.append(ch)
            start = p - m + 1
            if (start < 0 or start >= n or window_ok(start)) and dfs():
                return True
            word.pop()
        return False

    return "".join(word) if dfs() else ""
```

`("TFTF", "ab")` → `"ababa"`；`("TFTF", "abc")` → `""`；`("F", "d")` → `"a"`。

**取舍。** 最坏情况指数级（无解时要把所有分支走完），递归深度是 `n + m - 1`，大数据会爆栈；只适合 `n + m` 不超过十来位的小输入。它不依赖任何贪心结论，正确性一眼可见，所以最适合在小数据上和 `O(n·m)` 的贪心对照。正式解答用贪心。
