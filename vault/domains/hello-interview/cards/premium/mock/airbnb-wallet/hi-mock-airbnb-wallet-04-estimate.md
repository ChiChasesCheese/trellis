---
id: hi-mock-airbnb-wallet-04-estimate
node: fix.airbnb-wallet-mock
type: qa
step: 4
---
## Q
**Airbnb Wallet · 第 4 步 · 估算（每行带单位）**｜模拟面试

面试官：「有没有什么数字想先算一下？」

你会怎么回答？白板上画到哪一步？

## A
**你说。**
- **规矩：** 每行等号两边写单位，除完用 10 的幂回算；1,000 万用户、每周 1 笔转账、每天 2 次读是面试官给的。
- **转账速率：** 1,000 万 × 1 笔/人/周 = 1,000 万笔/周；÷ 604,800 秒 ≈ 16.5 笔/秒（回算 1e7 ÷ 6e5 ≈ 17）。峰值取 3 倍（我的假设，钱包没有明显忙时，用全天再乘 3）≈ 50 笔/秒。
- **年计数：** 1,000 万 × 52 周 = 5.2 亿笔/年（1e7 × 52 = 5.2e8，不是 5,200 万）。
- **读：** 1,000 万 × 2 次/天 = 2,000 万次/天 ÷ 86,400 ≈ 231 次/秒，峰值约 694 次/秒，读比写约 14:1，绝对值都很小。
- **写行数：** 每笔提现约写 5 行（建交易、冻结改钱包、存平台 id、改状态、改钱包）：50 × 5 = 250 行/秒。
- **存储：** 每笔约 500 字节（字段约 200，加行头对齐，保守取值）：5.2 亿 × 500 字节 = 260 GB/年，7 年 1.82 TB，索引 ×2 ≈ 3.6 TB。
- **平台调用并发：** 每次约 1 秒（假设）：50 次/秒 × 1 秒 = 50 个在飞；平台额度 100 次/秒，新建转账占一半，剩下留给刷新和扫描。
- **决定：** 读 694/秒、写 250 行/秒、3.6 TB：一个 Postgres 主库加一台同步备库，不分片，不加缓存。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 269">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">年计数与存储：字节要换成 GB、TB</text>
<rect x="8" y="26" width="324" height="61" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="45.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">每年转账数</text>
<text x="18" y="60.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">10,000,000 人 × 52 周/年</text>
<text x="18" y="75.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">= 520,000,000 笔/年（5.2 亿，不是 5,200 万）</text>
<rect x="8" y="95" width="324" height="61" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="114.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">原始存储/年</text>
<text x="18" y="129.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">5.2 亿 笔 × 500 字节/笔</text>
<text x="18" y="144.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">= 260 GB/年</text>
<rect x="8" y="164" width="324" height="61" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="183.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">保留 7 年</text>
<text x="18" y="198.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">260 GB/年 × 7 年</text>
<text x="18" y="213.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">= 1.82 TB；索引约 ×2 = 3.6 TB</text>
<text x="8" y="241" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">3.6 TB 一台库放得下（上限几十 TB），</text>
<text x="8" y="259" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">存储不是分片的理由；写 250 行/秒也不是</text>
</svg>
白板上新增：两张表，每一行带单位；下面写出三条决定：一个主库、不分片、不加缓存。

**常见失分。**
- **丢掉单位：** 数量级会错，而且自己发现不了。
- **年计数少一个数量级：** 5.2 亿说成 5,200 万，存储和写量都偏小 10 倍。
- **只算读不算平台调用：** 平台额度是最先碰到的上限。
- **算了不用：** 算出 250 行/秒却不说「所以不分片」。

**面试官可能接着问。**
- 为什么不取忙时窗口？ → 提现跨时区跨天，没有集中忙时；全天再乘 3 留给早晚高峰和营销，给真实分布我就换，结论不变。
- 3.6 TB 要分片吗？ → 不要；触发线是存储超 10 TB 或持续写超 10,000 行/秒，我们是 250 行/秒。
- 每人每周 10 笔呢？ → 全部 ×10：峰值约 500 笔/秒、2,500 行/秒（仍低于 10,000，一个主库够），但每年 2.6 TB、7 年 18 TB 过了 10 TB 线，所以热库只留最近 1 年（含索引约 5.2 TB），更老的按月分区转冷存储。
