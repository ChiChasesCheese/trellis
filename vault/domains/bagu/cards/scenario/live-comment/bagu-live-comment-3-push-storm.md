---
id: bagu-live-comment-3-push-storm
node: a.scenario.live-comment
type: qa
step: 3
---
## Q
**推送风暴 · 百万观众怎么控制**｜必会

面试官：「怎么把评论推送给百万在线观众？推送风暴怎么控制？」

## A
**基本回答。** 先按房间分片：观众的连接分布在多台推送网关，评论按房间发布到 MQ 或发布订阅，每台网关只收一份，再在本机分发给自己的连接。再合并：每 100 到 200 毫秒把这段时间的评论打成一包下发。最后限速和采样：超过阈值只推一部分，并给重要消息更高优先级。
**一句话记住。** 大会场的广播员不会每来一张纸条就喊一次，而是每隔几秒把攒下的纸条合成一段念出来；而且念不完时只挑重要的念。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 206">
<rect x="8" y="24" width="324" height="30" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170" y="43" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">评论按房间发布到 MQ 或发布订阅</text>
<line x1="58" y1="54" x2="58.0" y2="69.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="58,76 54.8,69.0 61.2,69.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="8" y="76" width="100" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="58" y="92.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">网关 1</text>
<text x="58" y="107.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">收一份，分发</text>
<line x1="170" y1="54" x2="170.0" y2="69.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="170,76 166.8,69.0 173.2,69.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="120" y="76" width="100" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170" y="92.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">网关 2</text>
<text x="170" y="107.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">收一份，分发</text>
<line x1="282" y1="54" x2="282.0" y2="69.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="282,76 278.8,69.0 285.2,69.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="232" y="76" width="100" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="282" y="92.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">网关 3</text>
<text x="282" y="107.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">收一份，分发</text>
<text x="8" y="138" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">每 100 ~ 200 毫秒合并成一包下发</text>
<text x="8" y="160" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">逐条推：100 万 × 1 万条 = 100 亿次/秒</text>
<text x="8" y="180" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">每 200 毫秒一包：100 万 × 5 = 500 万次/秒</text>
<text x="8" y="198" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">再限速采样，重要消息优先</text>
</svg>
先让每台网关只收一份评论，再在本机分发给自己手里的连接；合并成一包又把下发次数降了一个数量级。
**讲明白。**
- **真正的瓶颈是扇出放大：** 房间 100 万观众、每秒 1 万条评论，逐条推送是 100 亿次下发每秒；每 200 毫秒合并一批，每秒 5 批，降到 100 万 × 5 = 500 万次，每批里再采样出观众看得过来的数量。
- **第一步按房间分片：** 观众的长连接分布在多台推送网关上。评论按房间发布到 MQ 或发布订阅，每台网关只收一份，不是每条连接各收一份，再在本机分发给自己的连接。
- **第二步合并：** 每 100 到 200 毫秒把这段时间的评论打成一包下发。每次下发都有固定的帧头和系统调用开销，合并后分摊到多条消息上。
- **第三步限速和采样：** 超过阈值只推一部分，并给重要消息更高优先级（如主播、打赏、管理员的发言）。
- **客户端也要限速滚动：** 人眼看不了每秒上千条，客户端按观众看得过来的速度滚动。
- **慢消费者设写缓冲上限：** 某个观众网络慢，网关给他的写缓冲会越积越大。设上限，超了就丢弃，避免拖垮网关。
**举个例子。** 一个百万人在线的直播间，主播抽奖带来评论洪峰：
1. **不合并时：** 每条评论立刻给 100 万个连接各写一次，网关的写缓冲迅速堆积、内存上涨。
2. **合并后：** 网关把这 200 毫秒内收到的评论攒成一包，每个连接每 200 毫秒只写一次。
3. **采样：** 这一包里评论太多时，只挑出观众看得过来的一部分，重要消息优先。
4. **某个慢观众：** 写缓冲达到上限，丢弃他落后的评论，网关不被他拖垮。
5. **观众看到：** 滚动但流畅的弹幕，而不是卡顿。
**容易错。**
- **逐条推送：** 每条评论 × 在线人数，下发次数是 100 亿次每秒的量级，网关扛不住。
- **每个连接都各订阅一份：** 评论到每台网关应该只有一份，再在本机分发。
- **只合并不采样：** 洪峰时一包里仍有太多评论，客户端也看不过来。
- **慢消费者不设上限：** 一个慢连接会拖垮整台网关。
**业务场景。** 一个百万人在线的直播间，主播抽奖带来评论洪峰。不合并时网关写缓冲迅速堆积、内存上涨；改成 200 毫秒一包并采样后，网关负载平稳，观众看到的是滚动但流畅的弹幕。
**系统设计。** [[links.notification-system-scale|通知系统（支持单发与群发，百万级每秒）]]：被问「群发怎么避免瞬间压垮推送层」，答按网关合并投递、批量下发加限速，与直播间扇出是同一个问题。
**相关题。** 练习题 pub-sub
**可能问法。**
- 弹幕怎么推送给百万用户？ → 先按房间分片：观众连接分布在多台推送网关，评论按房间发布到 MQ 或发布订阅，每台网关只收一份，再在本机分发给自己的连接；再每 100 到 200 毫秒合并成一包下发；最后限速采样，重要消息优先级更高。
- 怎么避免消息风暴？ → 瓶颈是扇出放大：100 万观众、每秒 1 万条评论，逐条推送是 100 亿次下发每秒。每 200 毫秒合并一批可降到约 500 万次，每批再采样；客户端也要限速滚动；慢消费者设写缓冲上限，超了就丢弃，避免拖垮网关。
