---
id: tlc-longest-common-suffix-queries-2-code
node: p4.longest-common-suffix-queries
type: qa
step: 2
---
## Q
**LC 3093 最长公共后缀查询**｜写出 Python 实现

`wordsContainer` 与 `wordsQuery` 是小写字符串数组（各自 `1` 到 `10^4` 个，单词长 `1` 到 `5 * 10^3`，各自长度总和 `<= 5 * 10^5`）。对每个查询词，返回 `wordsContainer` 中与它有最长公共后缀的字符串的下标；并列时取长度最短的，再并列取下标最小的。

## A
**思路。** 容器单词反转后插入字典树，每个节点存经过它的单词中「最短、最早」的下标；根节点代表空后缀，也要存。查询词反向沿树走到不能再走为止，取停下节点上存的下标。

```python
def string_indices(words_container: list[str], words_query: list[str]) -> list[int]:
    nxt: list[dict[str, int]] = [{}]    # 反向字典树：nxt[u][c] 是节点 u 的孩子
    best: list[int] = [0]               # best[u]：经过 u 的容器单词里，最短且最早的下标

    def better(i: int, j: int) -> int:  # 长度短者胜；等长时下标小者胜
        return i if (len(words_container[i]), i) < (len(words_container[j]), j) else j

    for idx, word in enumerate(words_container):
        best[0] = better(idx, best[0])  # 根节点代表空后缀：所有单词都经过
        u = 0
        for ch in reversed(word):       # 从最后一个字符往前插入
            if ch not in nxt[u]:
                nxt[u][ch] = len(nxt)
                nxt.append({})
                best.append(idx)
            u = nxt[u][ch]
            best[u] = better(idx, best[u])

    ans: list[int] = []
    for q in words_query:
        u = 0
        for ch in reversed(q):          # 沿查询词的反向尽量往深走
            if ch not in nxt[u]:
                break
            u = nxt[u][ch]
        ans.append(best[u])             # 停下的节点就是最长公共后缀对应的节点
    return ans
```

运行：`["abcd","bcd","xbcd"]`，`["cd","bcd","xyz"]` → `[1, 1, 1]`；`["abcdefgh","poiuygh","ghghgh"]`，`["gh","acbfgh","acbfegh"]` → `[2, 0, 2]`；`["a"]`，`["b"]` → `[0]`；`["ab","ab"]`，`["ab"]` → `[0]`；`["bb","b"]`，`["a"]` → `[1]`。

**复杂度。** 时间 `O(Σ|容器| + Σ|查询|)`；空间 `O(Σ|容器|)`，节点数不超过容器总长度加一。

**写法要点。** 用两个并行列表 `nxt` 与 `best` 表示节点，比定义节点类省内存；节点编号就是 `len(nxt)`，创建时顺手 `append`；`reversed(word)` 是迭代器，不会复制字符串；`better` 用元组 `(长度, 下标)` 比较，一处写清「先短后早」；`best[0]` 单独更新，因为根不在字符循环里；`break` 之后 `u` 就停在最深的匹配节点。
