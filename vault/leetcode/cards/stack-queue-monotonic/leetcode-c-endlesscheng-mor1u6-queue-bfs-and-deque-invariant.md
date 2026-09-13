---
id: leetcode-c-endlesscheng-mor1u6-queue-bfs-and-deque-invariant
node: stack-queue-monotonic.queue-bfs-and-deque
type: cloze
anki: 1789002113471
tags: [concept-cloze, invariant, leetcode, recall]
---
BFS 中节点第一次被发现时记录的距离就是 {{c1::最短距离}}。

普通 BFS 中节点首次出队或首次入队时的距离最短；队列中的状态按非递减距离层次出现；已访问状态不应重复入队

**Evidence**

四、队列

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F08.07%20-%20%E9%98%9F%E5%88%97%E3%80%81BFS%20%E4%B8%8E%E5%8F%8C%E7%AB%AF%E9%98%9F%E5%88%97)
