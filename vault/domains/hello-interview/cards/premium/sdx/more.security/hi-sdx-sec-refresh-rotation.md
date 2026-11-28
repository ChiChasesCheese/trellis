---
id: hi-sdx-sec-refresh-rotation
node: more.security
type: qa
step: 12
---
## Q
**刷新令牌轮换：被盗变成可检测事件**｜补充 · 安全 · 追问

面试官：「刷新令牌轮换（rotation）怎么把令牌被盗变成可检测的事件？一个旧令牌被再次使用时服务端怎么处理？」

## A
**结论。** 每次刷新都发新的刷新令牌，并让刚用过的作废，每个令牌只能用一次。旧令牌被再次出示，说明同一血统有两方持有令牌，等于被盗的证据，服务端撤销整个令牌家族（整个会话），双方都要重新登录。

**要点。**
- **轮换：** 每次刷新返回新刷新令牌，旧的立即失效。
- **被盗后会怎样：** 贼和合法客户端中先刷新的那一方让另一方的令牌失效。
- **重用检测：** 已轮换的令牌再次出现，就证明同一家族有两份副本。
- **处置：** 撤销整个家族的所有令牌，强制重新认证。
- **为什么对浏览器必须：** 长寿命令牌无法安全存在浏览器里，轮换把窃取窗口压缩到下一次刷新之前。

**为什么。** 贼用盗来的令牌刷新一次，就会让合法用户的下一次刷新带着旧令牌失败；失败这一刻本身就是检测信号。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 232">
<rect x="8" y="14" width="90" height="40" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="53" y="38" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">令牌 1</text>
<rect x="125" y="14" width="90" height="40" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="170" y="38" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">令牌 2</text>
<rect x="242" y="14" width="90" height="40" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="287" y="38" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">令牌 3</text>
<polyline points="98,34 125,34" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="125,34 118.7,37.0 118.7,31.0" style="fill:var(--accent,#3b6fd4)"/>
<polyline points="215,34 242,34" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="242,34 235.7,37.0 235.7,31.0" style="fill:var(--accent,#3b6fd4)"/>
<text x="8" y="80" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">每次刷新：发新的，旧的作废</text>
<polyline points="53,54 53,118" fill="none" stroke-width="1.3" stroke-dasharray="4 3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="53,118 50.0,111.7 56.0,111.7" style="fill:var(--accent,#3b6fd4)"/>
<rect x="8" y="118" width="150" height="44" rx="6" stroke-width="1.2" stroke-dasharray="4 3" fill="none" stroke="currentColor"/>
<text x="83" y="136.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">令牌 1 再次出现</text>
<text x="83" y="151.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">说明被盗</text>
<polyline points="158,140 182,140" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="182,140 175.7,143.0 175.7,137.0" style="fill:var(--accent,#3b6fd4)"/>
<rect x="182" y="118" width="150" height="44" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="257" y="136.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">撤销整个家族</text>
<text x="257" y="151.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">强制重新登录</text>
<text x="8" y="196" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">同一血统出现两份副本</text>
<text x="8" y="216" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">= 被盗的证据</text>
</svg>

**面试里这样说。** 「我对刷新令牌做轮换，每次用完作废并签发新的。旧令牌再次出现就说明被盗，我撤销整个令牌家族，强制重新登录。访问令牌寿命保持在几分钟。」

**易错。**
- **宽限窗口过长：** 并发刷新被误判，或让贼获得可乘之机。
- **只作废单个令牌：** 贼持有的新令牌仍然有效，必须撤销整个家族。
- **并发请求同时刷新：** 需要处理竞态，避免把正常用户踢下线。
