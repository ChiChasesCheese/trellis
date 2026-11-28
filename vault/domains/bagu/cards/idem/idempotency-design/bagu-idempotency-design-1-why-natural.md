---
id: bagu-idempotency-design-1-why-natural
node: a.idem.idempotency-design
type: qa
step: 1
---
## Q
**幂等 · 为什么要做、哪些天然幂等**｜必会

面试官：「用户连点打赏按钮，扣了两次币。为什么接口要做幂等？哪些操作天然幂等？」

## A
**基本回答。** 幂等（idempotency）是同一个操作执行一次和执行多次，结果相同。网络只能保证「至少送达一次」：超时重试、网关重试、MQ 重投、用户连点，都会带来重复请求，所以幂等是服务端对外的契约，不能指望客户端只发一次。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 196">
<rect x="8" y="10" width="128" height="28" rx="3" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="72" y="28.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">用户连点</text>
<line x1="136" y1="24" x2="196" y2="84" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="196.0,84.0 188.8,81.3 193.3,76.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<rect x="8" y="46" width="128" height="28" rx="3" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="72" y="64.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">网关或框架重试</text>
<line x1="136" y1="60" x2="196" y2="84" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="196.0,84.0 188.3,84.4 190.7,78.4" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<rect x="8" y="82" width="128" height="28" rx="3" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="72" y="100.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">MQ 重复投递</text>
<line x1="136" y1="96" x2="196" y2="84" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="196.0,84.0 189.8,88.5 188.5,82.2" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<rect x="8" y="118" width="128" height="28" rx="3" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="72" y="136.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">运维手工补发</text>
<line x1="136" y1="132" x2="196" y2="84" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="196.0,84.0 192.5,90.9 188.5,85.9" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<rect x="196" y="56" width="136" height="56" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="264" y="73.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">打赏接口</text>
<text x="264" y="88.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">同一笔扣币</text>
<text x="264" y="103.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">可能执行 N 次</text>
<text x="8" y="170" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">幂等：执行 1 次 和执行 N 次，结果一样</text>
<text x="8" y="190" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">所以要在服务端兜住，别指望只发一次</text>
</svg>
左边是四种会让同一个请求重复到达的来源，箭头都指向同一个接口：只要有一处重复，同一笔扣币就可能执行不止一次，所以兜底要放在服务端。
**容易错。**
- **以为按钮置灰就够：**置灰只降低概率；用户刷新、重放请求、网关重试都绕得过去。
- **以为超时一定是失败：**超时只说明没收到响应，请求可能已经执行，客户端重发才会产生重复。
- **以为删除报错就不幂等：**幂等看的是最终状态一致，不是返回值一致；第二次删除影响 0 行，状态没变，仍然幂等。
- **以为插入天然幂等：**没有唯一约束的插入，每执行一次就多一行。
**举个例子。** 余额 500 币打赏 100 币，请求被网关重试到达 3 次：`balance = balance - 100` 相对变化执行 3 次余额变 200，多扣 200，不幂等；`SET balance = 400` 绝对赋值执行几次都是 400，天然幂等，但资金不能这样写，并发下会覆盖别人的改动；`DELETE ... WHERE id = 7` 第二次影响 0 行，返回值不同但最终状态相同，仍是幂等。发通知、调外部扣款、无唯一约束的插入都天然不幂等。补救：给每次打赏一个幂等键加唯一约束，第 2、3 次撞键失败。
