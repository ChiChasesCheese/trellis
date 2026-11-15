---
slug: find-and-replace-pattern
---
## Q
**LC 890 查找和替换模式**｜Medium

给单词数组 `words` 和模式串 `pattern`，返回能与 `pattern` 匹配的单词：存在字母的一一映射（双射），把 `pattern` 的每个字母换掉后恰好得到该单词。

## A
**一句话。** 逐字符建立双向映射：`pattern → word` 与 `word → pattern` 都不能冲突，才是一一对应。

```python
def find_and_replace_pattern(words, pattern):
    def match(w):
        a, b = {}, {}                 # 双向映射：必须是双射
        for x, y in zip(w, pattern):
            if (a.setdefault(x, y) != y
                    or b.setdefault(y, x) != x):
                return False
        return True
    return [w for w in words if match(w)]
```

**复杂度。** 时间 `O(nL)`，空间 `O(L)`（`n` 个单词，每个长 `L`）。

**易错点。**
- 只建单向映射：`"abb"` 与 `"mee"` 对，但 `"abc"` 与 `"mee"` 也会被误判成对，两个不同字母不能映成同一个。
- 用 `dict[x] = y` 直接覆盖：冲突被悄悄吞掉，要先查已有映射是否一致。

**追问。**
- 有更简洁的写法吗？：把每个串规范化成「每个字母第一次出现的编号序列」，相等就匹配。

**同模式。** LC 205 同构字符串、LC 290 单词规律、LC 291 单词规律 II
