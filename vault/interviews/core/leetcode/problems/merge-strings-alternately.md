---
slug: merge-strings-alternately
---
## Q
**LC 1768 交替合并字符串**｜Easy

交替取 `word1`、`word2` 的字母合并，较长者多出的部分接在末尾。

## A
**一句话。** `zip` 交替取到较短者结束，再把较长者的尾巴整体接上。

```python
def merge_alternately(word1, word2):
    n = min(len(word1), len(word2))
    head = "".join(a + b for a, b in zip(word1, word2))
    return head + word1[n:] + word2[n:]   # 另一个切片是空串
```

**复杂度。** 时间 `O(n+m)`，空间 `O(n+m)`。

**易错点。**
- 忘了追加尾巴：`("ab","pqrs")` 得 `"apbq"`，应为 `"apbqrs"`。
- 循环里用 `+=` 拼字符串：`O(n²)` 隐患，用 `"".join`。

**追问。**
- 合并 `k` 个字符串？：`zip_longest(*words, fillvalue="")` 按列轮流取。
- 输入是流怎么办？：写成生成器逐字符产出。

**同模式。** LC 88 合并两个有序数组、LC 21 合并两个有序链表、LC 2 两数相加
