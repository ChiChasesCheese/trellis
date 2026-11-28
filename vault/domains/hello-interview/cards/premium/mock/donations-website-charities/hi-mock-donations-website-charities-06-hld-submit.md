---
id: hi-mock-donations-website-charities-06-hld-submit
node: qb.sd.donations-website-charities.mock
type: qa
step: 6
---
## Q
**限时捐款网站 · 第 6 步 · 高层设计（一）：提交捐款**｜模拟面试

面试官：「很好，现在开始画高层设计，先从提交捐款这条流程开始。」

你会怎么回答？白板上画到哪一步？

## A
**你说。**
- **打法：** 按功能一条条叠：先让提交捐款跑通，再加收据，再用非功能需求带出深入问题。
- **五块：** 浏览器、PSP 前端组件、捐款 API（无状态多实例）、数据库、主 PSP。卡号只走浏览器到 PSP 前端组件这一条线，PSP 回一次性令牌。
- **提交流程：** 浏览器 `POST /donations`（带 donationId、令牌）；API 先 INSERT 一行 CREATED，主键 donationId，已存在就直接返回当前状态；再 `UPDATE … SET status='PROCESSING' WHERE id=? AND status='CREATED'`，影响 1 行才继续；调 PSP 创建并确认支付，donationId 同时作 PSP 幂等键，超时 10 秒；成功写 SUCCEEDED，明确拒绝写 FAILED，超时或 5xx 写 UNKNOWN；返回 status。
- **为什么先落库再调 PSP：** 先调后写，崩在中间就是「扣了款没记录」，最不能出的事故；先落库，崩溃后至少留下 CREATED 或 PROCESSING 供对账找到。
- **事务不跨 PSP：** 条件更新立刻提交，PSP 调用不包在事务里，否则尖峰时连接被占光。
- **主动留白：** 收据怎么发、超时之后怎么办、三层防重复的细节先不管，后两个是深入重点。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 486">
<rect x="8" y="8" width="72" height="38" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="44" y="23.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">浏览器</text>
<text x="44" y="38.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">捐款页</text>
<rect x="92" y="8" width="72" height="38" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="128" y="23.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">API</text>
<text x="128" y="38.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">无状态</text>
<rect x="176" y="8" width="72" height="38" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="212" y="23.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">数据库</text>
<text x="212" y="38.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">Postgres</text>
<rect x="262" y="8" width="72" height="38" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="298" y="23.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">PSP</text>
<text x="298" y="38.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">主</text>
<rect x="5.68" y="64" width="76.64" height="20" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="44" y="78" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">id = UUID</text>
<text x="48" y="100" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">卡号 → PSP 前端组件</text>
<polyline points="44,112 298,112" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="298,112 291.0,115.2 291.0,108.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="48" y="134" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">一次性令牌</text>
<polyline points="298,146 44,146" fill="none" stroke-width="1.3" stroke-dasharray="4 3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="44,146 51.0,142.8 51.0,149.2" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="48" y="168" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">POST /donations</text>
<polyline points="44,180 128,180" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="128,180 121.0,183.2 121.0,176.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="132" y="202" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">INSERT（主键 donationId）</text>
<polyline points="128,214 212,214" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="212,214 205.0,217.2 205.0,210.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<rect x="180.64" y="228" width="62.72" height="20" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="212" y="242" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">CREATED</text>
<text x="132" y="264" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">UPDATE … WHERE CREATED</text>
<polyline points="128,276 212,276" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="212,276 205.0,279.2 205.0,272.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<rect x="170.2" y="290" width="83.6" height="20" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="212" y="304" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">PROCESSING</text>
<text x="132" y="326" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">charge(令牌, 幂等键 = id)</text>
<polyline points="128,338 298,338" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="298,338 291.0,341.2 291.0,334.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="132" y="360" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">成功 / 拒绝 / 超时</text>
<polyline points="298,372 128,372" fill="none" stroke-width="1.3" stroke-dasharray="4 3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="128,372 135.0,368.8 135.0,375.2" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="132" y="394" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">写结果（单独一次提交）</text>
<polyline points="128,406 212,406" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="212,406 205.0,409.2 205.0,402.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<rect x="173.68" y="420" width="76.64" height="20" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="212" y="434" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">SUCCEEDED</text>
<text x="48" y="456" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">{donationId, status}</text>
<polyline points="128,468 44,468" fill="none" stroke-width="1.3" stroke-dasharray="4 3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="44,468 51.0,464.8 51.0,471.2" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<line x1="44" y1="48" x2="44" y2="62" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="44" y1="86" x2="44" y2="482" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="128" y1="48" x2="128" y2="89" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="128" y1="104" x2="128" y2="157" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="128" y1="172" x2="128" y2="445" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="128" y1="460" x2="128" y2="482" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="212" y1="48" x2="212" y2="191" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="212" y1="206" x2="212" y2="226" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="212" y1="250" x2="212" y2="253" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="212" y1="268" x2="212" y2="288" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="212" y1="312" x2="212" y2="315" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="212" y1="330" x2="212" y2="349" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="212" y1="364" x2="212" y2="383" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="212" y1="398" x2="212" y2="418" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="212" y1="442" x2="212" y2="482" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="298" y1="48" x2="298" y2="191" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="298" y1="206" x2="298" y2="315" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="298" y1="330" x2="298" y2="482" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
</svg>
白板上新增：同一条流程按时间画出来；数据库一侧的状态依次是 CREATED、PROCESSING、SUCCEEDED。

**常见失分。**
- **一上来画满：** 队列、Redis、熔断全上，请求怎么走却没讲清。
- **先扣款再写库：** 崩溃时扣了款没记录。
- **事务包住 PSP 调用：** 连接被占光，整站被拖死。
- **不说令牌化：** 面试官会追问合规。

**面试官可能接着问。**
- 为什么不让浏览器直接调 PSP 扣款？ → 金额和机构要由服务端决定并落库；直接扣款我们不知道钱到没到，没有 webhook 这个缺口补不上。
- 同步等 PSP 会拖慢吗？ → 约 0.5 秒可接受；尖峰线程会堵在 PSP 上，深入三用并发上限加排队解决。
- 调 PSP 途中崩了？ → 那行停在 PROCESSING，对账任务用同一幂等键去 PSP 查，不会丢。
- 为什么用关系库？ → 每笔按主键读写，要的是条件更新和事务。
