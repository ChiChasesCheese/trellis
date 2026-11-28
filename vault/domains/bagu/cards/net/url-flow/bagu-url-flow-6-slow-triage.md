---
id: bagu-url-flow-6-slow-triage
node: a.net.url-flow
type: qa
step: 6
---
## Q
**网页慢 · 怎么逐段定位**｜必会

面试官：「用户反馈网页打开很慢，你怎么知道慢在哪一段？」

## A
**基本回答。** 按流程分段计时，用 `curl` 一次看清。这些值是累计的（从请求开始算起），相邻相减才是该段耗时：TCP = connect − namelookup，TLS = appconnect − connect，服务端处理 = starttransfer − appconnect，下载 = total − starttransfer。哪段大查哪段：DNS 大查解析器和 TTL；TCP 或 TLS 大查网络路径、就近接入、复用和会话恢复；服务端段大看调用链里的慢查询和下游；下载段大看响应体、压缩、CDN；渲染慢看浏览器 Network 瀑布图。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 246">
<text x="4" y="14" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">例：一次慢请求，横轴是时间</text>
<text x="4" y="43" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">DNS</text>
<rect x="64" y="26" width="15" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="83" y="43" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">30 ms</text>
<text x="4" y="73" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">TCP</text>
<rect x="79" y="56" width="25" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="108" y="73" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">50 ms</text>
<text x="4" y="103" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">TLS</text>
<rect x="104" y="86" width="60" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="134" y="103" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">120 ms</text>
<text x="4" y="133" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">服务端</text>
<rect x="164" y="116" width="125" height="24" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="226.5" y="133" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">250 ms</text>
<text x="4" y="163" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">下载</text>
<rect x="289" y="146" width="35" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="285" y="163" text-anchor="end" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">70 ms</text>
<text x="4" y="192" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">curl 打印的是累计值（毫秒）：</text>
<text x="4" y="210" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">dns 30 · tcp 80 · tls 200</text>
<text x="4" y="228" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">ttfb 450 · total 520</text>
<text x="170" y="228" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">相邻相减才是每段</text>
</svg>
条的长度是该段耗时，最长的高亮就是该查的地方。
**代码。**
```bash
curl -o /dev/null -s -w 'dns %{time_namelookup} tcp %{time_connect} tls %{time_appconnect} ttfb %{time_starttransfer} total %{time_total}\n' https://example.com
```
**业务场景。** 一次输出 dns 0.03、tcp 0.08、tls 0.20、ttfb 0.45、total 0.52：相减得 DNS 30、TCP 50、TLS 120、服务端 250、下载 70 毫秒，最长的是服务端段，去看调用链。另一例：只有某运营商用户慢，拨测显示该运营商 DNS 段 3 秒、其余正常，问题在它的解析器，换 HTTPDNS 或预解析绕开。
**容易错。**
- **把累计值当单段耗时：** tls 0.20 其实只花 120 ms。
- **以为 TTFB 高就是服务端：** 它含 DNS、TCP、TLS 前置时间。
- **只在自己机房测：** 要从用户侧的运营商和地区拨测，偶发慢要多次采样。
