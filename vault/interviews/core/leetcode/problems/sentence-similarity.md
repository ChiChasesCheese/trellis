---
slug: sentence-similarity
---
## Q
**LC 734 句子相似性**｜Easy

两个句子是单词数组 `sentence1`、`sentence2`，再给相似单词对 `similarPairs`。两句相似当且仅当长度相同，且对应位置的单词相同或是一个相似对（相似关系不传递）。

## A
**一句话。** 把相似对放进集合，逐位比较：相同或 `(a, b)`、`(b, a)` 之一在集合里。

```python
def are_sentences_similar(s1, s2, pairs):
    if len(s1) != len(s2):
        return False
    ok = {(a, b) for a, b in pairs}
    return all(a == b or (a, b) in ok or (b, a) in ok
               for a, b in zip(s1, s2))
```

**复杂度。** 时间 `O(n + p)`，空间 `O(p)`。

**易错点。**
- 只查一个方向：相似对 `(a, b)` 是无序的，两个方向都要查。
- 忘了长度检查：`zip` 会悄悄截断，长度不同也会判相似。

**追问。**
- 相似关系可传递（LC 737）？：用并查集，把每个相似对并起来，比较两个单词的根。

**同模式。** LC 737 句子相似性 II、LC 1813 句子相似性 III、LC 205 同构字符串
