---
id: problems-pub-sub-eviction-condition
node: problems.components.pub-sub
type: qa
step: 5
tags: [grown]
---
## Q
进程内 Pub-Sub 里，『阻塞发布者』（BLOCK）策略下，发布者到底在等什么条件成立？为什么『等日志变短』是错的？

## A
等的是**最慢的位点越过了队头**，不是『日志变短』——没有任何人会替它变短，日志只在追加时才淘汰。只有队头被所有订阅者读过，淘汰它才不算丢消息：

```python
while self._min_cursor() <= self._start_seq:
    self._not_full.wait(remaining)
```

没有任何位点时 `_min_cursor()` 取 `next_seq`（视为都读完了），否则一个没人订阅的主题会把发布者永久挂住。

『拒绝发布』（REJECT）用**同一个判据**，只是不等：先淘汰所有人都读过的队头，淘汰完还是满的才抛背压异常。漏掉这一步是一个真实的 bug——REJECT 若从不淘汰，日志一旦写满就永远满着，『有界组件』退化成『写满即死』。
