---
id: hi-sdx-uid-uuidv7
node: more.unique-id-generator
type: qa
step: 4
---
## Q
**UUIDv7 只用随机位，会撞吗**｜补充 · 发号器（Unique ID Generator） · 追问

面试官：「如果直接用 UUIDv7，全平台峰值每毫秒生成 200 个，且只用随机位、不放计数器，会撞吗？它和 64 位雪花比怎么选？」

## A
**结论。** 实际不会撞。UUIDv7 有 74 个随机位，同一毫秒内 200 个撞车的概率约 10^-18，即使每一毫秒都在峰值，一天也只有约 10^-10。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 125">
<g font-size="11" font-family="sans-serif" text-anchor="middle" stroke-width="1.2">
<g stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))">
<rect x="5" y="30" width="100" height="30" rx="3"/>
<rect x="105" y="30" width="34" height="30" rx="3"/>
<rect x="139" y="30" width="62" height="30" rx="3"/>
<rect x="201" y="30" width="34" height="30" rx="3"/>
<rect x="235" y="30" width="100" height="30" rx="3"/>
</g>
<g fill="none" stroke="currentColor">
<polyline points="141,66 141,74 199,74 199,66"/>
<polyline points="237,66 237,74 333,74 333,66"/>
<line x1="170" y1="74" x2="170" y2="82"/>
<line x1="285" y1="74" x2="285" y2="82"/>
<line x1="170" y1="82" x2="285" y2="82"/>
</g>
<g fill="currentColor">
<text x="170" y="18">UUIDv7 共 128 位</text>
<text x="55" y="49">时间戳 48</text>
<text x="122" y="49" font-size="10">ver 4</text>
<text x="170" y="49">rand_a 12</text>
<text x="218" y="49" font-size="10">var 2</text>
<text x="285" y="49">rand_b 62</text>
</g>
<g style="fill:var(--dim,#6b7280)">
<text x="228" y="98">随机 74 位 = 12 + 62</text>
</g>
<g style="fill:var(--accent,#3b6fd4)">
<text x="170" y="118">同一毫秒 200 个：撞车约 10^-18</text>
</g>
</g>
</svg>

**要点。**
- **结构：** 48 位毫秒时间戳 + 4 位版本 + 2 位变体 + 74 位随机（rand_a 12 位 + rand_b 62 位），共 128 位。
- **生日近似：** 同一毫秒内 n 个 ID 的撞车概率约 n(n−1)/2 ÷ 2^74。n = 200 时是 19900 ÷ 1.9×10^22 ≈ 10^-18。
- **跨毫秒不会撞：** 不同毫秒的时间戳不同。一天有 8640 万个毫秒，全按峰值算上限约 9×10^-11。
- **计数器方式的作用：** 保证同一毫秒内严格递增，不是为了防撞。
- **对比雪花：** UUIDv7 不需要机器号和租约，没有协调；代价是 128 位，主键和所有二级索引都比 64 位大一倍，同一毫秒内的顺序不保证。

**面试里这样说。** 「UUIDv7 有 74 位随机，峰值每毫秒 200 个，撞车概率约 10^-18，足够。我选它是为了省掉机器号租约；如果要 64 位主键，或者索引空间很紧，才用雪花。随机数必须来自密码学安全的生成器。」

**易错。**
- **说 UUID 不保证唯一：** 概率上可以忽略，关键是随机源要好。
- **把 UUID 存成 36 字节字符串：** 应存 16 字节二进制。
