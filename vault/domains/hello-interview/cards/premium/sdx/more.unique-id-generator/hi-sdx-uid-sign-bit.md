---
id: hi-sdx-uid-sign-bit
node: more.unique-id-generator
type: qa
step: 5
---
## Q
**41+13+10 布局：有符号整数只能用 34.8 年**｜补充 · 发号器（Unique ID Generator） · 加分

面试官：「你的布局是 41 位时间戳 + 13 位机器号 + 10 位序列号，正好 64 位，没留符号位。41 位毫秒本来能撑 69.7 年，为什么当作有符号 64 位整数时只能保证 34.8 年内非负？」

## A
**结论。** 因为最高位就是时间戳的最高位。毫秒数超过 2^40（约 34.8 年）后这一位变成 1，有符号 64 位整数会把它读成负数。

**要点。**
- **原版有符号位：** Twitter 的 1+41+10+12 布局第一位恒为 0，时间戳可以用满 41 位。
- **本布局没有：** 64 位全被占满，符号位其实是时间戳的第 41 位。
- **算一下：** 2^40 毫秒 ÷ (1000 × 86400 × 365.25) ≈ 34.8 年；2^41 毫秒才是 69.7 年。
- **后果：** Java 的 long、MySQL 的 BIGINT（有符号）会出现负 ID，按 ID 排序时新数据排到最前面。
- **解法：** 从机器号或序列号让出 1 位做符号位，时间戳保持 41 位；或者全链路按无符号处理（BIGINT UNSIGNED），但很脆弱，任何一个有符号的环节都会出错。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 176">
<text x="10" y="26" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">最高位（bit 63）= 符号位</text>
<rect x="10" y="34" width="205" height="40" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="112.5" y="58.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">41 位时间戳</text>
<rect x="215" y="34" width="65" height="40" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="247.5" y="50.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">13 位</text>
<text x="247.5" y="65.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">机器号</text>
<rect x="280" y="34" width="50" height="40" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="305.0" y="50.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">10 位</text>
<text x="305.0" y="65.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">序列号</text>
<text x="10" y="100" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">前 34.8 年（毫秒数 &lt; 2^40）：最高位 0</text>
<text x="10" y="118" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">之后最高位变 1，有符号 long 读成负数</text>
<text x="10" y="146" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">41 位本可用 69.7 年，</text>
<text x="10" y="164" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">但没留符号位，最高位就是时间戳的最高位</text>
</svg>

**面试里这样说。** 「这个布局没有符号位，最高位是时间戳的最高位，所以有符号整数只能用 2^40 毫秒，约 34.8 年。我会从机器号或序列号让出一位做符号位，或者把自定义纪元定在上线日，并监控距离 2^40 还有多久。」

**易错。**
- **以为 41 位就是 69.7 年随便用：** 要看这一位会不会落在符号位上。
- **只在小时间戳下测试：** 这类边界要用接近 2^40 的时间戳测。
