---
id: hi-fix-retry-key-04-uber
node: fix.retry-key
type: qa
step: 5
---
## Q
**Uber 叫车与接单 · 重试键**｜补强

面试官：「骑手确认乘车后点了请求，网络抖了一下没收到响应，他再点一次。司机点接单也一样。怎么不出现两个订单、也不让司机看到「已被接走」？」

你会怎么回答？白板上画到哪一步？

## A
**你说。**
- **骑手一侧，键已经有了：** 「叫车流程本来就是两步：先 `POST /fares` 估价，服务端返回 `fare_id`，再 `POST /rides {fare_id}`。这个 `fare_id` 在叫车请求之前就在客户端手里，我直接把它当重试键：`rides.fare_id` 加唯一约束。」
- **重试怎么走：** 「第二次 `POST /rides {F7}` 的 INSERT 撞上唯一约束，我读已有的 ride 返回，同一个订单。骑手真想再叫一辆，要重新估价，拿到新的 `fare_id`。」
- **司机一侧，键是自然的：** 「接单这件事，一个司机对一个订单最多接一次，所以重试键就是 (ride_id, driver_id)，不用另外生成。」
- **条件更新加一次读：** 「`UPDATE rides SET status='ACCEPTED', driver_id=:d WHERE id=:r AND status='REQUESTED'`。影响 1 行，成功。影响 0 行有两种可能：被别人接走，或者是我自己上一次接成了。所以我再读一次 `driver_id`，是我就返回成功，不是我才告诉司机已被接走。」
- **为什么多读一次：** 「只记「已经接了」不够，要记「是谁接的」。0 行不能直接翻译成失败。」
- **和匹配锁的关系：** 「向司机发订单时，我用 Redis 锁保证一个司机同一时间只收到一个请求，10 秒的 TTL；接单的 UPDATE 是最后一道闸，锁过期后也不会出现两个司机。」
**白板。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 334">
<rect x="18" y="8" width="72" height="38" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="54" y="31" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">骑手 App</text>
<rect x="134" y="8" width="72" height="38" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="170" y="31" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">打车 API</text>
<rect x="250" y="8" width="72" height="38" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="286" y="31" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">数据库</text>
<text x="58" y="72" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">POST /fares（估价）</text>
<polyline points="54,84 170,84" fill="none" stroke-width="1.3" stroke="currentColor"/>
<polygon points="170,84 163.0,87.2 163.0,80.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="58" y="106" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">fare_id = F7</text>
<polyline points="170,118 54,118" fill="none" stroke-width="1.3" stroke-dasharray="4 3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="54,118 61.0,114.8 61.0,121.2" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="58" y="140" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">POST /rides {F7}</text>
<polyline points="54,152 170,152" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="170,152 163.0,155.2 163.0,148.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="282" y="174" text-anchor="end" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">INSERT rides（fare_id 唯一）</text>
<polyline points="170,186 286,186" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="286,186 279.0,189.2 279.0,182.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="170" y="214" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">响应丢失，用户再点</text>
<text x="58" y="236" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">POST /rides {F7}</text>
<polyline points="54,248 170,248" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="170,248 163.0,251.2 163.0,244.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="174" y="270" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">INSERT 冲突 → 读 ride</text>
<polyline points="170,282 286,282" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="286,282 279.0,285.2 279.0,278.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="58" y="304" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">同一个 ride</text>
<polyline points="170,316 54,316" fill="none" stroke-width="1.3" stroke-dasharray="4 3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="54,316 61.0,312.8 61.0,319.2" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<line x1="54" y1="48" x2="54" y2="330" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="170" y1="48" x2="170" y2="61" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="170" y1="76" x2="170" y2="129" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="170" y1="144" x2="170" y2="163" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="170" y1="178" x2="170" y2="203" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="170" y1="218" x2="170" y2="225" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="170" y1="240" x2="170" y2="330" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="286" y1="48" x2="286" y2="259" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="286" y1="274" x2="286" y2="330" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="8" y1="210" x2="105.68" y2="210" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="234.32" y1="210" x2="332" y2="210" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
</svg>
白板上：键由估价接口更早发出，先于叫车请求就在骑手手里。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 362">
<rect x="18" y="8" width="72" height="38" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="54" y="31" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">司机 App</text>
<rect x="134" y="8" width="72" height="38" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="170" y="31" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">打车 API</text>
<rect x="250" y="8" width="72" height="38" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="286" y="31" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">数据库</text>
<text x="58" y="72" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">accept(ride R)</text>
<polyline points="54,84 170,84" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="170,84 163.0,87.2 163.0,80.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="282" y="106" text-anchor="end" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">UPDATE … 条件：仍是 REQUESTED</text>
<polyline points="170,118 286,118" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="286,118 279.0,121.2 279.0,114.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<rect x="231.52" y="132" width="104.48" height="20" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="283.76" y="146" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">driver_id = D</text>
<text x="170" y="174" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">响应丢失，司机再点</text>
<text x="58" y="196" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">accept(ride R)</text>
<polyline points="54,208 170,208" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="170,208 163.0,211.2 163.0,204.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="174" y="230" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">UPDATE … → 0 行</text>
<polyline points="170,242 286,242" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="286,242 279.0,245.2 279.0,238.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="174" y="264" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">SELECT driver_id</text>
<polyline points="170,276 286,276" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="286,276 279.0,279.2 279.0,272.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="174" y="298" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">D（就是我）</text>
<polyline points="286,310 170,310" fill="none" stroke-width="1.3" stroke-dasharray="4 3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="170,310 177.0,306.8 177.0,313.2" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="58" y="332" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">成功，和第一次一样</text>
<polyline points="170,344 54,344" fill="none" stroke-width="1.3" stroke-dasharray="4 3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="54,344 61.0,340.8 61.0,347.2" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<line x1="54" y1="48" x2="54" y2="358" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="170" y1="48" x2="170" y2="95" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="170" y1="110" x2="170" y2="163" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="170" y1="178" x2="170" y2="321" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="170" y1="336" x2="170" y2="358" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="286" y1="48" x2="286" y2="130" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="286" y1="154" x2="286" y2="253" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="286" y1="268" x2="286" y2="358" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="8" y1="170" x2="105.68" y2="170" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="234.32" y1="170" x2="332" y2="170" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
</svg>
白板上：接单的重试读到 driver_id 就是自己，返回和第一次完全一样的成功。

