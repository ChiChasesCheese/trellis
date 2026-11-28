---
id: hi-sdx-email-message-mailboxentry
node: more.email-service
type: qa
step: 2
---
## Q
**邮件内容和用户状态分两张表**｜补充 · 邮件服务（Gmail） · 必会

面试官：「邮箱里一封信有正文、附件，也有每个收件人自己的已读、标签、星标。你把它们放在同一行里吗？一次『标记已读』在你的存储里会写多少字节？」

## A
**结论。** 不放同一行，拆成两张表：不可变的消息表（Message，收到时写一次）和按用户分区的邮箱条目表（MailboxEntry，只存引用加可变状态）。标记已读只改一行几十字节的条目，完全不碰正文。

**要点。**
- **同行的代价：** 已读是几个字节的改动，却要重写含整封正文的那一行，写放大和信的大小成正比。
- **Message 只写一次：** 头部、正文引用、附件引用，之后永不修改，可以放心缓存、去重、复制。
- **MailboxEntry 按用户：** 键为 (user_id, 时间或 message_id)，存 message_id 引用、flags、标签、会话 id。
- **读路径变便宜：** 列收件箱是在条目表上按用户范围扫描，只有打开某封信才去取正文。
- **抄送天然共享：** 发给 N 人的信是一份 Message 加 N 行条目，正文不复制 N 份。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 226">
<rect x="10" y="8" width="320" height="44" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="170.0" y="26.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Message（只写一次，不可变）</text>
<text x="170.0" y="41.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">头部 · 正文引用 · 附件引用</text>
<polyline points="60,52 60.0,85.0" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="60,92 56.8,85.0 63.2,85.0" style="fill:var(--accent,#3b6fd4)"/>
<polyline points="170,52 170.0,85.0" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="170,92 166.8,85.0 173.2,85.0" style="fill:var(--accent,#3b6fd4)"/>
<polyline points="280,52 280.0,85.0" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="280,92 276.8,85.0 283.2,85.0" style="fill:var(--accent,#3b6fd4)"/>
<text x="178" y="76" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">按 message_id 引用</text>
<rect x="10" y="92" width="100" height="56" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="60.0" y="109.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">MailboxEntry</text>
<text x="60.0" y="124.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">用户 A</text>
<text x="60.0" y="139.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">已读 · 标签</text>
<rect x="120" y="92" width="100" height="56" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170.0" y="109.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">MailboxEntry</text>
<text x="170.0" y="124.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">用户 B</text>
<text x="170.0" y="139.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">星标 · 文件夹</text>
<rect x="230" y="92" width="100" height="56" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="280.0" y="109.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">MailboxEntry</text>
<text x="280.0" y="124.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">用户 C</text>
<text x="280.0" y="139.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">未读 · 会话</text>
<text x="10" y="176" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">标记已读：只改自己那一行，几十字节</text>
<text x="10" y="194" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">列收件箱：按 user_id 范围扫描，不读正文</text>
<text x="10" y="212" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">抄送 N 人：一份 Message，N 行 MailboxEntry</text>
</svg>

**为什么。** 按「谁来写、多频繁」切数据：内容低频且不变，状态高频且每人各异。混在一行里，高频的小改动就要连带搬运低频的大对象。

**面试里这样说。** 「我把一封信拆成不可变的 Message 和按 user_id 分区的 MailboxEntry。已读、标签只更新自己那一行，几十字节，不碰正文；列收件箱是条目表上的范围扫描，抄送 N 人也只存一份正文。」

**易错。**
- **状态内嵌在消息行：** 每次已读都重写正文，高频小写变成大写，分区也无法按用户切。
- **每个收件人复制一份正文：** 群发和抄送的存储按收件人数放大。
- **把条目表按 message_id 分区：** 列收件箱要跨分区拼接，应按 user_id 分区。
