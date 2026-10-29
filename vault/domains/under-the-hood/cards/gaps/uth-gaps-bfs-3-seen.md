---
id: uth-gaps-bfs-3-seen
node: gaps.bfs
type: qa
step: 3
---
## Q
**页面互相链接成环，怎样不重复抓**｜Scrapy · 2.19 去重

A 页链到 B 页，B 页又链回 A 页，还有 100 个页面都链到同一个页面。爬虫怎样保证每个地址只抓一次？

## A
**结构。** 去重过滤器 `RFPDupeFilter` 在内存里放一个集合（set），存每个请求的指纹：把规范化后的地址、方法、请求体等做 SHA-1，得 20 字节。

**细节。**

- 在请求入队时检查，不是出队时：`enqueue_request` 先问 `request_seen`，见过就丢掉
- 同一个地址被 100 个页面链到，也只入队一次
- 设了 `JOBDIR`，指纹追加写进 `requests.seen`，重启后接着用

**为什么。** 入队时就记，队列里不会有重复项；出队才记，同一个地址会在队里排很多份。

**坑。** 集合只增不删，随抓过的页面数一路涨，长时间的大爬取里它本身会成为内存大头。

**例题：** LC 127 单词接龙（同类：LC 200 岛屿数量）

给起始单词 `beginWord`、目标单词 `endWord` 和词典 `wordList`，每步只能改一个字母，改后的词必须在词典里，求最短转换序列的单词数，到不了返回 0。例：`hit` → `cog`，词典 `[hot,dot,dog,lot,log,cog]` → 5。

```python
from collections import deque

def ladder_length(begin_word: str, end_word: str, word_list: list[str]) -> int:
    words = set(word_list)
    if end_word not in words:
        return 0
    queue = deque([(begin_word, 1)])
    visited = {begin_word}
    while queue:
        word, steps = queue.popleft()
        if word == end_word:
            return steps
        for i in range(len(word)):
            for c in "abcdefghijklmnopqrstuvwxyz":
                candidate = word[:i] + c + word[i + 1:]
                if candidate in words and candidate not in visited:
                    visited.add(candidate)
                    queue.append((candidate, steps + 1))
    return 0
```
