---
id: bagu-card-tokenization-pci-1-token-scope
node: b.scenario.card-tokenization-pci
type: qa
step: 1
---
## Q
**卡号令牌化 · PCI 范围与日志泄露**｜追问

面试官：「商户后端为什么不该碰卡号？令牌化和加密有什么区别？怎么让大部分系统不进 PCI 范围，日志里又怎么保证没有卡号？」

## A
**基本回答。** PCI DSS 是卡组织制定的行业标准，靠收单合同约束，不是法律；存储、处理、传输卡号（PAN）的系统及与它相连的系统都在范围内，要按最严格的标准审计。令牌化把卡号换成无意义的令牌，真卡号只在隔离的令牌金库；业务系统只存令牌、品牌和末四位，范围缩到金库一处。加密可逆（有密钥就能还原），密文仍算卡数据；随机令牌与卡号没有数学关系，只能向金库查，泄露令牌盗刷不了，通常还绑定商户。卡号输入用 PSP 的托管表单（hosted fields，嵌入页面的 iframe）或跳转收银台，卡号从浏览器直达 PSP，商户服务器只拿令牌，自评问卷通常可从 SAQ D 降到 SAQ A。CVV 授权后不得存储，加密也不行；展示最多露 BIN 和末四位。日志用字段白名单、默认不记请求体，遗留的收卡号接口改成只收令牌；再对日志和消息队列持续扫描 13–19 位数字串并用 Luhn 校验，命中告警：白名单是预防，扫描是发现漏网。
**2026 亮点。** 卡组织的网络令牌（network token）会随换卡、过期自动更新，授权率更高；PSP 自己的令牌省事但绑定该 PSP，要多渠道路由就得自建或用独立金库，金库本身仍在严格范围内。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 236">
<text x="250" y="16" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">PCI 范围缩到这一处</text>
<rect x="8" y="28" width="96" height="48" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="56" y="48.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">浏览器</text>
<text x="56" y="63.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">输入卡号</text>
<line x1="104" y1="52" x2="168" y2="52" stroke-width="1.2" stroke="currentColor"/>
<polygon points="168.0,52.0 161.0,55.2 161.0,48.8" fill="currentColor" stroke-width="0.5" stroke="currentColor"/>
<text x="136" y="44" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">卡号</text>
<rect x="168" y="28" width="164" height="48" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="250" y="48.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">PSP 托管表单</text>
<text x="250" y="63.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">令牌金库（存真卡号）</text>
<line x1="250" y1="76" x2="250" y2="126" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="250.0,126.0 246.8,119.0 253.2,119.0" style="fill:var(--accent,#3b6fd4)" stroke-width="0.5" style="stroke:var(--accent,#3b6fd4)"/>
<text x="258" y="98" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">令牌</text>
<text x="258" y="114" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">tok_8f3a</text>
<rect x="8" y="126" width="324" height="48" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170" y="146.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">商户后端、日志、数据仓库</text>
<text x="170" y="161.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">只存：令牌、品牌、末四位</text>
<line x1="8" y1="190" x2="332" y2="190" stroke-width="1.2" style="stroke:var(--dim,#6b7280)" stroke-dasharray="4 3"/>
<text x="170" y="210" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">日志持续扫描：13 到 19 位数字 + Luhn 校验</text>
<text x="170" y="228" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">命中就告警，并定位来源接口</text>
</svg>
卡号只走浏览器到 PSP 这一条路，商户后端、日志和数据仓库拿到的永远只是令牌，不在 PCI 范围内。
**举个例子。** 用户付款 4242 4242 4242 4242：卡号经托管表单直达 PSP，金库存真卡号、返回 `tok_8f3a`；商户库只存 `tok_8f3a`、VISA、4242；扣款时商户拿令牌请 PSP，PSP 在金库换回卡号发给卡组织。工程师临时打开网关调试日志，请求体里只有令牌，扫描器不告警；若有人把 4242424242424242 写进日志，16 位且 Luhn 通过，立刻告警。
**容易错。**
- **以为数据库加密了就出范围：** 存的还是 PAN，加密后仍是卡数据；出范围靠根本不保存卡号。
- **只靠白名单不扫描：** 管不到遗留接口和第三方组件。
