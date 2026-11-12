---
slug: reconstruct-original-digits-from-english
---
## Q
**LC 423 从英文中重建数字**｜Medium

字符串 `s` 是若干数字英文单词（`zero`~`nine`）打乱字母后拼成的，按升序返回原始数字串。

## A
**一句话。** 先用独一无二的字母数出 0、2、4、6、8，再按「剩下唯一」的字母依次数 3、5、7、1、9，每次扣掉整词字母。

```python
def original_digits(s):
    # (数字, 单词, 此刻唯一的识别字母)；顺序不能乱
    steps = [(0, "zero", "z"), (2, "two", "w"),
             (4, "four", "u"), (6, "six", "x"),
             (8, "eight", "g"), (3, "three", "h"),
             (5, "five", "f"), (7, "seven", "s"),
             (1, "one", "o"), (9, "nine", "i")]
    cnt = Counter(s)
    res = [0] * 10
    for d, word, key in steps:
        k = cnt[key]
        res[d] = k
        for ch, m in Counter(word).items():
            cnt[ch] -= k * m       # 扣掉这 k 个单词的全部字母
    return "".join(str(d) * c for d, c in enumerate(res))
```

**复杂度。** 时间 `O(n)`，空间 `O(1)`。

**易错点。**
- 识别顺序错：先数 `one`（用 `o`），`o` 还混在 `zero`、`two`、`four` 里，`"owoztneoer"` 得 `01112`，应为 `012`。
- 只扣识别字母不扣整词：`e`、`r`、`o` 残留，后面的 `h`、`s`、`i` 就不唯一。
- 按识别顺序拼结果：要按数字 0~9 的下标顺序展开。

**追问。**
- 词表换了怎么找顺序？：反复找「只在剩余一个单词里出现」的字母，识别后剥离。

**同模式。** LC 242 有效的字母异位词、LC 387 字符串中的第一个唯一字符、LC 1189「气球」的最大数量、LC 389 找不同
