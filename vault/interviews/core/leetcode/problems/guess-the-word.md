---
slug: guess-the-word
---
## Q
**LC 843 猜猜这个单词**｜Hard

`words` 里是互不相同的 6 字母单词，其中一个是秘密单词。`master.guess(w)` 返回 `w` 与秘密单词位置和字母都相同的个数。在限定次数（如 10 次）内猜中秘密单词。

## A
**一句话。** 极小化极大：候选集中每个词按「与其他候选的匹配数」分组，猜最坏情况下剩余候选最少的那个；得到匹配数 `k` 后，只保留与所猜词恰好匹配 `k` 位的候选。

```python
def find_secret_word(words, master):
    def match(a, b):
        return sum(x == y for x, y in zip(a, b))

    def worst(w):              # 猜 w 后最坏还剩几个候选
        groups = Counter(match(w, v) for v in cand)
        return max(groups.values())

    cand = words[:]
    while cand:
        guess = min(cand, key=worst)
        k = master.guess(guess)
        if k == 6:
            return
        cand = [w for w in cand if match(w, guess) == k]
```

**复杂度。** 每次猜测 `O(n²·6)`，空间 `O(n)`。

**易错点。**
- 随机猜：多数单词与秘密词匹配 0 位，返回 0 时排除得很少，随机策略可能超次数。
- 过滤时用 `>= k`：秘密词与所猜词恰好匹配 `k` 位，候选也必须恰好是 `k`。

**追问。**
- 为什么最坏分组要算上 `match = 6` 的那组？：那组只有所猜词自己，大小为 1，不影响最大值，写起来更简单。
- 更便宜的启发？：猜「与其他候选匹配 0 位的个数最少」的词，计算量相同但只看一组。

**同模式。** LC 704 二分查找、LC 375 猜数字大小 II
