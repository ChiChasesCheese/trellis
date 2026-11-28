---
id: bagu-waiting-room-1-admission-token
node: b.scenario.waiting-room
type: qa
step: 1
---
## Q
**排队室 · 准入令牌、抽签与客户端退避**｜追问

面试官：「演唱会开售，一百万人同一秒涌入，票只有一千张。入口怎么削峰、怎么公平地放人？」

## A
**基本回答。** 在库存服务前加准入层：用户先进排队室领一张服务端签名的准入令牌，只有带有效令牌的请求才到预占服务，其余得到明确的「请排队」或「未抽中」。放行速率跟库存路径容量挂钩（预占一秒能处理多少次就放多少人），不是在线人数。排队页轮询是 100 万人每 2 秒一次、响应相同的小 JSON，由 CDN 缓存吸收，不打源站。令牌含用户、商品、过期时间（如 10 分钟），用服务端密钥 HMAC 签名，网关无状态验证，绑定用户，转手无效。真排队有状态、体验好（看得到前面多少人），但奖励网络最快的人和脚本；抽签无状态：对 `H(密钥, user_id, sale_id)` 取模，小于阈值中签（1000 张票放行约 2000 人即 0.2%），同一账号结果固定、换 IP 没用，代价是不是严格先到先得，要在产品上说明并依赖实名和风控防多账号。客户端收到 429 要指数退避加随机抖动（jitter）：服务端限流只负责拒绝，不退避的客户端把每个失败请求变成十个，放大成重试风暴。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 306">
<rect x="10" y="8" width="320" height="34" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170" y="29" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">100 万人同一秒涌入</text>
<line x1="170" y1="42" x2="170" y2="58" stroke-width="1.2" stroke="currentColor"/>
<polygon points="170.0,58.0 166.8,51.0 173.2,51.0" fill="currentColor" stroke-width="0.5" stroke="currentColor"/>
<rect x="30" y="58" width="280" height="34" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170" y="79" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">排队室：轮询小 JSON，由 CDN 吸收</text>
<line x1="170" y1="92" x2="170" y2="108" stroke-width="1.2" stroke="currentColor"/>
<polygon points="170.0,108.0 166.8,101.0 173.2,101.0" fill="currentColor" stroke-width="0.5" stroke="currentColor"/>
<rect x="50" y="108" width="240" height="44" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170" y="126.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">抽签或排队，放行约 2000 人</text>
<text x="170" y="141.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">中签率约 0.2%</text>
<line x1="170" y1="152" x2="170" y2="168" stroke-width="1.2" stroke="currentColor"/>
<polygon points="170.0,168.0 166.8,161.0 173.2,161.0" fill="currentColor" stroke-width="0.5" stroke="currentColor"/>
<rect x="70" y="168" width="200" height="44" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170" y="186.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">发准入令牌（HMAC 签名）</text>
<text x="170" y="201.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">用户、商品、10 分钟过期</text>
<line x1="170" y1="212" x2="170" y2="228" stroke-width="1.2" stroke="currentColor"/>
<polygon points="170.0,228.0 166.8,221.0 173.2,221.0" fill="currentColor" stroke-width="0.5" stroke="currentColor"/>
<rect x="90" y="228" width="160" height="36" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170" y="242.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">预占服务</text>
<text x="170" y="257.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">库存 1000 张</text>
<text x="170" y="284" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">没中签：立刻看到明确结果；收到 429：</text>
<text x="170" y="300" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">指数退避 + 随机抖动，不要立刻重刷</text>
</svg>
请求像漏斗一样逐层变少：百万人先被排队室和 CDN 挡在外面，只有拿到令牌的约 2000 人才打到库存服务。
**举个例子。** 1000 张票放行 2000 人：100 万人进排队页，CDN 返回轮询，源站无感；每人算 `H(密钥, user_id, sale_id)` 取模，小于 0.2% 阈值中签，未中签立刻看到「未抽中」；中签者拿 HMAC 签名令牌，约 2000 个请求按库存路径速率到预占服务，伪造或转手的令牌验不过；个别 429 的客户端按 1 秒、2 秒、4 秒加抖动退避。
**容易错。**
- **按在线人数定放行速率：** 在线人数与库存服务承受力无关。
- **只做服务端限流：** 客户端退避加抖动也必须有。
