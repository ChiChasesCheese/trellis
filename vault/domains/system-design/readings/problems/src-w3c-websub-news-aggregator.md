---
nodes: [problems.search.news-aggregator]
url: https://www.w3.org/TR/websub/
---
# WebSub (W3C Recommendation)

值得读：W3C 官方规范，第一方来源，定义了发布方通过 `rel="hub"`/`rel="self"` 声明 hub
和话题、订阅方发起订阅并由 hub 通过 `hub.challenge` 做挑战验证、验证通过后 hub 直接
POST 推送新内容给订阅方回调地址的完整流程，并明确说明"发布方如何通知 hub 内容已更新"
这一步本身不在规范范围内，由发布方和 hub 自行约定。本题解「深入探讨」第 1 节采用了规范
描述的订阅/验证/推送流程作为混合采集方案里的推送分支，并补充了"这条推送路径要如何和自适应
轮询、兜底爬取分工组合"这一具体架构决策——规范本身只定义协议本身，不讨论采集系统的整体
架构取舍。
