---
nodes: [problems.social.music-streaming]
url: https://docs.python.org/3/library/collections.html#collections.deque
---
# collections — deque

值得读：官方文档对 `deque` 两端 O(1) 操作与 `maxlen` 的说明，是本文 `PlayQueue._upcoming`/
`_history`（两端都要 `pop`/`append`）与 `PlayHistory._events`（`maxlen` 表达"有界日志，
旧的自动淘汰"）的直接依据——普通 `list` 的 `pop(0)` 是 O(n)，`deque` 的 `popleft()` 是
O(1)，这正是播放队列频繁从队首取歌、从队首插回"上一首"时应该选的结构。
