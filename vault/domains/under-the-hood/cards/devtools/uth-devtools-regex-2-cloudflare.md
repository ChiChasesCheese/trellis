---
id: uth-devtools-regex-2-cloudflare
node: devtools.regex
type: qa
step: 2
---
## Q
**一条正则怎么打挂 Cloudflare**｜Cloudflare · 2019-07-02

一条 WAF 规则里的正则，为什么能让全球边缘服务器的 CPU 接近 100%？

## A
**背景。** 回溯引擎遇到走不通的路才会退，而几处“可以退”的地方会互相组合。正则里套两个 `.*`（`.` 是任意字符，`*` 是任意多个）：第一个 `.*` 先尽量多吃，失败就一格一格退；每退一格，第二个 `.*` 又要从头“吃光再退”。

**结构。** 关键片段 `.*(?:.*=.*)`：在没有 `=` 的长串上，两个 `.*` 要试遍所有切分点，n 个字符就是约 n²/2 种组合，而且每个起点都要重来一遍。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 214">
<text x="162" y="16" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">第一个 .* 停在哪</text>
<text x="8" y="52" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">第二个 .*</text>
<text x="8" y="68" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">停在哪</text>
<circle cx="78" cy="40" r="5" stroke="currentColor" stroke-width="1.8" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<circle cx="78" cy="60" r="5" stroke="currentColor" stroke-width="1.8" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<circle cx="78" cy="80" r="5" stroke="currentColor" stroke-width="1.8" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<circle cx="78" cy="100" r="5" stroke="currentColor" stroke-width="1.8" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<circle cx="78" cy="120" r="5" stroke="currentColor" stroke-width="1.8" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<circle cx="78" cy="140" r="5" stroke="currentColor" stroke-width="1.8" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<circle cx="78" cy="160" r="5" stroke="currentColor" stroke-width="1.8" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<circle cx="106" cy="60" r="5" stroke="currentColor" stroke-width="1.8" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<circle cx="106" cy="80" r="5" stroke="currentColor" stroke-width="1.8" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<circle cx="106" cy="100" r="5" stroke="currentColor" stroke-width="1.8" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<circle cx="106" cy="120" r="5" stroke="currentColor" stroke-width="1.8" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<circle cx="106" cy="140" r="5" stroke="currentColor" stroke-width="1.8" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<circle cx="106" cy="160" r="5" stroke="currentColor" stroke-width="1.8" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<circle cx="134" cy="80" r="5" stroke="currentColor" stroke-width="1.8" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<circle cx="134" cy="100" r="5" stroke="currentColor" stroke-width="1.8" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<circle cx="134" cy="120" r="5" stroke="currentColor" stroke-width="1.8" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<circle cx="134" cy="140" r="5" stroke="currentColor" stroke-width="1.8" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<circle cx="134" cy="160" r="5" stroke="currentColor" stroke-width="1.8" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<circle cx="162" cy="100" r="5" stroke="currentColor" stroke-width="1.8" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<circle cx="162" cy="120" r="5" stroke="currentColor" stroke-width="1.8" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<circle cx="162" cy="140" r="5" stroke="currentColor" stroke-width="1.8" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<circle cx="162" cy="160" r="5" stroke="currentColor" stroke-width="1.8" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<circle cx="190" cy="120" r="5" stroke="currentColor" stroke-width="1.8" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<circle cx="190" cy="140" r="5" stroke="currentColor" stroke-width="1.8" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<circle cx="190" cy="160" r="5" stroke="currentColor" stroke-width="1.8" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<circle cx="218" cy="140" r="5" stroke="currentColor" stroke-width="1.8" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<circle cx="218" cy="160" r="5" stroke="currentColor" stroke-width="1.8" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<circle cx="246" cy="160" r="5" stroke="currentColor" stroke-width="1.8" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170" y="198" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">每一对都要失败一次 n 个字符约 n^2/2 次</text>
</svg>
```

**细节。**

- 2019 年 7 月 2 日新规则上线，处理 HTTP/HTTPS 的 CPU 近 100%，用户看到 502
- 正则引擎在每个起点上都把这些组合试一遍，才宣布“没有匹配”
- Python 3.11 起有占有量词（`*+`）和原子组（`(?>…)`）：一旦匹配成功就不再回退

**坑。** 正则只要会处理用户输入，就用 RE2 类引擎，或加占有量词、原子组、超时，别让 `.*` 套 `.*`。

**对应 LeetCode：** 无直接对应的题
