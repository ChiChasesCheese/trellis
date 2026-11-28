---
id: bagu-live-comment-2-write-peak
node: a.scenario.live-comment
type: qa
step: 2
---
## Q
**写入削峰 · 评论要不要全部落库**｜必会

面试官：「每秒几十万条评论，数据库扛不住，评论要不要全部落库？」

## A
**基本回答。** 评论先进 MQ（如 Kafka）缓冲，消费者攒一批再批量插入，数据库按房间和时间分片。不必每条同步落库：实时展示走推送流，只有历史查询才需要持久化。重要消息（打赏、主播和管理员发言）保证落库，普通弹幕在高峰可采样或丢弃。
**一句话记住。** 水库调洪：暴雨时的洪峰先蓄进水库，下游按能承受的流量匀速放水；而且不是每滴水都要存档，只有重要的才存。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 214">
<rect x="8" y="24" width="72" height="40" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="44" y="40.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">评论</text>
<text x="44" y="55.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">尖峰</text>
<line x1="80" y1="44" x2="87.0" y2="44.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="94,44 87.0,47.2 87.0,40.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="94" y="24" width="108" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="148" y="40.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">MQ 缓冲</text>
<text x="148" y="55.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">房间 ID 分区</text>
<line x1="202" y1="44" x2="209.0" y2="44.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="216,44 209.0,47.2 209.0,40.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="216" y="24" width="116" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="274" y="40.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">消费者</text>
<text x="274" y="55.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">攒一批</text>
<line x1="274" y1="64" x2="274.0" y2="81.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="274,88 270.8,81.0 277.2,81.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="8" y="88" width="324" height="36" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170" y="110" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">批量插入，数据库按房间和时间分片</text>
<text x="8" y="148" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">按重要程度分级：</text>
<rect x="8" y="156" width="158" height="44" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="87" y="174.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">打赏、主播、管理员</text>
<text x="87" y="189.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">必须落库</text>
<rect x="174" y="156" width="158" height="44" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="253" y="174.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">普通弹幕</text>
<text x="253" y="189.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">高峰可采样、丢弃</text>
</svg>
尖峰先被 MQ 吸收，消费者攒一批再批量写库；而且不是每条评论都同等重要，要分级。
**讲明白。**
- **MQ 吸收尖峰：** 评论先进 MQ（如 Kafka）缓冲，把突发的写入变成平滑的消费。数据库不用直接面对每秒几十万条。
- **批量插入：** 消费者攒一批再一次性插入，比一条一条写大幅减少数据库 I/O（每次写入都有一次网络往返和一次落盘）。
- **按房间和时间分片：** 数据库按房间和时间分片，一个房间的评论按时间落在不同的分片上，读写压力分散。
- **「实时展示」和「持久保存」是两个需求：** 实时展示走推送流，观众不需要等数据库；只有历史查询才需要持久化。
- **按重要程度分级：** 重要消息（打赏、主播和管理员发言）保证落库；普通弹幕在高峰可以采样（只保留一部分）或丢弃。
- **用房间 ID 作为分区键：** 同一房间的评论进入同一个 MQ 分区，同一分区内保持顺序。
- **落库延迟几秒没关系：** 观众看到评论走的是推送这条链路，不依赖落库。
- **消费者要幂等：** MQ 可能重复投递，用评论 ID 去重，避免重复评论。
**举个例子。** 直播间抽奖开始，一秒内涌进几十万条「1」「参与」：
1. **尖峰到来：** 写入链路把评论放进 MQ 就返回，MQ 里短暂积压。
2. **消费者批量写：** 每次攒一批，一次批量写入几千条，比一条一条写省大量 I/O。
3. **积压消化：** 消费速度跟得上之后，积压在几十秒内消化完。
4. **观众感受：** 观众看到弹幕走的是推送，不受落库快慢影响。
5. **同时：** 主播的一条口令和观众的「1」不同级：主播的保证落库，普通的「1」在高峰可以采样。
**容易错。**
- **每条评论都同步落库：** 峰值把数据库打垮，落库慢还会拖住发评论的响应。
- **所有评论都要求全局有序：** 全局有序让吞吐无法扩展；按房间分区，同房间有序就够了。
- **把打赏也当普通弹幕采样：** 打赏涉及钱，必须保证落库；采样、丢弃只用于普通弹幕。
- **消费者不幂等：** MQ 重复投递会产生重复评论。
**业务场景。** 直播间抽奖开始，一秒内涌进几十万条「1」「参与」。MQ 吸收这个尖峰，数据库每次批量写几千条，消费速度跟得上后，积压在几十秒内消化完。
**系统设计。** [[links.messenger-chat-system|聊天/即时通讯系统（WhatsApp / Messenger）]]：被问「消息顺序怎么保证」，答按会话（房间）分区，同分区内有序，而不是全局有序，全局有序会让吞吐无法扩展。
**相关题。** 练习题 bounded-blocking-queue
**可能问法。**
- 评论系统怎么削峰？ → 评论先进 MQ（如 Kafka）缓冲，消费者攒一批再批量插入，数据库按房间和时间分片。批量写大幅减少数据库 I/O，突发写入被变成平滑消费。用房间 ID 作分区键，同房间评论保持顺序，消费者幂等。
- 弹幕需要全部存数据库吗？ → 不需要。实时展示走推送流，只有历史查询才需要持久化。重要消息（打赏、主播和管理员发言）要保证落库，普通弹幕高峰可以采样或丢弃，落库延迟几秒不影响观众看到评论。
