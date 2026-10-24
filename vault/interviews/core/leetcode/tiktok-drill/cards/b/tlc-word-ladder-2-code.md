---
id: tlc-word-ladder-2-code
node: b.word-ladder
type: qa
step: 2
---
## Q
**LC 127 单词接龙**｜写出 Python 实现

`beginWord`、`endWord`（长度相同，`1..10`，小写字母，互不相同）和字典 `wordList`（`1..5000` 个互不相同、同样长度的单词）。每步只能把一个字母换成另一个字母，且换出的单词必须在字典里。返回最短转换序列的单词个数（含起点和终点），无解返回 `0`。

## A
**思路。** 词典放进集合 `words`，既用来判断「候选单词是否合法」，也兼作「未访问集合」。BFS 从 `begin_word` 开始，一层一层处理；对每个单词，逐位替换成 26 个字母，若候选在 `words` 里就从集合中删除并入队。弹出 `end_word` 时返回当前层号 `steps`（单词个数），队列空了仍没遇到则返回 `0`。

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

**写法要点。** `set` 的 `in` 和 `remove` 都是 `O(1)`，把「合法性」和「访问标记」合并成一个结构；`for _ in range(len(queue))` 先固定本层大小，再处理，这是按层 BFS 的标准写法，层数自然得到；`word[:i] + ch + word[i + 1:]` 构造新单词；`string.ascii_lowercase` 提供 26 个字母；`deque` 的 `popleft` 是 `O(1)`，列表的 `pop(0)` 是 `O(n)`，不能用。
