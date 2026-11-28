---
id: bagu-java-money-bigdecimal-1-no-double-money
node: b.runtime.java-money-bigdecimal
type: qa
step: 1
---
## Q
**金额计算 · 为什么不用 double、BigDecimal 与 long**｜追问

面试官：「金额为什么不能用 double？BigDecimal 要注意什么？数据库里金额怎么存？」

## A
**基本回答。** double 是二进制浮点，0.1 是无限循环小数，只能存近似值：`0.1 + 0.2` 得 `0.30000000000000004`，累加 10 次 0.1 得 `0.9999999999999999`，分润会差一分钱，日终对账不平。金额用 BigDecimal，或用 long 存最小货币单位（分，数据库 BIGINT；或 DECIMAL(p, s)，不用 FLOAT/DOUBLE）；接口用字符串或整数传，避免前端浮点丢精度。long 的难点是币种小数位不同（日元 0 位，美元 2 位）。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 212">
<text x="10" y="14" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">double（二进制浮点）</text>
<rect x="8" y="24" width="60" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="38.0" y="41.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0.1</text>
<text x="80" y="42" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">+</text>
<rect x="92" y="24" width="60" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="122.0" y="41.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0.2</text>
<line x1="152" y1="37" x2="170" y2="37" stroke-width="1.2" stroke="currentColor"/>
<polygon points="170.0,37.0 163.6,39.9 163.6,34.1" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="170" y="24" width="162" height="26" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="251.0" y="41.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0.30000000000000004</text>
<text x="10" y="76" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">long 存最小单位（分）</text>
<rect x="8" y="86" width="60" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="38.0" y="103.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">10 分</text>
<text x="80" y="104" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">+</text>
<rect x="92" y="86" width="60" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="122.0" y="103.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">20 分</text>
<line x1="152" y1="99" x2="170" y2="99" stroke-width="1.2" stroke="currentColor"/>
<polygon points="170.0,99.0 163.6,101.9 163.6,96.1" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="170" y="86" width="162" height="26" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="251.0" y="103.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">30 分，精确</text>
<text x="10" y="138" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">100 分三等分：余数归最后一方</text>
<rect x="8" y="148" width="96" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="56.0" y="165.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">33 分</text>
<rect x="122" y="148" width="96" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170.0" y="165.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">33 分</text>
<rect x="236" y="148" width="96" height="26" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="284.0" y="165.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">34 分</text>
<text x="10" y="200" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">BigDecimal 用字符串构造，比较用 compareTo</text>
</svg>
double 的 0.1 和 0.2 本身是近似值，相加多出一截尾巴；用分存整数加法精确；除不尽时把余数明确分给某一方。
**举个例子。** BigDecimal 的坑：
- `new BigDecimal(0.1)` 是 0.1000000000000000055…，要用 `new BigDecimal("0.1")` 或 `BigDecimal.valueOf(0.1)`。
- `new BigDecimal("2.0").equals(new BigDecimal("2.00"))` 为 false（scale 不同，hashCode 也不同），`compareTo` 返回 0。
- `divide(x, 2, RoundingMode.HALF_UP)` 必须指定精度，除不尽否则抛 `ArithmeticException`；2.345 保留 2 位，HALF_UP 得 2.35，银行家舍入 HALF_EVEN 得 2.34。
- 100 分分给 3 方，每人 33 分余 1 分；规定余数归最后一方，即 33、33、34，加起来仍是 100。
**容易错。**
- **按比例拆分后各取整：** 每份四舍五入后加起来可能多一分或少一分，要规定余数归谁。
- **用 equals 比金额大小：** 比较用 `compareTo`。
