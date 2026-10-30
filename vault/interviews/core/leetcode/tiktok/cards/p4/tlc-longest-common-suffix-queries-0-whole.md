---
id: tlc-longest-common-suffix-queries-0-whole
node: p4.longest-common-suffix-queries
type: qa
---
## Q
**LC 3093 最长公共后缀查询**｜Hard · 近一年被问：美国 1 次、国内 0 次 · 最近 2026-07-02（美国面试记录）

给两个字符串数组 `wordsContainer` 和 `wordsQuery`。对每个 `wordsQuery[i]`，在 `wordsContainer` 中找一个与它有最长公共后缀的字符串；如果有多个，取长度最短的；长度也相同，取在 `wordsContainer` 中下标最小的。返回数组 `ans`，`ans[i]` 是对应的下标（没有任何公共后缀时，公共后缀是空串，所有容器字符串都满足，按同样的规则选）。`1 <= wordsContainer.length, wordsQuery.length <= 10^4`，`1 <= wordsContainer[i].length <= 5 * 10^3`，`1 <= wordsQuery[i].length <= 5 * 10^3`，字符串只含小写英文字母，`wordsContainer[i].length` 的总和和 `wordsQuery[i].length` 的总和都至多为 `5 * 10^5`。例：`wordsContainer = ["abcd","bcd","xbcd"]`，`wordsQuery = ["cd","bcd","xyz"]` → `[1,1,1]`；`wordsContainer = ["abcdefgh","poiuygh","ghghgh"]`，`wordsQuery = ["gh","acbfgh","acbfegh"]` → `[2,0,2]`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 把容器里的每个单词反转后插入字典树（Trie），每个节点存「经过它的单词中最短、最早的下标」；每个查询也反向走树，尽量往深走，停下的节点里存的下标就是答案。`O(Σ|容器| + Σ|查询|)`。

**识别。** 「最长公共后缀」把单词反转就是「最长公共前缀」，是字典树的典型场景；查询多、总长度只有 `5 * 10^5`，说明要预处理一次、每个查询只花自己长度的时间；平局规则（最短、最早）要预存在节点上，查询时不能再去收集候选。

**推导。** 暴力：每个查询和每个容器词逐字符比后缀，`O(Q * C * L)`，最坏 `10^4 * 10^4 * 5 * 10^3` → 太大。换成把所有后缀放进哈希表，总成本是每个词长度的平方和，一个长 `5000` 的词就有 `1250` 万个字符的后缀，仍然不可行 → 浪费：不同词的后缀大量共享前缀（反转后），逐个存是重复劳动 → 洞察：反转后的 Trie 里，从根到某节点的路径恰好是一个后缀，共享部分只存一份；每个节点预存最优代表（长度短者胜，等长保留更早的），因为按下标顺序插入，只在严格更短时才替换，就自然满足「最早」；根节点代表空后缀，所有单词都经过它，所以没有任何公共字符时答案是全局最短最早。

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

运行：示例 1 → `[1, 1, 1]`，示例 2 → `[2, 0, 2]`；`(["a"], ["b"])` → `[0]`；`(["ab","ab"], ["ab"])` → `[0]`；`(["bb","b"], ["a"])` → `[1]`；容器 `100` 个长 `5000` 的随机词、`100` 个同样长的查询约 `0.3` 秒。

**复杂度。** 时间 `O(Σ|容器| + Σ|查询|)`，每个字符一次字典操作；空间 `O(Σ|容器|)`，最多约 `5 * 10^5` 个节点。

**易错点。**
- 忘了更新根节点的代表：没有公共字符的查询会返回 `best[0]` 的初值 `0`。示例 1 的 `"xyz"` 会得到 `0`，正确是 `1`。
- 节点只记第一个经过的单词、不比长度：示例 1 会得到 `[0, 0, 0]`，正确是 `[1, 1, 1]`。
- 平局比较写成 `<=`：后插入的同长单词会覆盖更早的，`(["ab","ab"], ["ab"])` 得到 `1`，正确是 `0`。

**追问。**
- 内存：节点数可达 `5 * 10^5`，每个节点一个字典开销最大；可以改成一个字典，键为 `节点编号 * 26 + 字符编号`。
- 单词要动态增删：节点上的「最优代表」不能只存一个，要存按（长度，下标）排序的堆或有序集合。
- 把「后缀」换成「前缀」：不反转直接插入和查询，其余完全一样。

**同模式。** LC 208 实现 Trie（前缀树）、LC 1032 字符流（反向 Trie 找后缀）、LC 648 单词替换、LC 14 最长公共前缀、LC 720 词典中最长的单词。
