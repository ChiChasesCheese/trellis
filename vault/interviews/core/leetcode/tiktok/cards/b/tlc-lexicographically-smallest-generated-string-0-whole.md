---
id: tlc-lexicographically-smallest-generated-string-0-whole
node: b.lexicographically-smallest-generated-string
type: qa
---
## Q
**LC 3474 字典序最小的生成字符串**｜Hard · LC TikTok 热度 62/100

给两个字符串 `str1`（长度 `n`，只含 `'T'` 和 `'F'`）和 `str2`（长度 `m`，小写字母）。长度为 `n + m - 1` 的字符串 `word` 由它们生成，当且仅当对每个 `0 <= i <= n - 1`：若 `str1[i] == 'T'`，则 `word[i..i+m-1] == str2`；若 `str1[i] == 'F'`，则 `word[i..i+m-1] != str2`。返回可以生成的字典序最小的字符串，不存在则返回 `""`。`1 <= n <= 10^4`，`1 <= m <= 500`。例：`str1 = "TFTF", str2 = "ab"` → `"ababa"`；`str1 = "TFTF", str2 = "abc"` → `""`；`str1 = "F", str2 = "d"` → `"a"`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 先把所有 `'T'` 窗口的 `str2` 铺进去（重叠处字母冲突就无解），没被钉死的自由位先填最小的 `'a'`；再扫每个 `'F'` 窗口，若它恰好等于 `str2`，就把窗口里**最靠右**的自由位改成 `'b'`，窗口里没有自由位则无解。`O(n·m)`。

**识别。** `'T'` 是等式约束，直接铺；`'F'` 是不等式约束，只要窗口里有一位不同就满足。「字典序最小」意味着每个自由位尽量取 `'a'`，不得不改时，改动越靠后、字母越小，对字典序的损害越小。`n·m <= 5 * 10^6`，直接用切片比较就够。

**推导。** 暴力：在 `26^(n+m-1)` 个字符串里找，或逐位回溯，最坏指数级。观察：`'T'` 窗口钉死一部分位置；其余位置如果不受任何约束，最小是 `'a'`。`'F'` 窗口已经不等于 `str2` 就不用管；恰好等于时必须让某个自由位不同，该位当前是 `'a'`，下一个最小的字母是 `'b'`；在窗口的自由位里选最右的一个，因为较左的位保持 `'a'` 字典序更小。改动只会碰自由位，不会破坏 `'T'` 窗口；窗口右侧到末尾全被 `'T'` 钉死，也保证这次改动不会让更早的 `'F'` 窗口意外变回 `str2`。

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

**运行。** `("TFTF", "ab")` → `"ababa"`；`("TFTF", "abc")` → `""`；`("F", "d")` → `"a"`；`("TT", "aa")` → `"aaa"`；`("FFF", "a")` → `"bbb"`；`("F", "aa")` → `"ab"`；`("TFT", "aa")` → `""`。

**复杂度。** 时间 `O(n·m)`：铺 `'T'` 窗口最多 `n·m` 次赋值，检查 `'F'` 窗口每个一次 `O(m)` 的切片比较；空间 `O(n + m)`。

**易错点。**
- 铺 `'T'` 时不检查重叠冲突，直接覆盖：`("TT", "ab")` 会得到 `"aab"`，正确是 `""`。
- 改窗口里最左的自由位而不是最右：`("F", "aa")` 得 `"ba"`，正确是 `"ab"`。
- 改了被 `'T'` 钉死的位，会破坏 `'T'` 窗口；窗口里没有自由位时必须返回 `""`，比如 `("TFT", "aa")`。

**追问。**
- `m` 很大（如 `10^5`）时每个窗口比较 `O(m)` 太慢：用滚动哈希（rolling hash）或 Z 函数做 `O(1)` 比较，改动一位后只需修补哈希。
- 想验证答案：写一个按位回溯的暴力，从小到大试字母，在小数据上对照。
- 字母表只允许 `'a'`、`'b'`：此解法只用到这两个字母加上 `str2` 里的字母，不受影响。

**同模式。** LC 767 重构字符串、LC 316 去除重复字母、LC 936 戳印序列（按窗口约束构造）、LC 1202 交换字符串中的元素。
