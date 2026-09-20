---
nodes: [problems.games.cricinfo]
url: https://github.com/ashishps1/awesome-low-level-design/blob/main/problems/cricinfo.md
---
# Designing a Cricket Information System like CricInfo

值得读：最流行的免费题面，把 Match、Team、Player、Scorecard、Innings、Over、Ball 的类目
列得很全，适合用来核对自己的分层有没有漏项。它的参考实现用单例（Singleton）管理
`MatchService`/`ScorecardService`，`Scorecard` 是一个被 `updateScore()` 之类方法从外部
修改的对象——完全没有"球是唯一事件、其余全部派生"这层架构，也没有处理改判。本文认为这两点
恰恰是这道题真正值得讲的地方，因此把篇幅重新分配到了事件重放和第三裁判改判上。仓库使用
GPL-3.0 许可，可以直接引用。

%% trellis:begin %%
## Source
[Open the original ↗](https://github.com/ashishps1/awesome-low-level-design/blob/main/problems/cricinfo.md)
%% trellis:end %%
