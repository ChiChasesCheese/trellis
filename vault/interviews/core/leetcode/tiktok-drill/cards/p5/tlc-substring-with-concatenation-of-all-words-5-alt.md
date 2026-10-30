---
id: tlc-substring-with-concatenation-of-all-words-5-alt
node: p5.substring-with-concatenation-of-all-words
type: qa
step: 5
---
## Q
**LC 30 串联所有单词的子串**｜另一种解法

不用滑动窗口，直接对每个起点检查，能不能过？它的最坏复杂度是多少，什么时候选它？

## A
**做法。** 枚举每个起点 `i`，从 `i` 起按步长 `w` 取 `k` 个单词，边取边计数；某个单词的计数超过 `need` 就提前跳出，`for ... else` 里全部取完才记录。
```python
from collections import Counter

def find_substring_brute(s: str, words: list[str]) -> list[int]:
    w, k = len(words[0]), len(words)
    need = Counter(words)
    ans: list[int] = []
    for i in range(len(s) - k * w + 1):
        seen: Counter[str] = Counter()
        for j in range(i, i + k * w, w):
            word = s[j:j + w]
            seen[word] += 1
            if seen[word] > need[word]:              # need 里没有的词计数为 0，一并被拦下
                break
        else:
            ans.append(i)                            # 没有 break：k 个单词都合法
    return ans
```
示例 1、2、3 的输出与滑窗版相同：`[0, 9]`、`[]`、`[6, 9, 12]`。

**复杂度。** 最坏 `O(n * k * w)`，起点数 `n - k*w + 1` 乘每个起点 `k` 次切片，每次 `O(w)`。对抗输入：`s = "a" * 10000`，`words = ["a"] * 4999 + ["b"]`，每个起点都要扫近 5000 步才失败，约 1.7 秒；滑窗版同输入约 0.001 秒。

**怎么选。** 数据小、或面试时间紧先写它，十行写对且好验证；一旦 `k * w` 接近 `n`，或者 `words` 很长，就换滑窗版。滑窗版的代价是偏移循环和吐词逻辑更容易写错，所以可以先用这个版本当参照。
