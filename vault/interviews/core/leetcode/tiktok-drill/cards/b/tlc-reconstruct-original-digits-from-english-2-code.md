---
id: tlc-reconstruct-original-digits-from-english-2-code
node: b.reconstruct-original-digits-from-english
type: qa
step: 2
---
## Q
**LC 423 从英文中重建数字**｜写出 Python 实现

字符串 `s`（长度 `1 ~ 10^5`）是把若干个英文数字单词（`zero` ~ `nine`）的字母全部打乱后拼起来的结果，保证合法。返回其中出现的数字，升序排列、重复的写多次。

## A
**思路。** 用 `Counter` 数出每个字母的个数，再按固定顺序处理十个数字：每一步中，识别字母的当前计数就是该数字的个数 `k`；然后把这 `k` 个单词包含的所有字母从计数里扣掉，使后面的字母变得唯一。最后按数字升序把每个数字重复 `k` 次拼成字符串。

```python
def original_digits(s: str) -> str:
    # (数字, 英文单词, 识别它的字母)：顺序保证识别字母在轮到它时已经唯一
    steps = [
        (0, "zero", "z"), (2, "two", "w"), (4, "four", "u"), (6, "six", "x"), (8, "eight", "g"),
        (3, "three", "h"), (5, "five", "f"), (7, "seven", "s"), (1, "one", "o"), (9, "nine", "i"),
    ]
    cnt = Counter(s)
    digits = [0] * 10
    for digit, word, key in steps:
        k = cnt[key]                          # 此刻 key 字母只可能来自这个数字
        digits[digit] = k
        for ch, m in Counter(word).items():   # 把这 k 个单词用掉的字母全部扣掉
            cnt[ch] -= k * m
    return "".join(str(d) * c for d, c in enumerate(digits))
```

运行：`"owoztneoer"` → `'012'`，`"fviefuro"` → `'45'`，`"nineeightsix"` → `'689'`，`"eon"` → `'1'`，`"zeroonetwothreefourfivesixseveneightnine"` → `'0123456789'`。

**复杂度。** 时间 `O(n)`：一次 `Counter(s)`，之后 10 步每步只处理固定的几个字母；空间 `O(1)`（字母表 15 个，数字 10 个）。

**写法要点。** `Counter(s)` 一行计数，缺失的字母读出来是 `0` 而不会 `KeyError`。`steps` 用三元组把数字、单词、识别字母放在一起，顺序即算法，改单词表只改这里。`Counter(word).items()` 处理单词里字母重复（`three` 有两个 `e`）：扣减量是 `k * m`。`"".join(str(d) * c for d, c in enumerate(digits))` 用 `enumerate` 按数字升序展开，天然满足「升序」。
