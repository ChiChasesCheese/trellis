---
id: hi-x-realtime-push-connections-3-choose
node: sd.cross.realtime-push-connections
type: qa
step: 3
---
## Q
**实时推送与有状态连接**｜跨题模式 · 怎么选

新题里要把结果送到客户端，怎么决定用推送还是轮询、推送丢了怎么办、断线后补什么？请按判断信号分情况说明，并各举一例。

## A
| 判断信号 | 做法 | 例子 |
|---|---|---|
| 结果是一次性的，等待者的读很轻 | 轮询就够，不引入长连接 | [[coding-contest-platform\|在线判题与编程竞赛平台（LeetCode）]] |
| 单向、逐字流出的输出 | SSE，断线重连带最后事件编号，从缓冲补发 | [[chatbot-design\|对话式 AI 聊天服务（简化版 ChatGPT）]] |
| 双向实时，事件有严格先后 | WebSocket 连到该实体的唯一写者，事件带序号，断线后拉完整局面再订阅增量 | [[online-chess-platform\|在线国际象棋平台]] |
| 只关心最新值，中间状态可丢 | 合并（每 100 到 200 毫秒一次最新快照），版本号去重 | [[tt-realtime-auction-bidding\|实时竞价拍卖]]、[[stock-trading-platform\|设计简化版股票交易平台（券商端，限价单）]] |
| 每条消息都不能丢 | 持久收件箱加 ack，推送只加速，重连按游标补发 | [[messenger-chat-system\|设计聊天/即时通讯系统（WhatsApp / Messenger）]] |
| 变化频繁但客户端能自己追 | 通知只带“有新游标”，客户端用游标拉，并定时兜底轮询 | [[file-sync-system\|设计云盘与文件同步系统（Dropbox / Google Drive）]] |
