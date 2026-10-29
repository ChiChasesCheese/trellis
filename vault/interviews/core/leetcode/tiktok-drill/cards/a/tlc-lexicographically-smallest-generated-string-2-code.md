---
id: tlc-lexicographically-smallest-generated-string-2-code
node: a.lexicographically-smallest-generated-string
type: qa
step: 2
---
## Q
**LC 3474 字典序最小的生成字符串**｜写出 Python 实现

`str1` 只含 `'T'`、`'F'`，长度 `n`（`1..10^4`）；`str2` 为小写字母串，长度 `m`（`1..500`）。长度 `n + m - 1` 的字符串 `word` 满足：`str1[i] == 'T'` 时 `word[i..i+m-1] == str2`，`'F'` 时不相等。返回字典序最小的 `word`，无解返回 `""`。

## A
**思路。** 用列表 `word` 记录被 `'T'` 钉死的字母，重叠处冲突就返回 `""`。自由位先填 `'a'`。再扫每个 `'F'` 窗口：若恰好等于 `str2`，改窗口里最靠右的自由位为 `'b'`；没有自由位则返回 `""`。

```python
def generate_string(str1: str, str2: str) -> str:
    n, m = len(str1), len(str2)
    word: list[str | None] = [None] * (n + m - 1)      # None 表示这一位还没有被 'T' 钉死
    for i, flag in enumerate(str1):
        if flag != "T":
            continue
        for j, ch in enumerate(str2):                  # 把 str2 铺到 [i, i+m)
            if word[i + j] not in (None, ch):          # 两个 'T' 窗口在重叠处要求不同字母：无解
                return ""
            word[i + j] = ch
    forced = [ch is not None for ch in word]           # 被 'T' 钉死的位置不能再动
    res = [ch or "a" for ch in word]                   # 自由位先填最小字母 'a'
    for i, flag in enumerate(str1):
        if flag == "F" and res[i : i + m] == list(str2):   # 'F' 窗口不小心等于 str2：必须改一位
            for j in range(i + m - 1, i - 1, -1):          # 改窗口里最靠右的自由位，对字典序伤害最小
                if not forced[j]:
                    res[j] = "b"
                    break
            else:
                return ""                                  # 窗口里全是被钉死的位：无解
    return "".join(res)
```

**运行。** `("TFTF", "ab")` → `"ababa"`；`("TFTF", "abc")` → `""`；`("F", "d")` → `"a"`；`("TT", "aa")` → `"aaa"`；`("FFF", "a")` → `"bbb"`；`("T", "z")` → `"z"`。

**复杂度。** 时间 `O(n·m)`：铺 `'T'` 与检查 `'F'` 各至多 `n·m` 个字符操作；空间 `O(n + m)`。

**写法要点。** `word[i + j] not in (None, ch)` 一次判断「已有且不同」；`ch or "a"` 把 `None` 变成 `'a'`（字母都是非空字符串，不会误判）；`forced` 单独保存「是否被钉死」，因为填完 `'a'` 以后无法再区分；`for … else` 的 `else` 只在内层循环没有 `break`（没找到自由位）时执行，正好表达「无解」；`res[i : i + m] == list(str2)` 用列表切片比较，避免每次 `"".join`。
