---
id: hi-mock-notification-02-requirements
node: fix.notification-mock
type: qa
step: 2
---
## Q
**通知系统 · 第 2 步 · 功能与非功能需求**｜模拟面试

面试官：「好，说说需求：功能上做哪几条，非功能上最看重什么？」

你会怎么回答？白板上画到哪一步？

## A
**你说。**
- **先给功能，四条：** 「一，发回执：一次一个用户，带模板和参数。二，发活动：人群编号加模板，由我扇出到逐人。三，查状态：某条消息现在是受理、已发、已送达、失败，还是被退订挡掉。四，偏好和退订：偏好存在偏好服务里，我读取并且执行。」
- **非功能一，投递保证：** 「至少一次（at-least-once）：回 202 之后消息不丢。去重靠唯一键，同一张回执只发一次；极小的重复窗口，我在深入里讲。」
- **非功能二，延迟，按类别写：** 「回执：从受理到交给供应商，p99 ≤ 5 秒。活动：1,000 万人在 10 分钟内发完，不要求每个人几秒内收到。两类目标不同，所以才要隔离。」
- **非功能三，退订：** 「每条消息发送前查一次偏好，偏好缓存的有效期不超过 60 秒，退订最迟约一分钟生效。营销退订不挡回执：一张支付回执是交易通知，不是营销。」
- **非功能四，受理的可用性：** 「受理接口 99.95%，一个月约 22 分钟不可用（30 天 × 24 小时 × 60 分钟 × 0.05% ≈ 21.6 分钟）。发送本身是异步的，不计入这个数。」
- **说不追求的：** 「不保证顺序，不追求每条消息毫秒级送达，不做多区域多活。」
- **点出难点：** 「难在四处：活动不能把回执挤到后面；供应商慢或挂；重试不能变成重复发送；千万级扇出崩溃后要能接着做。」
**白板。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 253">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">功能需求：四条</text>
<rect x="8" y="26" width="324" height="44" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="44.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="bold">① 发回执</text>
<text x="18" y="59.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">一人一条：模板 + 参数 + 用户</text>
<rect x="8" y="78" width="324" height="44" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="96.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="bold">② 发活动</text>
<text x="18" y="111.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">人群编号 + 模板，扇出到逐人</text>
<rect x="8" y="130" width="324" height="59" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="148.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="bold">③ 查状态</text>
<text x="18" y="163.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">accepted · sent · delivered</text>
<text x="18" y="178.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">failed · suppressed（被退订挡掉）</text>
<rect x="8" y="197" width="324" height="44" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="215.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="bold">④ 偏好与退订</text>
<text x="18" y="230.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">偏好服务存，本服务读取并执行</text>
</svg>

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 298">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">非功能需求：每条带数字</text>
<rect x="8" y="26" width="324" height="59" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="44.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="bold">投递保证</text>
<text x="18" y="59.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">至少一次；回 202 之后不丢</text>
<text x="18" y="74.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">同一张回执只发一次（窗口见深入四）</text>
<rect x="8" y="93" width="324" height="59" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="111.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="bold">延迟</text>
<text x="18" y="126.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">回执 p99 ≤ 5 秒：受理到交给供应商</text>
<text x="18" y="141.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">活动 1,000 万人 ≤ 10 分钟发完</text>
<rect x="8" y="160" width="324" height="59" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="178.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="bold">退订</text>
<text x="18" y="193.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">发送前检查，偏好缓存 ≤ 60 秒</text>
<text x="18" y="208.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">退订后最多再收 1 分钟内已在途的</text>
<rect x="8" y="227" width="324" height="59" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="245.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="bold">受理可用性</text>
<text x="18" y="260.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">API 99.95%（每月约 22 分钟不可用）</text>
<text x="18" y="275.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">发送是异步的，不计入</text>
</svg>
白板上新增：左边功能四条，右边非功能四条，每条带数字。
**为什么这样说。** （约 4 分钟，累计第 6 分钟。）面试官看非功能需求是否量化，以及是否包含这类系统独有的几项：投递保证、按类别的延迟、退订。「高可用、低延迟」谁都能说，不得分；「回执 p99 ≤ 5 秒、活动 10 分钟发完」才能推出设计。强的回答把非功能需求逐条连到后面的深入；弱的回答是列一串形容词，没有数字，也漏掉退订。
**面试官可能接着问。**
- 为什么是至少一次，不是至多一次？ → 至多一次会悄悄丢消息，丢了没人知道；至少一次的重复是看得见的，可以去重。回执不能丢，所以选至少一次再去重。
- 退订后还收到消息怎么办？ → 偏好缓存 60 秒，所以最多再收一条已在途的。若合规要求即时生效，把缓存的有效期降到 0，每条发送前读偏好存储，代价是每条消息多一次读，峰值每秒约 8.3 万次，要由缓存集群承担。
- 回执用户选了「不要短信」呢？ → 渠道偏好仍然生效：回执改走推送或邮件。营销退订只挡活动，不挡回执。
- 活动可以晚一点发吗？ → 可以，这正是活动的价值：它能排队、能限速，让出额度给回执。
**常见失分。**
- **只写功能不写非功能：** 面试官看不到你知道难点在哪里。
- **形容词当指标：** 「高可用」没有数字，就推不出任何设计。
- **漏掉退订和偏好：** 他当时没有问，也没有说发送前要检查；合规问题答不上来。
- **不问投递保证：** 后面被问「崩溃之后怎么办」时没有立场可以站。
