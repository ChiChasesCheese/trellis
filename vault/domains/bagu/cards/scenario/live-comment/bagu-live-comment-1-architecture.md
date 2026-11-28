---
id: bagu-live-comment-1-architecture
node: a.scenario.live-comment
type: qa
step: 1
---
## Q
**直播评论系统 · 整体架构怎么分**｜必会

面试官：「设计一个高并发的直播间评论系统，整体架构怎么分？」

## A
**基本回答。** 把写入和推送解耦：客户端发评论到接入层，评论服务做鉴权、限流、审核，之后写入消息队列（MQ）。一路消费者批量落库，另一路把评论送到推送网关，网关再经长连接下发给在线观众。进房看历史评论走缓存加数据库查询。
**一句话记住。** 像电台的点歌台：听众递纸条只管塞进收件箱，后台一路把纸条归档，另一路交给播音员念给所有听众听。收纸条和广播是两条各干各的线，谁慢都不拖累另一边。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 214">
<text x="8" y="14" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">写入链路</text>
<rect x="8" y="24" width="72" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="44" y="48" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">客户端</text>
<rect x="92" y="24" width="72" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="128" y="48" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">接入层</text>
<line x1="80" y1="44" x2="85.0" y2="44.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="92,44 85.0,47.2 85.0,40.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="176" y="24" width="72" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="212" y="40.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">评论服务</text>
<text x="212" y="55.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">审核限流</text>
<line x1="164" y1="44" x2="169.0" y2="44.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="176,44 169.0,47.2 169.0,40.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="260" y="24" width="72" height="40" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="296" y="48" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">MQ</text>
<line x1="248" y1="44" x2="253.0" y2="44.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="260,44 253.0,47.2 253.0,40.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="8" y="84" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">评论服务：鉴权、限流、审核</text>
<line x1="296" y1="64" x2="296.0" y2="101.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="296,108 292.8,101.0 299.2,101.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="280" y1="64" x2="217.9" y2="104.2" stroke-width="1.2" stroke="currentColor"/>
<polygon points="212,108 216.1,101.5 219.6,106.9" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="176" y="108" width="72" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="212" y="124.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">批量落库</text>
<text x="212" y="139.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">数据库</text>
<rect x="260" y="108" width="72" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="296" y="124.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">推送网关</text>
<text x="296" y="139.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">按房间分片</text>
<text x="8" y="128" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">存储链路</text>
<line x1="296" y1="148" x2="296.0" y2="161.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="296,168 292.8,161.0 299.2,161.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="212" y="168" width="120" height="36" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="272" y="190" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">长连接 → 在线观众</text>
<text x="8" y="190" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">推送链路</text>
</svg>
评论从左上进来，经过评论服务进入 MQ，再分成两路：一路批量落库，一路由推送网关经长连接发给观众。
**讲明白。**
- **为什么要解耦：** 写入量（每秒几十万条）和推送扇出（一条评论乘以在线人数，扇出就是一份变多份）是两个独立瓶颈。解耦之后各自水平扩展、各自降级。
- **写入链路：** 客户端发评论到接入层，评论服务做鉴权（确认是谁）、限流、审核，然后写入消息队列（MQ）。写入链路只负责把评论放进 MQ 就返回，所以很快。
- **存储链路：** 一路消费者从 MQ 里批量取评论，批量落库，用来以后查历史。
- **推送链路：** 另一路把评论送到推送网关，网关再经长连接（观众进房后和服务器保持不断开的连接）下发给在线观众。
- **扇出会放大：** 一条评论、100 万观众，就是 100 万次下发。所以推送链路的瓶颈和写入完全不同，要单独扩展。
- **进房看历史：** 进房首屏只取最近 N 条，放在缓存里；更早的历史走缓存加数据库查询。
- **读多写少用反范式：** 读多写少的部分用读写分离、缓存和反范式（把常用字段冗余进评论行，如昵称、头像），避免联表。
**举个例子。** 观众甲在直播间发一条「666」：
1. **接入层收到：** 评论服务确认他已登录、没有被限流、没有命中敏感词。
2. **写入 MQ：** 评论放进 MQ 就返回成功，甲的手机立刻显示这条评论。
3. **存储这一路：** 消费者攒一批评论，批量写入数据库，用来以后翻历史。
4. **推送这一路：** 推送网关收到这条评论，经长连接发给所有在线观众，大家几乎同时看到。
5. **中途有人进房：** 新观众进房时，从缓存里取最近 N 条评论作为首屏，之后跟随推送。
**容易错。**
- **评论服务同步落库再推送：** 数据库成为写入瓶颈，一慢全慢，推送也被拖住。
- **把存储和推送当成一件事：** 它们的规模和扩展方式完全不同，一条评论写一次，却要推给所有在线观众。
- **忽略扇出放大：** 只看写入的 QPS 容易低估推送压力，100 万观众意味着每条评论 100 万次下发。
- **进房首屏每次都查数据库：** 进房是高频操作，首屏要走缓存。
**业务场景。** 头部主播开播，评论每秒几十万条。写入链路只负责把评论放进 MQ 就返回，落库和推送各自按自己的速度消费，互不拖累。
**系统设计。** [[links.fb-live-comments|Facebook 直播评论]]：被问「评论系统整体怎么分」，答写入链路、存储链路、推送链路三条线，用 MQ 解耦，再分别讲每条线的扩展方式。
**相关题。** 练习题 pub-sub、练习题 chat-room
**可能问法。**
- 弹幕系统怎么设计？ → 把写入和推送解耦：客户端发评论到接入层，评论服务做鉴权、限流、审核，写入 MQ；一路消费者批量落库，另一路送到推送网关，经长连接下发给在线观众。写入量和推送扇出是两个独立瓶颈，解耦后各自水平扩展、各自降级。
- 直播评论的读写路径是什么？ → 写路径：客户端 → 接入层 → 评论服务（鉴权、限流、审核）→ MQ → 批量落库。推送路径：MQ → 推送网关 → 长连接 → 观众。读路径：进房首屏取最近 N 条，走缓存加数据库；读多写少的部分用反范式，把常用字段冗余进评论行，避免联表。
