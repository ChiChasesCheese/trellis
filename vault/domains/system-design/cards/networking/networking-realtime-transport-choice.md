---
id: networking-realtime-transport-choice
node: networking.realtime
type: qa
---
## Q
Long polling vs SSE vs WebSockets — give the one-line selection rule and a canonical example for each.

## A
Choose by **directionality and frequency**:

- **Long polling**: rare updates, maximum compatibility, no infra changes — e.g. legacy notification checks.
- **SSE**: server→client only, over plain HTTP — e.g. live scores, LLM token streaming, dashboards.
- **WebSockets**: genuinely **bidirectional** and frequent — e.g. chat, collaborative editing, multiplayer games.

Default to the weakest tool that fits: SSE beats WebSockets when the client never needs to push.

## Q zh
长轮询 vs SSE vs WebSockets — 给出单行选择规则和每个的规范示例。

## A zh
选择按**方向性和频率**：

- **长轮询**：罕见的更新、最大兼容性、没有基础设施变化 — 例如遗留通知检查。
- **SSE**：仅服务器→客户端，通过普通 HTTP — 例如实时分数、LLM 令牌流、仪表板。
- **WebSockets**：真正**双向**且频繁 — 例如聊天、协作编辑、多人游戏。

默认最弱工具适合：当客户端永不需要推送时 SSE 击败 WebSockets。
