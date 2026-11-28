---
id: bagu-im-delivery-1-reliable-order-offline
node: b.scenario.im-delivery
type: qa
step: 1
---
## Q
**IM 消息可靠下发 · 不丢、不重、有序、离线同步**｜追问

面试官：「设计千万 DAU 的 IM：用户在地铁里发消息时断网，恢复后怎么保证不丢不重？消息 ID 和顺序怎么设计？离线消息怎么存储和同步？」

## A
**基本回答。** 不丢靠确认加重发：客户端发消息带自己生成的 msg_id，服务端落库后回 ack，没收到就重发；推给接收方也等接收方 ack。不重靠幂等：服务端和接收端都按 msg_id 去重，同一个 ID 第二次来只回 ack。网络上做不到真正的恰好一次，做法是至少一次投递加幂等去重。顺序：每个会话由服务端分配单调递增的 seq，消息按会话分区，客户端按 seq 排序、发现空洞就拉取补齐；全局有序不需要也做不到。离线消息先存后推进收件箱，上线后带已收到的最大 seq 拉增量，确认后清理。群聊：小群写扩散（每人一份，读快，写放大），大群读扩散（群内一份，每人记已读位置，读时合并）。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 268">
<rect x="15" y="6" width="70" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="50.0" y="22.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">发送方</text>
<rect x="135" y="6" width="70" height="24" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="170.0" y="22.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">服务端</text>
<rect x="255" y="6" width="70" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="290.0" y="22.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">接收方</text>
<line x1="50" y1="30" x2="50" y2="244" stroke-width="1.2" stroke="currentColor" stroke-dasharray="4 3"/>
<line x1="170" y1="30" x2="170" y2="244" stroke-width="1.2" stroke="currentColor" stroke-dasharray="4 3"/>
<line x1="290" y1="30" x2="290" y2="244" stroke-width="1.2" stroke="currentColor" stroke-dasharray="4 3"/>
<line x1="50" y1="54" x2="168" y2="54" stroke-width="1.2" stroke="currentColor"/>
<polygon points="168.0,54.0 161.0,57.2 161.0,50.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="110" y="48" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">发 m1（带 msg_id）</text>
<text x="176" y="72" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">落库</text>
<line x1="168" y1="96" x2="52" y2="96" stroke-width="1.2" stroke="currentColor" stroke-dasharray="4 3"/>
<polygon points="52.0,96.0 59.0,92.8 59.0,99.2" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="110" y="90" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">ack 丢了 ✗</text>
<text x="56" y="116" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">等不到 ack</text>
<line x1="50" y1="138" x2="168" y2="138" stroke-width="1.2" stroke="currentColor"/>
<polygon points="168.0,138.0 161.0,141.2 161.0,134.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="110" y="132" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">重发 m1</text>
<text x="176" y="158" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">按 m1 去重，不再落库</text>
<line x1="168" y1="182" x2="52" y2="182" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="52.0,182.0 59.0,178.8 59.0,185.2" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="110" y="176" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">ack</text>
<line x1="172" y1="206" x2="288" y2="206" stroke-width="1.2" stroke="currentColor"/>
<polygon points="288.0,206.0 281.0,209.2 281.0,202.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="230" y="200" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">推 m1，seq=8</text>
<line x1="288" y1="230" x2="172" y2="230" stroke-width="1.2" stroke="currentColor" stroke-dasharray="4 3"/>
<polygon points="172.0,230.0 179.0,226.8 179.0,233.2" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="230" y="224" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">ack</text>
<text x="8" y="260" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">至少一次投递 + 幂等去重 = 效果上恰好一次</text>
</svg>
发送方发 m1，服务端落库但 ack 在路上丢了；发送方等不到就重发 m1，服务端按 ID 认出重复，不再落库、只回 ack；再推给接收方，接收方也回 ack。
**举个例子。** 用户在地铁发消息：生成 m1，本地标「发送中」；服务端落库分到 seq=8 并回 ack，但列车进隧道 ack 丢了；客户端超时重发 m1，服务端发现已落库，只再回一次 ack。对方离线时消息留在收件箱，上线带已收到的最大 seq=7 拉到 seq=8；若收到 6 和 8 却缺 7，主动拉 7 补洞。
**容易错。**
- **以为发出去就是送达：** 没收到 ack 就是不确定，要重发。
- **只重发不去重：** 会重复。
