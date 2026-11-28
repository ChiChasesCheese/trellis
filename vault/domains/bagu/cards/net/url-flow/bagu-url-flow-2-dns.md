---
id: bagu-url-flow-2-dns
node: a.net.url-flow
type: qa
step: 2
---
## Q
**DNS 解析 · 缓存分几层、怎么一步步查**｜必会

面试官：「第二步 DNS 解析具体怎么走？结果缓存在哪几层？」

## A
**基本回答。** 依次查：浏览器缓存 → 操作系统缓存与 `/etc/hosts` → 本地递归解析器（运营商或 8.8.8.8）。解析器没缓存才迭代：根只告诉你 `.com` 的 TLD 服务器在哪，TLD 只告诉你 `example.com` 的权威服务器在哪，权威（域名所有者配置）返回 A / AAAA 记录。客户端对解析器是递归（要最终答案），解析器对各级是迭代（每级只给下一步线索），解析器缓存结果给所有用户共用，所以大多数查询在前几层就结束，根几乎不被直接访问。各层按 TTL（权威随记录返回的秒数）缓存：TTL 越长越省，改地址生效越慢。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 256">
<text x="4" y="13" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">先查：浏览器缓存 → 系统缓存/hosts → 解析器缓存</text>
<text x="4" y="29" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">都没命中，解析器才出门问（迭代）</text>
<rect x="4" y="34" width="72" height="22" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="40" y="49" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">本地解析器</text>
<line x1="40" y1="56" x2="40" y2="230" stroke-width="1.2" style="stroke:var(--dim,#6b7280)" stroke-dasharray="4 3"/>
<rect x="91" y="34" width="72" height="22" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="127" y="49" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">根服务器</text>
<line x1="127" y1="56" x2="127" y2="230" stroke-width="1.2" style="stroke:var(--dim,#6b7280)" stroke-dasharray="4 3"/>
<rect x="178" y="34" width="72" height="22" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="214" y="49" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">TLD</text>
<line x1="214" y1="56" x2="214" y2="230" stroke-width="1.2" style="stroke:var(--dim,#6b7280)" stroke-dasharray="4 3"/>
<rect x="264" y="34" width="72" height="22" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="300" y="49" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">权威服务器</text>
<line x1="300" y1="56" x2="300" y2="230" stroke-width="1.2" style="stroke:var(--dim,#6b7280)" stroke-dasharray="4 3"/>
<line x1="44" y1="76" x2="123" y2="76" stroke-width="1.2" stroke="currentColor"/>
<polygon points="123.0,76.0 116.0,79.2 116.0,72.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="83.5" y="71" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">a.com？</text>
<line x1="123" y1="104" x2="44" y2="104" stroke-width="1.2" style="stroke:var(--dim,#6b7280)" stroke-dasharray="4 3"/>
<polygon points="44.0,104.0 51.0,100.8 51.0,107.2" style="fill:var(--dim,#6b7280);stroke:var(--dim,#6b7280)" stroke-width="0.5"/>
<text x="83.5" y="99" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">去问 TLD</text>
<line x1="44" y1="132" x2="210" y2="132" stroke-width="1.2" stroke="currentColor"/>
<polygon points="210.0,132.0 203.0,135.2 203.0,128.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="127" y="127" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">a.com？</text>
<line x1="210" y1="160" x2="44" y2="160" stroke-width="1.2" style="stroke:var(--dim,#6b7280)" stroke-dasharray="4 3"/>
<polygon points="44.0,160.0 51.0,156.8 51.0,163.2" style="fill:var(--dim,#6b7280);stroke:var(--dim,#6b7280)" stroke-width="0.5"/>
<text x="127" y="155" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">去问权威</text>
<line x1="44" y1="188" x2="296" y2="188" stroke-width="1.2" stroke="currentColor"/>
<polygon points="296.0,188.0 289.0,191.2 289.0,184.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="170" y="183" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">a.com？</text>
<line x1="296" y1="216" x2="44" y2="216" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="44.0,216.0 51.0,212.8 51.0,219.2" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="170" y="211" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">A：1.2.3.4</text>
<text x="4" y="253" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">每一级都按 TTL 缓存，下次不用再问</text>
</svg>
顶部是客户端先查的缓存，下面是解析器没缓存时的三轮迭代。
**细节。** 默认 UDP 53，响应太大转 TCP；加密有 DoT（853）和 DoH。CDN：域名 CNAME 到厂商域名，权威 DNS 按解析器位置（或 EDNS 客户端子网）返回最近节点 IP。Java 的 `InetAddress` 默认缓存 30 秒（装安全管理器则永久），做故障切换要设 `networkaddress.cache.ttl`，否则服务还连旧 IP。
**业务场景。** 某接口域名切到新机房，TTL 600 秒，权威改成新地址后，缓存里旧记录还有最多 10 分钟，期间部分用户仍去旧机房；所以切换前要提前调低 TTL。
**容易错。**
- **以为每次访问都问根服务器。**
- **分不清递归和迭代：** 不是根替你去问下一级。
- **改了记录就以为立刻全部生效：** 应用进程里也有缓存。
