---
id: amz-file-watcher-stage1-poll-and-diff-in-code
node: amazon.amz-file-watcher
type: qa
step: 3
tags: [grown]
---
## Q
在 Amazon 文件监听器设计里，第 1 关的核心 `poll()` 怎么写？第一次调用该发出什么事件？

## A
第一次只拍基线（baseline，记下此刻目录的样子），不发事件；之后每次拍快照（snapshot，路径到指纹的字典），与「订阅者已经知道的目录状态」（已提交的世界）比对：
```python
def poll(self) -> list[Event]:
    raw = self._fs.scan(self._root, self._recursive)
    with self._lock:
        if self._committed is None:      # 第一次：只建基线
            self._committed = raw
            return []
        events = diff(self._committed, raw)
        self._committed = raw
        targets = list(self._subs.values())
    self._dispatch(events, targets)       # 回调在锁外
    return events
```
监听开始前就存在的文件不算新建。
