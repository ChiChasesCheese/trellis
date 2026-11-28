---
id: hi-fix-scope-math-02-qps-from-totals
node: fix.scope-math
type: qa
step: 2
---
## Q
**GoFundMe · 总量除以时间**｜补强

面试官：「大概的读写量是多少？这个页面一秒钟有多少读？」

你会怎么回答？白板上画到哪一步？

## A
**你说。**
- **先写总量和时间：** 「1 亿次页面读取，集中在 20,000 秒里，大约 5.6 小时。」
- **除，并带上单位：** 「1 亿 ÷ 20,000 秒 = 每秒 5,000 次。」
- **用量级回算：** 「1e8 ÷ 2e4 = 0.5e4，是 5,000，不是 2 万。」先把两个数写成 ×10 的幂，指数相减，系数相除。
- **换一道算一遍：** 「限时捐款：10 亿美元 ÷ 每笔 10 美元 = 1 亿笔；3 天 = 3 × 24 × 3,600 = 259,200 秒；1 亿 ÷ 259,200 ≈ 每秒 386 笔。」
- **背一把尺子：** 「1 天 = 86,400 秒，约 1e5。每天 N 次，除以 1e5，就是每秒多少次。每天 1 亿次约每秒 1,157 次。」
- **说出你选的时间窗：** 「流量集中在 5.6 小时里，所以是 5,000，比按全天算的 1,157 高；我按高的设计。」
**白板。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 262">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">总量 ÷ 时间 = 每秒多少（带单位，再回算）</text>
<rect x="8" y="26" width="324" height="78" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="46.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">页面读取</text>
<text x="18" y="61.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">1 亿次 ÷ 20,000 秒</text>
<text x="18" y="76.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">= 5,000 次/秒</text>
<text x="18" y="91.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">回算：1e8 ÷ 2e4 = 0.5e4</text>
<rect x="8" y="114" width="324" height="94" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="142.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">限时捐款</text>
<text x="18" y="157.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">10 亿美元 ÷ 10 美元 = 1 亿笔</text>
<text x="18" y="172.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">3 天 = 3 × 24 × 3,600 = 259,200 秒</text>
<text x="18" y="187.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">1 亿 ÷ 259,200 ≈ 386 笔/秒</text>
<text x="8" y="232" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">常见的错：把 20,000 当成 2 万次/秒——</text>
<text x="8" y="250" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">总量除以时间，结果的单位是「次/秒」</text>
</svg>

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 230">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">要背的一把尺子（秒）</text>
<rect x="8" y="28" width="324" height="26" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="18" y="45" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">1 小时 = 3,600</text>
<rect x="8" y="60" width="324" height="26" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="18" y="77" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">1 天 = 86,400  ≈ 1e5</text>
<rect x="8" y="92" width="324" height="26" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="18" y="109" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">3 天 = 259,200</text>
<rect x="8" y="124" width="324" height="26" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="18" y="141" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">1 个月（30 天） = 2,592,000  ≈ 2.6e6</text>
<rect x="8" y="156" width="324" height="26" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="18" y="173" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">1 年 = 31,536,000  ≈ 3.2e7</text>
<text x="8" y="202" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">每天 1 亿次 ≈ 每秒 1,157 次（1e8 ÷ 86,400）</text>
<text x="8" y="220" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">粗算：每天 N 次 ≈ N ÷ 1e5 次/秒</text>
</svg>
白板上：两个算式，每个都带单位和回算；右边是秒数的尺子。
**为什么这样说。** （约 1 分钟。）面试官看你的数字能不能当场算对、说清假设。强的回答先写总量和时间窗，再除，再回算一遍；错了当场改。弱的回答是心算后直接报数，报出来的数和写下来的算式对不上，后面所有设计的理由都要被重新核对。
**面试官可能接着问。**
- 万一你说错了怎么办？ → 当场改：「我刚才说 2 万，算式是 5,000，以 5,000 为准，对设计的结论是一样的。」自己发现，比被面试官指出强得多。
- 为什么要用 1e8、2e4 这种写法？ → 零的个数最容易数错；写成幂，指数相减，零的个数就不用数了。
- 时间窗怎么选？ → 有数就用数；没有，就先说出你的假设，比如「集中在几小时里」。窗口越短，速率越高，我选更保守的那个。
**常见失分。**
- **把 20,000 当成 2 万次/秒：** 总量除以时间，结果的单位是次/秒，不是时间本身。
- **不写单位：** 单位对不上时，错误一眼就能看出来；不写，错了也看不出。
- **不回算：** 一次心算，错 4 倍很正常；回算只要 5 秒。
