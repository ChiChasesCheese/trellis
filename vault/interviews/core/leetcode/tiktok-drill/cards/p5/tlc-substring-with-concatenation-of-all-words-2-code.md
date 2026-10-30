---
id: tlc-substring-with-concatenation-of-all-words-2-code
node: p5.substring-with-concatenation-of-all-words
type: qa
step: 2
---
## Q
**LC 30 串联所有单词的子串**｜写出 Python 实现

`s` 长度 `1..10^4`，`words` 有 `1..5000` 个等长单词（长度 `1..30`），都由小写字母组成。返回 `s` 中所有串联子串（`words` 所有单词任意顺序首尾相接，重复单词按次数）的起始下标，顺序任意。

## A
**思路。** 单词长度 `w`，单词个数 `k`。对每个偏移 `off` 单独扫描，每次吃进一个单词：不在 `words` 里则清空窗口；某个单词超额则左端吐单词直到不超；窗口恰有 `k` 个单词则记录左端并吐出最左一个继续滑。

```python
from collections import Counter

def find_substring(s: str, words: list[str]) -> list[int]:
    w, k, n = len(words[0]), len(words), len(s)
    need = Counter(words)                            # 要凑的单词及次数（words 里可能有重复）
    ans: list[int] = []
    for off in range(w):                             # 窗口起点只可能与 off 同余 w，逐个余数各扫一遍
        have: Counter[str] = Counter()               # 当前窗口 s[left : right] 里各单词的个数
        left = off
        for right in range(off, n - w + 1, w):       # 每步吃进一个单词 s[right : right + w]
            word = s[right:right + w]
            if word not in need:
                have.clear()                         # 遇到不在 words 里的单词：窗口整体作废
                left = right + w
                continue
            have[word] += 1
            while have[word] > need[word]:           # 某个单词多了：左端吐单词直到不超
                have[s[left:left + w]] -= 1
                left += w
            if right + w - left == k * w:            # 恰好 k 个单词且没有超额 => 与 words 一致
                ans.append(left)
                have[s[left:left + w]] -= 1          # 吐出最左一个，继续往右滑
                left += w
    return ans
```

运行：`"barfoothefoobarman"` + `["foo","bar"]` → `[0, 9]`；`"wordgoodgoodgoodbestword"` + `["word","good","best","word"]` → `[]`；`"barfoofoobarthefoobarman"` + `["bar","foo","the"]` → `[6, 9, 12]`；`"a"` + `["ab"]` → `[]`；`"aaa"` + `["a","a"]` → `[0, 1]`。

**复杂度。** 时间 `O(n * w)`：`w` 个偏移，每个偏移扫 `n / w` 个单词，每个单词进出窗口各一次，每次切片和哈希 `O(w)`；空间 `O(k * w)`。

**写法要点。** `Counter(words)` 一步统计重复；`Counter[str]` 的 `[]` 读取缺失键返回 0 且不插入，`have[word] > need[word]` 不会因 `need` 缺键而异常；`range(off, n - w + 1, w)` 让切片 `s[right:right + w]` 永远不越界；多个偏移的结果可能不是升序，题目不要求顺序，需要时再 `sorted`。
