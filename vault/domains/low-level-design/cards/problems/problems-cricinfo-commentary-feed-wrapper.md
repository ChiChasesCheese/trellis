---
id: problems-cricinfo-commentary-feed-wrapper
node: problems.games.cricinfo
type: qa
step: 6
tags: [grown]
---
## Q
体育比分系统设计里，直播评论订阅（第 4 关的观察者应用）为什么被实现成一个包住 `Innings` 的外部类 `CommentaryFeed`，而不是把订阅列表和通知逻辑直接加进 `Innings` 里？

## A
把订阅逻辑直接加进 `Innings`，就意味着“加一个不影响记分本身的新需求”要去修改记分这个已经测试过、且承载着全部规则复杂度的核心类。做成外部的 `CommentaryFeed`——它持有对 `Innings` 的引用，`record`/`amend_last_ball` 先转调 `Innings` 的同名方法，成功后再通知订阅者——`Innings` 完全不知道自己被包住了，一行代码都不用改。测试可以直接证明这一点：绕开 `CommentaryFeed`、直接在 `Innings` 上记分，订阅者完全收不到通知，但记分本身完全正常。
