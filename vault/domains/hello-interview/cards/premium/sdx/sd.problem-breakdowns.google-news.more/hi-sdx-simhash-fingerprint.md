---
id: hi-sdx-simhash-fingerprint
node: sd.problem-breakdowns.google-news.more
type: qa
step: 1
---
## Q
**SimHash：让相似文章的指纹只差几位**｜补充 · 新闻聚合（Google News） · 必会

面试官：「同一条新闻有几十家媒体转载改写，只改了几个词。用 MD5 比较，为什么认不出它们是同一篇？有什么哈希能让相似的文章得到相似的指纹？」

## A
**结论。** 普通哈希故意让输入差一点、输出就面目全非。SimHash 反过来：文章里每个词先哈希，再按位「投票」，按票数的正负定出 64 位指纹。两篇文章共有的词投一样的票，所以指纹只差几位，用汉明距离（不同位的个数）就能判断近似重复。

**要点。**
- **普通哈希的问题：** 改一个字，MD5 大约一半的位都会变，只能认出一字不差的重复。
- **投票：** 每个词哈希成 64 位，开 64 个计数器。词的某一位是 1，对应计数器加 1；是 0 就减 1。实际会按词频等给每个词一个权重，图里权重都取 1。
- **定指纹：** 计数器大于 0，指纹这一位取 1，否则取 0。
- **为什么相似：** 换掉几个词，只改变这几个词的票，大多数计数器的正负不变，只有合计接近 0 的位会翻转。
- **判断：** 64 位指纹的汉明距离不超过 3，常被当作近似重复。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 260">
<text x="8" y="18" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">词</text>
<text x="40" y="18" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">哈希</text>
<text x="123.0" y="18" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">位1</text>
<text x="161.0" y="18" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">位2</text>
<text x="199.0" y="18" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">位3</text>
<text x="237.0" y="18" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">位4</text>
<text x="275.0" y="18" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">位5</text>
<text x="313.0" y="18" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">位6</text>
<text x="8" y="40" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">w1</text>
<text x="40" y="40" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">000111</text>
<text x="123.0" y="40" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">-1</text>
<text x="161.0" y="40" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">-1</text>
<text x="199.0" y="40" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">-1</text>
<text x="237.0" y="40" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">+1</text>
<text x="275.0" y="40" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">+1</text>
<text x="313.0" y="40" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">+1</text>
<text x="8" y="62" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">w2</text>
<text x="40" y="62" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">010111</text>
<text x="123.0" y="62" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">-1</text>
<text x="161.0" y="62" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">+1</text>
<text x="199.0" y="62" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">-1</text>
<text x="237.0" y="62" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">+1</text>
<text x="275.0" y="62" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">+1</text>
<text x="313.0" y="62" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">+1</text>
<text x="8" y="84" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">w3</text>
<text x="40" y="84" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">101100</text>
<text x="123.0" y="84" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">+1</text>
<text x="161.0" y="84" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">-1</text>
<text x="199.0" y="84" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">+1</text>
<text x="237.0" y="84" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">+1</text>
<text x="275.0" y="84" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">-1</text>
<text x="313.0" y="84" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">-1</text>
<text x="8" y="106" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">w4</text>
<text x="40" y="106" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">000110</text>
<text x="123.0" y="106" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">-1</text>
<text x="161.0" y="106" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">-1</text>
<text x="199.0" y="106" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">-1</text>
<text x="237.0" y="106" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">+1</text>
<text x="275.0" y="106" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">+1</text>
<text x="313.0" y="106" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">-1</text>
<text x="8" y="128" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">w5</text>
<text x="40" y="128" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">010011</text>
<text x="123.0" y="128" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">-1</text>
<text x="161.0" y="128" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">+1</text>
<text x="199.0" y="128" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">-1</text>
<text x="237.0" y="128" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">-1</text>
<text x="275.0" y="128" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">+1</text>
<text x="313.0" y="128" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">+1</text>
<polyline points="8,136 332,136" fill="none" stroke-width="1" stroke="currentColor"/>
<text x="8" y="154" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">合计</text>
<text x="123.0" y="154" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">-3</text>
<text x="161.0" y="154" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">-1</text>
<text x="199.0" y="154" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">-3</text>
<text x="237.0" y="154" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">+3</text>
<text x="275.0" y="154" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">+3</text>
<text x="313.0" y="154" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">+1</text>
<rect x="102" y="163" width="232" height="24" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="8" y="180" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">指纹</text>
<text x="123.0" y="180" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<text x="161.0" y="180" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<text x="199.0" y="180" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<text x="237.0" y="180" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<text x="275.0" y="180" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<text x="313.0" y="180" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<text x="8" y="210" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">换掉 w5：合计 -1 -1 -3 +5 +1 -1</text>
<text x="8" y="230" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">指纹 000110，只差第 6 位</text>
<text x="8" y="250" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">无关文章 110001，差 4 位</text>
</svg>

**为什么。** 每一位都是对全文所有词的一次多数表决。一个词只占票数的一小部分，小改动很难翻转多数，大改动才会翻转很多位，所以距离近似反映内容的差异。

**面试里这样说。** 「我给每篇文章算一个 64 位 SimHash：每个词哈希后按位加减投票，合计为正的位取 1。相似文章只差几位，汉明距离不超过 3 就算近似重复，比只能认出一字不差的 MD5 合适。」

**易错。**
- **用 MD5 或 SHA 当近似去重指纹：** 改一个词指纹全变，相似文章认不出来。
- **把汉明距离当相似度百分比：** 它只是不同位的个数，阈值要用真实数据校准，3 只是常见起点。
- **对很短的文本用 SimHash：** 词太少，每个词占的票数大，改一个词就可能翻转好几位。
