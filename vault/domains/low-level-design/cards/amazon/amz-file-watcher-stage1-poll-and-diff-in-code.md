---
id: amz-file-watcher-stage1-poll-and-diff-in-code
node: amazon.amz-file-watcher
type: qa
step: 3
tags: [grown]
---
## Q
在 Amazon 文件监听器设计里，第 1 关的核心 `poll()` 怎么写？第一次调用该报什么？

## A
第一次只拍基线，不报事件；之后拍快照、与已提交的世界比对：
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
