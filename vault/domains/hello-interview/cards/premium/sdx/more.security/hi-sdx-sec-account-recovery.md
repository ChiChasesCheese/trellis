---
id: hi-sdx-sec-account-recovery
node: more.security
type: qa
step: 15
---
## Q
**只用通行密钥登录，恢复流程才是真实安全等级**｜补充 · 安全 · 追问

面试官：「你上线了纯通行密钥登录。为什么账号真实的安全等级可能还是『短信』？账号恢复该怎么设计？」

## A
**结论。** 账号的安全强度取决于最弱的会话获取路径。攻击者不会破解通行密钥，而是走「我丢了设备」流程。恢复若是邮件魔法链接、短信验证码（换卡）或客服电话，这条路径就成了真正的认证机制。

**要点。**
- **先防丢设备：** 注册时要求至少 2 个通行密钥（手机加笔记本或安全密钥），再发一次性恢复码，只显示一次，哈希存储。
- **恢复走重新注册：** 用另一个凭据证明身份，而不是证明拥有一个邮箱。
- **兜底路径要又慢又吵：** 延迟几小时到几天，通知所有已注册渠道，附带取消链接，让真正的主人能否决。
- **成功后全部撤销：** 所有会话、刷新令牌、API 密钥；提现和修改恢复方式等高风险操作冷却一段时间。
- **客服是攻击面：** 需要带外验证的身份证明，不能凭来电者一句话替他登记新因素。
- **不要用知识问题：** 母亲的姓氏是公开信息，不是秘密。

**为什么。** 攻击者需要安静和速度；兜底路径刻意变慢、变吵，就把这两样都拿走了。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 262">
<rect x="100" y="8" width="140" height="34" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="170" y="29" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">攻击者</text>
<polyline points="130,42 80,78" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="80,78 83.3,71.8 86.9,76.8" style="fill:var(--accent,#3b6fd4)"/>
<polyline points="210,42 262,78" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="262,78 255.1,76.9 258.6,71.9" style="fill:var(--accent,#3b6fd4)"/>
<rect x="8" y="78" width="150" height="52" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="83" y="100.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">通行密钥登录</text>
<text x="83" y="115.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">私钥签名，难攻破</text>
<rect x="182" y="78" width="150" height="52" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="257" y="100.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">「我丢了设备」</text>
<text x="257" y="115.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">短信 · 邮件 · 客服</text>
<polyline points="83,130 130,164" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="130,164 123.1,162.8 126.7,157.8" style="fill:var(--accent,#3b6fd4)"/>
<polyline points="257,130 210,164" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="210,164 213.3,157.8 216.9,162.8" style="fill:var(--accent,#3b6fd4)"/>
<rect x="100" y="164" width="140" height="34" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="170" y="185" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">拿到会话</text>
<text x="8" y="224" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">安全强度 = 最弱的那条路径</text>
<text x="8" y="246" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">恢复要慢、要吵、成功后撤销全部会话</text>
</svg>

**面试里这样说。** 「恢复流程决定真实安全等级。我要求注册至少两个通行密钥并发一次性恢复码；兜底路径设几小时延迟并通知所有渠道，主人可取消；恢复成功后撤销所有会话和令牌，并冷却高风险操作。」

**易错。**
- **恢复走短信或邮件链接：** 强因素形同虚设。
- **客服可直接重置因素：** 社会工程的入口。
- **恢复后不撤销旧会话：** 攻击者的会话仍在。
