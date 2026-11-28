---
id: hi-fix-retry-key-06-robinhood
node: fix.retry-key
type: qa
step: 7
---
## Q
**Robinhood 下单 · 重试键**｜补强

面试官：「用户点了买入 100 股，请求超时，他又点了一次。一单变两单，在交易里是真金白银。你的下单接口怎么设计？」

你会怎么回答？白板上画到哪一步？

## A
**你说。**
- **先写出请求：** 「`POST /orders {client_order_id, symbol, side, qty, type}`。App 在用户进入 Review 页的时候生成 `client_order_id`，直到看到结果才丢弃。」
- **唯一约束：** 「订单库 `UNIQUE (user_id, client_order_id)`。库按 user_id 分片，所以这个约束落在同一个分片里，不需要跨分片协调。」
- **先写库再提交交易所：** 「订单先以 PENDING 写库并提交，再提交给交易所；先写库是为了即使后面崩溃，我们也知道有一个订单可能在交易所。」
- **交易所一侧的键：** 「提交时带上 clientOrderId（取我们的订单 id）。交易所接口一般有这个字段，而且会拒绝重复的，以所用交易所的文档为准。」
- **重试怎么走：** 「第二次 POST 的 INSERT 冲突，我读已有的订单，返回同一个订单和它当前的状态：PENDING、SUBMITTED 或 FILLED。不会再向交易所提交。」
- **崩溃怎么收敛：** 「清理任务扫长时间 PENDING 的订单，先用 clientOrderId 去交易所查：查到就记下 externalOrderId，查不到才提交；就算查询和提交撞车，交易所也会拒绝同一个 clientOrderId。」
- **用户刻意再买一单：** 「重新走 Review 页，生成新的 `client_order_id`，那是新的订单。取消 `DELETE /orders/{id}` 本身是幂等的：目标状态是已取消，重复取消返回当前状态。」
**白板。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 328">
<rect x="8" y="8" width="72" height="38" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="44" y="31" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">App</text>
<rect x="92" y="8" width="72" height="38" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="128" y="31" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">订单 API</text>
<rect x="176" y="8" width="72" height="38" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="212" y="31" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">订单库</text>
<rect x="262" y="8" width="72" height="38" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="298" y="31" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">交易所</text>
<rect x="4" y="64" width="164.24" height="20" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="86.12" y="78" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Review 页：C = 新 UUID</text>
<text x="48" y="100" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">POST /orders {C, 买 100}</text>
<polyline points="44,112 128,112" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="128,112 121.0,115.2 121.0,108.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="132" y="134" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">INSERT … C，PENDING，提交</text>
<polyline points="128,146 212,146" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="212,146 205.0,149.2 205.0,142.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="294" y="168" text-anchor="end" font-size="12" font-family="sans-serif" fill="currentColor">submit(clientOrderId = 订单 id)</text>
<polyline points="128,180 298,180" fill="none" stroke-width="1.3" stroke="currentColor"/>
<polygon points="298,180 291.0,183.2 291.0,176.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="170" y="208" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">响应丢失，用户再点</text>
<text x="48" y="230" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">POST /orders {C, 买 100}</text>
<polyline points="44,242 128,242" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="128,242 121.0,245.2 121.0,238.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="132" y="264" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">INSERT 冲突 → 读订单</text>
<polyline points="128,276 212,276" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="212,276 205.0,279.2 205.0,272.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="48" y="298" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">同一个订单 + 状态</text>
<polyline points="128,310 44,310" fill="none" stroke-width="1.3" stroke-dasharray="4 3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="44,310 51.0,306.8 51.0,313.2" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<line x1="44" y1="48" x2="44" y2="62" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="44" y1="86" x2="44" y2="324" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="128" y1="48" x2="128" y2="62" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="128" y1="86" x2="128" y2="89" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="128" y1="104" x2="128" y2="157" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="128" y1="172" x2="128" y2="197" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="128" y1="212" x2="128" y2="219" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="128" y1="234" x2="128" y2="287" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="128" y1="302" x2="128" y2="324" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="212" y1="48" x2="212" y2="89" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="212" y1="104" x2="212" y2="123" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="212" y1="138" x2="212" y2="157" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="212" y1="172" x2="212" y2="197" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="212" y1="212" x2="212" y2="219" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="212" y1="234" x2="212" y2="253" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="212" y1="268" x2="212" y2="324" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="298" y1="48" x2="298" y2="123" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="298" y1="138" x2="298" y2="324" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="8" y1="204" x2="105.68" y2="204" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="234.32" y1="204" x2="332" y2="204" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
</svg>
白板上：键在 Review 页生成，订单先写库再提交交易所，重试读到同一个订单。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 210">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">崩在哪一步，怎么收敛</text>
<rect x="8" y="26" width="324" height="46" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="18" y="45.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">① 写库之前</text>
<text x="18" y="60.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">没有订单；客户端重试同一个 C，建一个</text>
<rect x="8" y="80" width="324" height="46" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="99.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">② 写库之后、提交交易所之前</text>
<text x="18" y="114.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">PENDING 行：清理任务先查后补</text>
<rect x="8" y="134" width="324" height="46" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="153.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">③ 交易所已收、我们没记下</text>
<text x="18" y="168.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">清理任务按 clientOrderId 查到，补记</text>
<text x="8" y="200" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">同一个 C 永远只对应一个订单</text>
</svg>
白板上：崩在哪一步都能靠同一个 clientOrderId 收敛。

**为什么这样说。** 面试官在看三件事：键什么时候生成、写库和提交交易所的先后、崩溃后怎么知道交易所有没有这个订单。弱的回答是「订单接口做成幂等」，却不说客户端发什么；强的回答把键写进请求体，并把同一个键一直传到交易所。
**面试官可能接着问。**
- 为什么不是服务端生成订单 id 再返回？ → 响应一丢，客户端没有 id 可重发，重试变成新订单。
- 交易所不支持 clientOrderId 怎么办？ → 提交前先把订单和我们自己的引用号写库，提交后以交易所返回的 id 对账；超时就只能查、不能盲目重发。我会和面试官确认交易所的接口能力。
- 同一个 App 的两个设备同时下单呢？ → 两个设备生成两个键，是两个订单；这是产品层要提示的，不是重试问题。
- 订单状态是怎么推进的？ → PENDING、SUBMITTED、PARTIALLY_FILLED、FILLED、CANCELLED、FAILED；推进都走条件更新，每次只前进。
**常见失分。**
- **提交交易所之后才写库：** 崩溃后我们不知道有订单在交易所。
- **重试再向交易所提交一次：** 买两遍。
- **用 (用户, 股票, 数量) 判重：** 用户分两次各买 100 股是合法的。
- **取消没有处理重复：** 对已取消的订单再取消应返回当前状态，而不是报错重试。