**为什么这样说。** 面试官要看你能不能识别出「键」不一定是新生成的 UUID：它可以是服务端更早发出的 id，也可以是业务上本来就唯一的一对 (订单, 司机)。弱的回答是：重试时「已被接走」直接返回给司机，司机以为自己没接到，其实订单是他的。强的回答用一次读把「我赢了」和「别人赢了」分开。
**面试官可能接着问。**
- 什么时候必须生成新的随机键，什么时候用自然键？ → 同一个意图可能合法地发生多次（捐款、下单）就要每次新生成；意图天然唯一（一个司机接一个订单、一次估价对应一次叫车）就用业务值。
- 司机重试时订单已经被取消了呢？ → 条件更新 0 行，读出来 status 是 CANCELLED，返回已取消，不是已被接走。
- 骑手叫车和估价隔了很久呢？ → `fare_id` 带过期时间，过期的估价不能叫车，要重新估价，也就是新的键。
- 司机的重试和匹配的超时重派同时发生呢？ → 重派之前也走条件更新（REQUESTED 才能改派），两个动作争同一行，只有一个赢，输的读到现状再决定。
**常见失分。**
- **0 行当失败：** 重试被当成「已被接走」，司机以为没接到。
- **只存「已接」不存「谁」：** 没法区分是自己还是别人。
- **每次点击新生成键：** 重试变成两个订单。
- **用 (骑手, 时间窗口) 判重：** 骑手几分钟内叫两辆车是可能的。
