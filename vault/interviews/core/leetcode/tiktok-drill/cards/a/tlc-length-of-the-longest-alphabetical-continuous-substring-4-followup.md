---
id: tlc-length-of-the-longest-alphabetical-continuous-substring-4-followup
node: a.length-of-the-longest-alphabetical-continuous-substring
type: qa
step: 4
---
## Q
**LC 2414 最长的字母序连续子字符串的长度**｜追问

面试官接着问：（1）怎么返回这个子串本身？（2）还有没有“按段分组”的写法？（3）如果 `z` 后面可以接 `a`（字母表首尾相接）呢？

## A
1. **返回子串**：用 `end` 记录当前最长段的结束下标，更新 `best` 时同时更新 `end`，最后 `s[end - best + 1 : end + 1]`。也可以在更新时记录起点 `start = i - run + 1`。
2. **按段分组**：在同一个连续段里，`ord(字符) - 下标` 是常数（字符每加一，下标也加一）。用 `groupby` 按这个键分组，最长组的长度就是答案：

```python
from itertools import groupby


def longest_continuous_substring_groupby(s: str) -> int:
    return max(len(list(group)) for _, group in groupby(enumerate(s), key=lambda p: ord(p[1]) - p[0]))
```

   `"abacaba"` → `2`，`"abcde"` → `5`，与逐对扫描的结果一致。这个写法的好处是：把“连续”换成别的等差关系（比如偶数连续）只需改 `key`。
3. **首尾相接**：延续条件改成 `(ord(cur) - ord(prev)) % 26 == 1`，此时 `"za"` 和 `"yzab"` 都算连续；如果字符串本身首尾相连（环），还要把末尾的段和开头的段合并，可以把 `s + s` 扫一遍，段长度上限取 `26`。

**Python 提醒**：`groupby` 只合并**相邻**的相同键，且它返回的分组是迭代器，要立刻消费（上面用了 `len(list(group))`），否则迭代到下一组时上一组的内容就失效了。`itertools.pairwise` 需要 Python 3.10+。
