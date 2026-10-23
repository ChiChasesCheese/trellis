---
id: hl-sd03-feed-arbitration-gap
node: system-design.sd03-low-latency-trading
type: qa
step: 13
---
## Q
行情摄取里 A/B 仲裁、缺口（gap）处理、乱序怎么做？

## A
- **A/B 仲裁**：交易所用 UDP 组播同时发给所有订阅者，A/B 两路冗余（不同交换机 / 路径），每条消息有序号。Feed Handler 两路同时收，**先到者胜**，用「已见序号」的环形位图去重，任一路丢包不影响；
- **缺口**（两路都没有序号 n）：① 标记所有受影响品种为 **STALE**（簿不可信）；② 请求重传（Nasdaq MoldUDP64 向重传服务器发单播 UDP 请求包，CME MDP 3.0 是 TCP replay + 快照回环）或拉取快照 + 之后的增量重新对齐；③ 重新对齐前**策略不得对 STALE 品种发新单**（fail closed），已有挂单按策略配置决定是否撤单；
- **乱序**：对少量乱序用小窗口缓冲重排，窗口超时仍缺 ⟹ 当作缺口。
