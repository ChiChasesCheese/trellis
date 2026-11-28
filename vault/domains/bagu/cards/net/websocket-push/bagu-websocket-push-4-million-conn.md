---
id: bagu-websocket-push-4-million-conn
node: a.net.websocket-push
type: qa
step: 4
---
## Q
**百万在线 · 推送系统怎么设计**｜必会

面试官：「100 万用户同时在线，怎么设计这个推送系统？」

## A
**基本回答。** 拆接入层和业务层：连接有状态，瓶颈在文件描述符、每连接缓冲内存和心跳；业务逻辑无状态，可随便扩缩。网关只维持连接（心跳、收发）和转发，每台几万连接，加容量加机器；用一张「用户在哪台网关」的路由表（如 Redis hash，连接建立写入、断开删除），业务服务查表后经 MQ 或 RPC 送到目标网关再写入连接。广播（直播间弹幕）时网关订阅房间主题，每台只收一份再本机分发，业务侧发一次而不是对每个观众发一次。每个连接写缓冲设上限，超了丢消息或断开，防慢消费者拖垮网关内存。滚动发布时通知客户端重连并加随机退避，避免重连风暴打满鉴权服务。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 262">
<rect x="4" y="4" width="126" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="67" y="23" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">业务服务</text>
<rect x="206" y="2" width="130" height="38" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="271" y="17" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">路由表</text>
<text x="271" y="33" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">用户在哪台网关</text>
<line x1="131" y1="19" x2="205" y2="19" stroke-width="1.2" style="stroke:var(--dim,#6b7280)" stroke-dasharray="4 3"/>
<polygon points="205.0,19.0 198.0,22.2 198.0,15.8" style="fill:var(--dim,#6b7280);stroke:var(--dim,#6b7280)" stroke-width="0.5"/>
<text x="168" y="14" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">查</text>
<rect x="4" y="70" width="332" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170" y="88" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">MQ / RPC：按网关投递</text>
<line x1="67" y1="35" x2="67" y2="69" stroke-width="1.2" stroke="currentColor"/>
<polygon points="67.0,69.0 63.8,62.0 70.2,62.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="4" y="126" width="104" height="40" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="56" y="142" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">网关 1</text>
<text x="56" y="158" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">约 5 万连接</text>
<line x1="56" y1="99" x2="56" y2="125" stroke-width="1.2" stroke="currentColor"/>
<polygon points="56.0,125.0 52.8,118.0 59.2,118.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="56" y1="196" x2="56" y2="167" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<polygon points="56.0,167.0 59.2,174.0 52.8,174.0" style="fill:var(--dim,#6b7280);stroke:var(--dim,#6b7280)" stroke-width="0.5"/>
<rect x="118" y="126" width="104" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170" y="142" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">网关 2</text>
<text x="170" y="158" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">约 5 万连接</text>
<line x1="170" y1="99" x2="170" y2="125" stroke-width="1.2" stroke="currentColor"/>
<polygon points="170.0,125.0 166.8,118.0 173.2,118.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="170" y1="196" x2="170" y2="167" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<polygon points="170.0,167.0 173.2,174.0 166.8,174.0" style="fill:var(--dim,#6b7280);stroke:var(--dim,#6b7280)" stroke-width="0.5"/>
<rect x="232" y="126" width="104" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="284" y="142" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">网关 20</text>
<text x="284" y="158" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">约 5 万连接</text>
<line x1="284" y1="99" x2="284" y2="125" stroke-width="1.2" stroke="currentColor"/>
<polygon points="284.0,125.0 280.8,118.0 287.2,118.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="284" y1="196" x2="284" y2="167" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<polygon points="284.0,167.0 287.2,174.0 280.8,174.0" style="fill:var(--dim,#6b7280);stroke:var(--dim,#6b7280)" stroke-width="0.5"/>
<rect x="4" y="196" width="332" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170" y="214" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">用户：100 万同时在线</text>
<text x="4" y="246" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">100 万 ÷ 5 万 = 20 台，再留冗余</text>
</svg>
业务服务不直接连用户，先查路由表再投递到正确的网关。每台 5 万连接，100 万在线要 20 台，再留冗余，因为一台挂掉时它的连接要被其他台接走。
**业务场景。** 头部主播开播，一台网关重启，它的 20 万观众同时重连，瞬间打满鉴权服务；重连带随机延迟和限速才不会放大故障。
**容易错。**
- **以为瓶颈在业务 CPU：** 是连接数相关的资源。
- **广播时对每个用户各发一次：** 应按网关合并。
- **不给写缓冲设上限。**
