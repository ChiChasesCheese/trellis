---
id: tlc-core-word-ladder
node: p3.word-ladder
type: qa
---
## Q
**LC 127 单词接龙**｜Hard · LC TikTok 热度 62/100 · 近一年被问：美国 2 次、国内 1 次 · CodeTop 国内累计 6 次 · 最近 2026-10-25（面试记录） · 也在：Amazon、NeetCode 150、Top Interview 150

字典 `wordList` 中从 `beginWord` 到 `endWord` 的**转换序列**是一个序列 `beginWord -> s1 -> s2 -> ... -> sk`：相邻两个单词只差一个字母；每个 `si`（`1 <= i <= k`）都在 `wordList` 中（`beginWord` 不需要在字典里）；`sk == endWord`。给 `beginWord`、`endWord` 和 `wordList`，返回从 `beginWord` 到 `endWord` 的**最短转换序列中的单词数目**；不存在则返回 `0`。

约束：`1 <= beginWord.length <= 10`，`endWord.length == beginWord.length`，`1 <= wordList.length <= 5000`，`wordList[i].length == beginWord.length`，所有单词由小写英文字母组成，`beginWord != endWord`，`wordList` 中的字符串互不相同。

例：`beginWord = "hit"`, `endWord = "cog"`, `wordList = ["hot","dot","dog","lot","log","cog"]` → `5`（`hit -> hot -> dot -> dog -> cog`）；去掉 `"cog"` 后 → `0`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 把单词看成图的顶点，只差一个字母的两个单词之间连边；「最少转换步数」就是无权图的最短路，用 BFS，一层一层扩展，第一次到达 `endWord` 时的层数就是答案。邻居用「逐位替换 26 个字母、看是否在字典里」生成，入队时就从集合里删掉，天然去重。

**识别。** 「每步只改一个字母 / 一次变换」+「最少步数」→ 隐式图上的 **BFS 最短路**；顶点是单词，边是「差一个字母」。看到「最短序列」「最少次数」「所有变换代价相同」就想到 BFS（而不是 DFS）。`N = 5000`、`L = 10`：`O(N²·L)` 的两两比较会到 `2.5·10^8`，需要换一种生成邻居的方式。

**推导。** 朴素建图：两两比较所有单词是否差一位，`O(N²·L) = 2.5·10^8`，太慢，只能勉强。改进：不建图，对当前单词直接枚举所有「一位变化」的候选 `L × 25` 个，用集合查询是否在字典，`O(L²·26)` 每个单词。BFS 要避免重复访问：把单词放在一个「未访问集合」里，发现就从集合移除并入队，这样每个单词最多入队一次。层数从 `1`（只有 `beginWord` 的序列长度为 `1`）起算，每处理完一层加 `1`，弹出 `endWord` 时的层数就是单词数。`endWord` 不在字典则直接返回 `0`。

```python
def ladder_length(begin_word: str, end_word: str, word_list: list[str]) -> int:
    words = set(word_list)             # 还没访问过的词典单词；O(1) 查询
    if end_word not in words:
        return 0
    queue = deque([begin_word])
    steps = 1                          # 当前这一层的单词所在的序列长度
    while queue:
        for _ in range(len(queue)):    # 一次处理完整的一层
            word = queue.popleft()
            if word == end_word:
                return steps
            for i in range(len(word)):
                for ch in string.ascii_lowercase:
                    nxt = word[:i] + ch + word[i + 1:]
                    if nxt in words:
                        words.remove(nxt)          # 入队即标记已访问，防止重复入队
                        queue.append(nxt)
        steps += 1
    return 0
```

运行：`"hit" → "cog", ["hot","dot","dog","lot","log","cog"]` → `5`，`"hit" → "cog", ["hot","dot","dog","lot","log"]` → `0`，`"a" → "c", ["a","b","c"]` → `2`，`"hot" → "dot", ["dot"]` → `2`，`"aaa" → "ccc"，有捷径的小字典` → `4`，`5000 个长度为 10 的单词，终点孤立（BFS 要遍历全部可达单词）` → `0`。

**复杂度。** 时间 `O(N · L · 26 · L)`：每个单词最多入队一次，对它的 `L` 个位置各试 26 个字母，每个候选拼接字符串和哈希查询各 `O(L)`；`N = 5000`、`L = 10` 约 `1.3·10^6` 个候选、`10^7` 级字符操作，远低于一秒。空间 `O(N · L)`。

**易错点。**
- 把边数当单词数：`hit -> cog` 的最短序列有 `5` 个单词、`4` 步；若从 `0` 起算层数，得到 `4`。题目要的是单词数，起点自己算一个。
- DFS 代替 BFS：DFS 找到的第一条路径不一定最短。`aaa -> ccc`，字典 `[aab,abb,bbb,bbc,bcc,ccc,aac,acc]`，最短是 `4`（`aaa -> aac -> acc -> ccc`），DFS 沿着 `aab -> abb -> ...` 一路深入，实际返回 `8`。
- 标记访问放在出队时：同一单词可能被多个单词在同一层入队多次，队列膨胀、时间显著变慢；应当入队时就标记（这里是从集合 `remove`）。
- 忘了 `beginWord` 不一定在字典里：不能要求 `beginWord in words`，也不要把它当作字典单词检查；而 `endWord` 必须在字典里，否则直接 `0`。

**追问。**
- 要返回所有最短序列（LC 126 单词接龙 II）：BFS 记录每个单词的层数和所有前驱，再从终点 DFS 回溯；或双向 BFS 加回溯。
- 字典很大、查询很多：预处理「通配符桶」`h*t`、`*ot`、`ho*` → 单词列表，邻居变成「所在桶里的其它单词」，每个单词只生成 `L` 个键而不是 `26L` 个候选；字符集很大时更划算。
- 起点终点相距很远、分支很多：双向 BFS，每次扩展较小的一侧，搜索量从 `b^d` 降到约 `2·b^(d/2)`；见「另一种解法」。

**同模式。** LC 126 单词接龙 II、LC 433 最小基因变化、LC 752 打开转盘锁、LC 1306 跳跃游戏 III、LC 773 滑动谜题（同样是隐式图 BFS）。
