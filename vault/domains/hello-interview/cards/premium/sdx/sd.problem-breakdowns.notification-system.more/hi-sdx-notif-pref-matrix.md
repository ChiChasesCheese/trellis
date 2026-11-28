---
id: hi-sdx-notif-pref-matrix
node: sd.problem-breakdowns.notification-system.more
type: qa
step: 1
---
## Q
**偏好按「类型 × 渠道」建模**｜补充 · 通知系统 · 必会

面试官：「用户要能管理通知偏好。你给每个用户存一个『推送开、邮件关』这样的渠道开关够吗？为什么？」

## A
**结论。** 不够。偏好要存成（用户, 通知类型, 渠道）到开关的矩阵：同一个渠道上，安全提醒要保留，「有人点赞」要关掉，渠道开关表达不了这种差别。

**要点。**
- **渠道开关的缺陷：** 推送关掉就连安全提醒也收不到；推送开着又被点赞刷屏，两头都不对。
- **矩阵的主键：** (userId, notificationType, channel, enabled)，每个类型在每个渠道独立开关。
- **默认策略按类型：** 没有记录时用该类型的默认值，社交类默认只开部分渠道。
- **安全类不可覆盖：** 安全提醒、验证码默认全渠道开启，用户不能关，发送前也不查偏好。
- **读多写少：** 偏好放关系库加缓存，发送前读缓存；用户改了偏好，缓存要失效，让下一次发送用到最新值。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 250">
<text x="126" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">推送</text>
<text x="194" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">短信</text>
<text x="262" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">邮件</text>
<rect x="10" y="26" width="104" height="40" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="62.0" y="42.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">安全提醒</text>
<text x="62.0" y="57.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">不可关闭</text>
<rect x="120" y="26" width="60" height="40" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="150.0" y="50.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">开</text>
<rect x="188" y="26" width="60" height="40" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="218.0" y="50.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">开</text>
<rect x="256" y="26" width="60" height="40" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="286.0" y="50.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">开</text>
<rect x="10" y="74" width="104" height="40" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="62.0" y="90.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">订单状态</text>
<text x="62.0" y="105.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">用户可调</text>
<rect x="120" y="74" width="60" height="40" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="150.0" y="98.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">开</text>
<rect x="188" y="74" width="60" height="40" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="218.0" y="98.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">关</text>
<rect x="256" y="74" width="60" height="40" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="286.0" y="98.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">开</text>
<rect x="10" y="122" width="104" height="40" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="62.0" y="138.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">有人点赞</text>
<text x="62.0" y="153.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">用户可调</text>
<rect x="120" y="122" width="60" height="40" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="150.0" y="146.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">关</text>
<rect x="188" y="122" width="60" height="40" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="218.0" y="146.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">关</text>
<rect x="256" y="122" width="60" height="40" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="286.0" y="146.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">开</text>
<text x="10" y="186" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">主键 (userId, 类型, 渠道) → 开或关</text>
<text x="10" y="204" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">没有记录时用该类型的默认策略</text>
<text x="10" y="222" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">安全类默认全开，用户不能覆盖</text>
</svg>

**为什么。** 用户关心的是「什么事」值得打扰他，渠道只是怎么打扰；把两者拆成两个维度，才能表达「这种事走这个渠道」。

**面试里这样说。** 「偏好我存成（用户, 类型, 渠道）的矩阵，每格独立开关，没记录就用类型默认值；安全提醒和验证码默认全开、用户不能关，也不走偏好检查。这样用户能关掉点赞推送，又不会漏掉安全提醒。」

**易错。**
- **只做渠道级开关：** 要么漏掉重要通知，要么被低价值通知淹没。
- **允许用户关掉安全类：** 账号被盗时用户收不到提醒。
- **偏好改了缓存不失效：** 用户已经关闭的类型还在被发送。
