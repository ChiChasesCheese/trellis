---
id: problems-cricinfo-notify-outside-lock
node: problems.games.cricinfo
type: qa
step: 7
tags: [grown]
---
## Q
体育比分系统设计里，`CommentaryFeed._notify` 为什么要先把订阅者列表复制一份、释放锁之后再逐个调用订阅者，而不是在持锁的情况下直接遍历 `self._subscribers` 调用？

## A
订阅者是外部代码，如果在持有 `CommentaryFeed` 自己的锁时调用它们，一个很常见的场景——订阅者在收到第一条更新后，在回调里反过来调用 `subscribe`/`unsubscribe`——就会让这个线程尝试重新获取自己已经持有的锁，把自己锁死（如果用的是不可重入的普通锁）。复制列表、释放锁、再调用，是“持锁只做属于自己的最小操作，调用外部代码之前先放手”这条纪律的具体做法。
