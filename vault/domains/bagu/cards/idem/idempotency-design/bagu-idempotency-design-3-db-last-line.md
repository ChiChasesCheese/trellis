---
id: bagu-idempotency-design-3-db-last-line
node: a.idem.idempotency-design
type: qa
step: 3
---
## Q
**幂等 · 最终防线为什么是数据库**｜必会

面试官：「用 Redis 的 token 或锁做幂等不是更快吗？为什么说最终防线必须是数据库唯一约束？」

## A
**基本回答。** Redis 的 token 或锁可能丢（主从切换、过期），所以只能挡掉绝大多数重复、降低数据库压力；最终的防线必须是数据库的唯一约束或条件更新。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 196">
<rect x="20" y="6" width="190" height="28" rx="3" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="115" y="24.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">请求（可能重复）</text>
<line x1="115" y1="34" x2="115" y2="52" stroke-width="1.2" stroke="currentColor"/>
<polygon points="115.0,52.0 111.8,45.0 118.2,45.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="20" y="52" width="190" height="42" rx="3" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="115" y="70" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Redis token 或锁</text>
<text x="115" y="85" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">挡掉绝大多数重复</text>
<line x1="115" y1="94" x2="115" y2="116" stroke-width="1.2" stroke="currentColor"/>
<polygon points="115.0,116.0 111.8,109.0 118.2,109.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="124" y="110" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">放行</text>
<rect x="20" y="116" width="190" height="42" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="115" y="134" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">数据库唯一约束或</text>
<text x="115" y="149" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">条件更新：最终防线</text>
<line x1="210" y1="73" x2="228" y2="73" stroke-width="1.2" style="stroke:var(--dim,#6b7280)" stroke-dasharray="4 3"/>
<line x1="228" y1="73" x2="228" y2="137" stroke-width="1.2" style="stroke:var(--dim,#6b7280)" stroke-dasharray="4 3"/>
<line x1="228" y1="137" x2="212" y2="137" stroke-width="1.2" style="stroke:var(--dim,#6b7280)" stroke-dasharray="4 3"/>
<polygon points="212.0,137.0 219.0,133.8 219.0,140.2" style="fill:var(--dim,#6b7280);stroke:var(--dim,#6b7280)" stroke-width="0.5"/>
<text x="236" y="100" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">token 丢了</text>
<text x="236" y="118" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">请求漏下来</text>
<text x="8" y="184" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">撞唯一键，第二笔就失败了</text>
</svg>
请求先经过 Redis 这一层，它挡掉绝大多数重复；但 Redis 有时会丢数据，漏下来的请求（右边虚线）会直接到达数据库，这时靠唯一约束或条件更新兜底，撞键的那一笔失败。
**容易错。**
- **以为 Redis 够快就够用：**快不代表可靠。主从切换丢数据和 key 过期都会让 token 失效。
- **GET 之后再 DEL：**两步之间别的请求也能 GET 成功，两个请求都拿到 token；要用 `GETDEL`（Redis 6.2.0 起）或 Lua 一次完成检查并删除，只有消费成功的那个才执行业务。
- **资金接口 Redis 挂了就放行：**没法确认是否重复，放行就可能重复扣款，宁可失败。

