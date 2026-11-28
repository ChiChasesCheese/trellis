---
id: bagu-websocket-push-5-reconnect
node: a.net.websocket-push
type: qa
step: 5
---
## Q
**断线重连 · 消息补发怎么做**｜必会

面试官：「用户断线 20 秒后重连，这期间的消息怎么补？」

## A
**基本回答。** 推送天然至少一次，断线窗口内必漏，所以靠「可重放的日志加序号」补。客户端指数退避加随机抖动重连（1、2、4 秒，避免同时重连）；每条消息带按会话或房间单调递增的序号（既能发现缺口，也能去重）；重连时带上最后收到的序号，服务端从存储（Redis List 或 Stream、MQ、数据库，只留有限窗口）补发之后的消息，客户端按序号去重、先缓存乱序消息、补齐后按序交付。补发期间新到的实时消息先缓冲，追到最新序号再切回实时，避免交错。缺口太大就让客户端拉全量快照。不是所有消息都补：弹幕可丢不补，只补礼物、公告等关键消息。心跳超时才能发现半开连接；客户端确认后才推进已读位置，没确认的重发。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 262">
<text x="4" y="14" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">按会话编号：每条消息一个递增序号</text>
<rect x="4" y="40" width="36" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="22" y="58" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="45" y="40" width="36" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="63" y="58" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<rect x="86" y="40" width="36" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="104" y="58" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<rect x="127" y="40" width="36" height="28" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="145" y="58" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">4</text>
<rect x="168" y="40" width="36" height="28" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="186" y="58" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">5</text>
<rect x="209" y="40" width="36" height="28" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="227" y="58" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">6</text>
<rect x="250" y="40" width="36" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="268" y="58" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">7</text>
<rect x="291" y="40" width="36" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="309" y="58" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">8</text>
<line x1="127" y1="36" x2="245" y2="36" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<text x="186" y="32" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">断线 20 秒</text>
<text x="4" y="92" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">断线的这 20 秒，4、5、6 没送到（高亮）</text>
<text x="4" y="116" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">① 重连：指数退避加随机抖动</text>
<text x="4" y="138" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">② 带上最后收到的序号 3</text>
<text x="4" y="160" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">③ 服务端从存储补发 4、5、6</text>
<text x="4" y="182" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">④ 客户端按序号去重、按序交付</text>
<text x="4" y="204" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">⑤ 补完追上最新，再切回实时 7、8</text>
<text x="4" y="232" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">缺口太大就直接拉快照，不逐条补</text>
</svg>
高亮的 4、5、6 是断线 20 秒里漏掉的；底部是重连后的处理顺序。
**业务场景。** 观众坐地铁隧道断线 20 秒，关键消息序号 4（礼物）、5（公告）、6（礼物）没送到：重连带 `last=3`，服务端取序号大于 3 的补发 4、5、6，补发时到达的 7 先缓冲，6 补完再交付；期间的弹幕不补；再收到 5 按序号丢弃。
**容易错。**
- **重连不带序号：** 服务端不知道从哪补。
- **补发和实时消息交错：** 顺序会乱。
- **所有客户端同时重连：** 重连风暴。
