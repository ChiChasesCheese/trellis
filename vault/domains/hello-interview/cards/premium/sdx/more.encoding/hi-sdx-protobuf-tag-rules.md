---
id: hi-sdx-protobuf-tag-rules
node: more.encoding
type: qa
step: 2
---
## Q
**Protobuf：字段编号才是身份**｜补充 · 编码与模式演进（Encoding & Evolution） · 必会

面试官：「Protobuf 在线路上靠什么识别一个字段？由此推出的演进规则是什么？删掉一个字段后，它的编号为什么不能给新字段用？」

## A
**结论。** 线路上只有字段编号（tag）、线路类型和值，没有字段名。所以改名没事、改编号会让数据错位，删掉的编号必须保留（`reserved`）、永不复用。

**要点。**
- **改名免费：** 名字只存在于代码里，编码里没有。
- **改编号等于换字段：** 旧数据里的编号 2 会被解码成新定义里的编号 2。
- **复用编号是静默损坏：** 旧记录里编号 2 原本是 `age`，你把它删了又把编号 2 给了 `score`，旧数据里的 30 会被读成 `score = 30`，不报错。
- **新增字段：** 用新编号，并且有默认值，旧数据没有它也能解析（向后兼容）。
- **旧代码遇到新字段：** 按线路类型知道要跳过几个字节，直接跳过（向前兼容）。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 250">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">旧记录的线路内容（编号 : 值）</text>
<rect x="8" y="24" width="150" height="30" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="83.0" y="43.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1 : "Ann"</text>
<rect x="170" y="24" width="150" height="30" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="245.0" y="43.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2 : 30</text>
<rect x="8" y="84" width="150" height="50" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="83.0" y="105.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">旧定义</text>
<text x="83.0" y="120.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">1 name  2 age</text>
<rect x="170" y="84" width="160" height="50" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="250.0" y="105.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">错误的新定义</text>
<text x="250.0" y="120.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">1 name  2 score</text>
<polyline points="238,54 238.0,77.0" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="238,84 234.8,77.0 241.2,77.0" style="fill:var(--accent,#3b6fd4)"/>
<polyline points="83,54 83.0,77.0" fill="none" stroke-width="1.3" stroke="currentColor"/>
<polygon points="83,84 79.8,77.0 86.2,77.0" fill="currentColor"/>
<text x="8" y="164" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">旧数据里的 30 被读成 score = 30</text>
<text x="8" y="182" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">类型相同时不报错，数据悄悄错位</text>
<text x="8" y="208" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">正确：删掉 age 后写 reserved 2</text>
<text x="8" y="226" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">新字段用新编号 3，编号永不复用</text>
</svg>

**面试里这样说。** 「Protobuf 靠字段编号识别字段，改名安全，改编号会错位。删字段要把编号和名字都 `reserved`，因为复用编号会让旧数据被悄悄读成新字段，而且不报错。新增字段用新编号并给默认值。」

**易错。**
- **把 `int32 age` 改成 `string age` 但沿用编号：** 线路类型变了，旧数据解析出错或被当作未知字段丢弃。
- **删字段只删定义不保留编号：** 过几个版本有人复用，生产数据被悄悄读错。
