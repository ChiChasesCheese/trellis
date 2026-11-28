---
id: hi-fix-retry-key-03-ticketmaster
node: fix.retry-key
type: qa
step: 4
---
## Q
**Ticketmaster 占座 · 重试键**｜补强

面试官：「用户点座位占座，请求超时了，他再点一次，却看到「这个座位已被占用」，可明明就是他自己占的。怎么修？」

你会怎么回答？白板上画到哪一步？

## A
**你说。**
- **先说出毛病在哪：** 「`SET lock:ticket:T <值> NX EX 600` 第二次返回 nil。我把「抢锁失败」一律当成「被别人占了」，所以连自己的重试也被拒绝。」
- **重试键放在哪里：** 「客户端点座位时生成 `hold_attempt_id`，`POST /holds {ticket_id, hold_attempt_id}`。锁的值不是 user_id，而是这个 attempt id。」
- **第二次的三个分支：** 「`SET … NX` 返回 OK：我拿到了。返回 nil，就 `GET` 一下：值等于我的 attempt id，是我自己的重试，原样返回；不等于，是别人占着，返回已被占用。」
- **不要续命：** 「自己的重试只读，不重置 TTL，否则用户不停点击就能一直占着座位。返回的是剩余的 540 秒。」
- **booking 行也要幂等：** 「锁拿到之后插一行 booking，`UNIQUE (hold_attempt_id)`。进程在拿锁和插行之间崩了，重试进来看到自己的锁，再插一次，冲突就读已有的行。两步随便哪一步崩，重试都能接上。」
- **多个座位：** 「一次选多个座位，所有座位用同一个 attempt id，依次抢；有一个失败就释放已抢到的，释放时同样检查值是我的 attempt id 才删。」
- **支付边界：** 「创建 PaymentIntent 时用 booking_id 当幂等键，两层各有一个稳定的键。」
**白板。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 430">
<rect x="8" y="8" width="72" height="38" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="44" y="31" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">浏览器</text>
<rect x="92" y="8" width="72" height="38" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="128" y="31" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">API</text>
<rect x="176" y="8" width="72" height="38" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="212" y="31" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Redis</text>
<rect x="262" y="8" width="72" height="38" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="298" y="31" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">数据库</text>
<rect x="4" y="64" width="141.44" height="20" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="74.72" y="78" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">点座位：A = 新 UUID</text>
<text x="48" y="100" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">POST /holds {座位, A}</text>
<polyline points="44,112 128,112" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="128,112 121.0,115.2 121.0,108.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="132" y="134" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">SET lock:T A NX EX 600</text>
<polyline points="128,146 212,146" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="212,146 205.0,149.2 205.0,142.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="132" y="168" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">OK</text>
<polyline points="212,180 128,180" fill="none" stroke-width="1.3" stroke-dasharray="4 3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="128,180 135.0,176.8 135.0,183.2" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="132" y="202" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">INSERT booking（A 唯一）</text>
<polyline points="128,214 298,214" fill="none" stroke-width="1.3" stroke="currentColor"/>
<polygon points="298,214 291.0,217.2 291.0,210.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="170" y="242" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">响应丢失，用户再点</text>
<text x="48" y="264" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">同样的请求（同一个 A）</text>
<polyline points="44,276 128,276" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="128,276 121.0,279.2 121.0,272.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="132" y="298" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">SET … NX → nil</text>
<polyline points="128,310 212,310" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="212,310 205.0,313.2 205.0,306.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="132" y="332" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">GET lock:T → A</text>
<polyline points="128,344 212,344" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="212,344 205.0,347.2 205.0,340.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="132" y="366" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">INSERT 冲突 → 读 booking</text>
<polyline points="128,378 298,378" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="298,378 291.0,381.2 291.0,374.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="48" y="400" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">同一个 booking，剩 540 秒</text>
<polyline points="128,412 44,412" fill="none" stroke-width="1.3" stroke-dasharray="4 3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="44,412 51.0,408.8 51.0,415.2" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<line x1="44" y1="48" x2="44" y2="62" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="44" y1="86" x2="44" y2="426" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="128" y1="48" x2="128" y2="62" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="128" y1="86" x2="128" y2="89" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="128" y1="104" x2="128" y2="231" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="128" y1="246" x2="128" y2="253" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="128" y1="268" x2="128" y2="389" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="128" y1="404" x2="128" y2="426" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="212" y1="48" x2="212" y2="123" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="212" y1="138" x2="212" y2="191" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="212" y1="206" x2="212" y2="231" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="212" y1="246" x2="212" y2="287" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="212" y1="302" x2="212" y2="321" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="212" y1="336" x2="212" y2="355" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="212" y1="370" x2="212" y2="389" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="212" y1="404" x2="212" y2="426" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="298" y1="48" x2="298" y2="191" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="298" y1="206" x2="298" y2="355" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="298" y1="370" x2="298" y2="426" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="8" y1="238" x2="105.68" y2="238" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="234.32" y1="238" x2="332" y2="238" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
</svg>
白板上：键放进锁的值；重试时 SET NX 返回 nil，GET 出来是自己的键，返回同一个 booking，TTL 不变。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 210">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">SET lock:T &lt;A&gt; NX EX 600 的三种结果</text>
<rect x="8" y="26" width="324" height="46" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="18" y="45.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">OK</text>
<text x="18" y="60.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">我拿到了：新建 booking</text>
<rect x="8" y="80" width="324" height="46" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="99.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">nil，GET 出来是我的 A</text>
<text x="18" y="114.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">是我的重试：返回原 booking，TTL 不动</text>
<rect x="8" y="134" width="324" height="46" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="18" y="153.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">nil，GET 出来是别人的</text>
<text x="18" y="168.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">座位被占：返回已被占用</text>
<text x="8" y="200" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">没有第二个键：值里放的就是重试键</text>
</svg>
白板上：SET NX 的三种结果，加重的一行是重试。

**为什么这样说。** 面试官在测你有没有把「抢锁失败」细分成「别人占了」和「自己重试」。弱的回答只说 Redis `SET NX` 是原子的，没人能抢到同一把锁，漏掉了自己重试会被误拒。强的回答把重试键放进锁的值，用一次 `GET` 区分，并说清楚不能续命。
**面试官可能接着问。**
- 为什么锁的值不用 user_id？ → 同一个用户可能开两个标签页，值是 user_id 时两个页签互相认为是对方的重试；值是 attempt id，第二个页签得到「已被占用」，语义更准确。
- `SET` 之后 `GET` 之前锁过期了呢？ → `GET` 返回 nil：我再 `SET NX` 一次，座位没被别人占就重新拿到，被占了就返回已被占用。这个窗口很小，结果都是正确的。
- 释放锁怎么写？ → 用 Lua 脚本：值等于我的 attempt id 才 `DEL`，避免删掉别人的锁。
- TTL 在支付时过期怎么办？ → 数据库的条件更新（座位仍是 available）仍是最后一道闸；输家自动退款，支付时可以延长锁。
**常见失分。**
- **只说 SET NX 是原子的：** 原子只保证互斥，没解决自己重试被拒绝。
- **重试时又 SET 覆盖：** 没有 NX 的 `SET` 会让别人的锁被抢走，或者重置 TTL。
- **锁的值是常量：** 谁都能删、谁都能当自己，没法认出重试。
- **重试把 TTL 续上：** 一直点击就能一直占座。
