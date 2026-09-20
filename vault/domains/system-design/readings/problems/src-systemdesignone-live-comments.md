---
nodes: [problems.social.live-comments]
url: https://systemdesign.one/live-comment-system-design/
tags: [no-archive]
---
# Live comment system design

值得读：商业刷题站对这道题的完整 walkthrough，给出网关连接数、dispatcher 吞吐等具体
数字，覆盖面比免费的 algomaster/codemia 大纲更深。本题解没有采用它给出的具体数字（这些
数字只来自这一个二手来源，未经一手验证），而是用自己标注为假设的连接密度和推送速率
上限重新推导容量估算；和本题解相同的地方是都选择了 SSE 而不是 WebSocket 作为广播传输
协议。
