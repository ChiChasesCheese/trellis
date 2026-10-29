---
id: tlc-substring-with-concatenation-of-all-words-0-whole
node: a.substring-with-concatenation-of-all-words
type: qa
---
## Q
**LC 30 串联所有单词的子串**｜Hard · 字节高频

给字符串 `s` 和字符串数组 `words`，`words` 里所有单词**长度相同**。「串联子串」是 `s` 中恰好由 `words` 的所有单词按**任意顺序**首尾相接而成的子串（`words` 里的重复单词要按次数都用上）。返回所有串联子串的起始下标，顺序任意。`1 <= s.length <= 10^4`，`1 <= words.length <= 5000`，`1 <= words[i].length <= 30`，`words[i]` 和 `s` 由小写英文字母组成。

例：`s = "barfoothefoobarman"`，`words = ["foo","bar"]` → `[0,9]`；`s = "wordgoodgoodgoodbestword"`，`words = ["word","good","best","word"]` → `[]`；`s = "barfoofoobarthefoobarman"`，`words = ["bar","foo","the"]` → `[6,9,12]`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 把单词当作「大字母」做定长滑动窗口：窗口长度恰好 `k` 个单词（`k = len(words)`），步长是单词长度 `w`；起点只可能有 `w` 种余数，所以对每个起点偏移 `0..w-1` 各扫一遍，用 `Counter` 记窗口内各单词个数，某个单词超额就从左端吐出单词，窗口恰有 `k` 个单词时记录左端。`O(n * w)`。

**识别。**
- 「所有单词等长」→ 可以按固定步长 `w` 切分，把字符串看成单词序列。
- 「任意顺序拼接」→ 不是排列问题，是**多重集合相等**：窗口里各单词的个数等于 `words` 里各单词的个数（`Counter`）。
- 「串联子串长度固定为 `k * w`」→ 定长窗口；窗口一个单词一个单词地滑，滑动窗口的左端也只进不退。

**推导。** 暴力：枚举 `words` 的全排列，每个排列在 `s` 中找位置，`k!` 不行。第二版：对每个起点 `i`，切出 `k` 个单词用 `Counter` 比较，`O(n * k * w)`，最坏 `n = 10^4` 乘窗口总长 `10^4`，约 `10^8` 次字符操作，且相邻起点重复切分。浪费在于起点 `i` 和 `i + w` 的窗口共享 `k - 1` 个单词。起点按余数 `i mod w` 分成 `w` 个互不相交的序列，每个序列里窗口每次向右挪一个单词：吃进右边一个、必要时吐出左边的，每个单词进出各一次。总工作量 `w` 个偏移 x 每个偏移 `n / w` 个单词 x 每次切片 `O(w)`，即 `O(n * w)`。

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

运行：示例 1 → `[0, 9]`，示例 2 → `[]`，示例 3 → `[6, 9, 12]`，`s = "a", words = ["ab"]` → `[]`，`s = "aaa", words = ["a","a"]` → `[0, 1]`，`s = "a" * 10000, words = ["a"] * 5000` → 5001 个下标，约 0.002 秒。

**复杂度。** 时间 `O(n * w)`（每个偏移扫 `n / w` 个单词，每个单词的切片、哈希、进出窗口都是 `O(w)`），`n = 10^4, w = 30` 时约 `3 * 10^5`；空间 `O(k * w)`（`need` 保存 `words` 的不同单词）。

**易错点。**
- 只扫偏移 0：串联子串可以从任意位置开始。`s = "xfoobar", words = ["foo","bar"]` 只扫偏移 0 返回 `[]`，正确 `[1]`。
- 只看「单词是否出现过」不计次数：`s = "foofoo", words = ["foo","bar"]` 返回 `[0]`，正确 `[]`。重复单词（示例 2 的 `"word"` 两次）也必须按次数用 `Counter`。
- 窗口里出现不在 `words` 里的单词时没有整体清空，会把前面攒的计数带进下一段。

**追问。**
- 单词长度不一样：定长切分失效，用 Trie / Aho-Corasick 匹配加回溯或 DP。
- 每个位置的切片重复分配字符串：先把 `s` 里每个位置的单词映射成整数编号，再在整数上滑窗，省去重复哈希字符串。
- 只要个数不要下标：`len(find_substring(s, words))`，无需保存列表。

**同模式。** LC 76 最小覆盖子串、LC 438 找到字符串中所有字母异位词、LC 567 字符串的排列、LC 3 无重复字符的最长子串。
