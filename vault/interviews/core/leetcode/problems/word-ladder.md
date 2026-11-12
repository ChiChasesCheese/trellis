---
slug: word-ladder
---
## Q
**LC 127 单词接龙**｜Hard

每步只能改一个字母，且结果必须在 `wordList` 中。求从 `beginWord` 到 `endWord` 的最短转换序列的单词数，不存在返回 `0`。

## A
**一句话。** 单词为点、差一个字母为边，对无权图做 BFS，逐位试 26 个字母生成邻居。

```python
def ladder_length(begin_word, end_word, word_list):
    words = set(word_list)       # 未访问的词典单词
    if end_word not in words:
        return 0
    queue = deque([begin_word])
    steps = 1                    # 起点自己算一个单词
    while queue:
        for _ in range(len(queue)):
            word = queue.popleft()
            if word == end_word:
                return steps
            for i in range(len(word)):
                for ch in string.ascii_lowercase:
                    nxt = word[:i] + ch + word[i + 1:]
                    if nxt in words:
                        words.remove(nxt)   # 入队即标记
                        queue.append(nxt)
        steps += 1
    return 0
```

**复杂度。** 时间 `O(N·L²·26)`，空间 `O(N·L)`。

**易错点。**
- 数成边数：`hit -> cog` 是 `5` 个单词，从 `0` 起算会得到 `4`。
- 出队时才标记访问：同一单词同层被多次入队，队列膨胀。
- 要求 `beginWord` 在字典里：它不必在，但 `endWord` 必须在，否则返回 `0`。

**追问。**
- 搜索太慢？：双向 BFS，每次扩展较小的一侧，搜索量约从 `b^d` 降到 `2·b^(d/2)`。
- 要所有最短序列（LC 126）？：BFS 记录层数和全部前驱，再从终点 DFS 回溯。
- 如何少生成候选？：预建通配符桶 `h*t`，邻居就是同桶单词。

**同模式。** LC 126 单词接龙 II、LC 433 最小基因变化、LC 752 打开转盘锁、LC 773 滑动谜题
