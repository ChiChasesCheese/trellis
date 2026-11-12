---
slug: longest-common-suffix-queries
---
## Q
**LC 3093 最长公共后缀查询**｜Hard

对每个查询词，在容器里找与它公共后缀最长的词；并列取最短，再并列取下标最小。返回下标数组。

## A
**一句话。** 容器单词反转后建字典树，节点存经过它的最短最早的下标，查询反向走到尽头取该节点的值。

```python
def string_indices(words_container, words_query):
    nxt = [{}]      # 反向字典树
    best = [0]      # best[u]：经过 u 的最短最早下标

    def better(i, j):   # 短者胜，等长则下标小者胜
        a, b = words_container[i], words_container[j]
        return i if (len(a), i) < (len(b), j) else j

    for idx, word in enumerate(words_container):
        best[0] = better(idx, best[0])  # 根：空后缀
        u = 0
        for ch in reversed(word):
            if ch not in nxt[u]:
                nxt[u][ch] = len(nxt)
                nxt.append({})
                best.append(idx)
            u = nxt[u][ch]
            best[u] = better(idx, best[u])

    ans = []
    for q in words_query:
        u = 0
        for ch in reversed(q):
            if ch not in nxt[u]:
                break
            u = nxt[u][ch]
        ans.append(best[u])     # 停下的节点就是最长公共后缀
    return ans
```

**复杂度。** 时间 `O(Σ|容器| + Σ|查询|)`，空间 `O(Σ|容器|)`。

**易错点。**
- 忘了更新根节点的代表：没有公共字符的查询返回初值 `0`，示例 1 的 `"xyz"` 得 `0`，应为 `1`。
- 节点只记第一个经过的单词、不比长度：示例 1 得 `[0,0,0]`，应为 `[1,1,1]`。
- 平局比较写成 `<=`：后插入的同长词覆盖更早的，`(["ab","ab"], ["ab"])` 得 `1`，应为 `0`。

**追问。**
- 内存太大怎么办？：节点数可达 `5·10^5`，一个字典存所有边，键为 `节点编号*26 + 字符`。
- 改成最长公共前缀？：不反转，其余完全一样。

**同模式。** LC 208 实现 Trie、LC 1032 字符流、LC 648 单词替换、LC 14 最长公共前缀
