---
id: bagu-dns-1-resolve-ttl
node: b.net.dns
type: qa
step: 1
---
## Q
**DNS · 解析过程、缓存与切换**｜必会

面试官：「DNS 解析的完整过程是什么，递归和迭代有什么区别？域名切换 IP 后为什么部分用户还访问旧地址，怎么灰度？」

## A
**基本回答。** 先查浏览器缓存，再查操作系统缓存和 `/etc/hosts`，再问本地递归解析器；它没缓存才迭代去问：根服务器指向 `.com` 的 TLD 服务器，TLD 指向权威服务器，权威返回 A（IPv4）或 AAAA（IPv6）记录。客户端把问题整个委托给解析器是递归，解析器逐级问、每级只说下一步问谁是迭代。各层按 TTL 缓存。
**2026 亮点。** DNS 自动化本身可能是单点：区域端点记录被自动化写成空记录时，整个区域的依赖同时解析失败，客户端缓存还会拉长故障；关键依赖要有跨区域备用端点，或保留上一次良好解析（过期仍可用，serve-stale）。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 244">
<text x="8" y="14" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">递归：客户端把问题整个委托</text>
<rect x="8" y="100" width="70" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="43.0" y="116.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">浏览器</text>
<text x="43.0" y="131.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">系统缓存</text>
<line x1="78" y1="120" x2="116" y2="120" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="116.0,120.0 109.6,122.9 109.6,117.1" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="97" y="112" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">递归</text>
<rect x="116" y="100" width="76" height="40" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="154.0" y="116.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">本地</text>
<text x="154.0" y="131.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">递归解析器</text>
<rect x="236" y="26" width="96" height="34" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="284.0" y="39.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1 根服务器</text>
<text x="284.0" y="54.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">指向 .com TLD</text>
<line x1="192" y1="120" x2="236" y2="43" stroke-width="1.2" stroke="currentColor"/>
<polygon points="236.0,43.0 235.3,50.0 230.4,47.1" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="236" y="100" width="96" height="34" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="284.0" y="113.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2 TLD（.com）</text>
<text x="284.0" y="128.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">指向权威服务器</text>
<line x1="192" y1="120" x2="236" y2="117" stroke-width="1.2" stroke="currentColor"/>
<polygon points="236.0,117.0 229.8,120.3 229.4,114.6" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="236" y="174" width="96" height="34" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="284.0" y="187.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3 权威服务器</text>
<text x="284.0" y="202.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">返回 A / AAAA</text>
<line x1="192" y1="120" x2="236" y2="191" stroke-width="1.2" stroke="currentColor"/>
<polygon points="236.0,191.0 230.2,187.1 235.1,184.1" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="8" y="226" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">迭代：每一级只说下一步该问谁</text>
<text x="8" y="244" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">各层按 TTL 缓存：浏览器、系统、解析器</text>
</svg>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 104">
<rect x="6" y="10" width="76" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="44.0" y="26.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1 提前</text>
<text x="44.0" y="41.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">调低 TTL</text>
<rect x="88" y="10" width="76" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="126.0" y="26.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2 等旧</text>
<text x="126.0" y="41.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">TTL 过完</text>
<rect x="170" y="10" width="76" height="40" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="208.0" y="26.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3 切换</text>
<text x="208.0" y="41.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">新 IP</text>
<rect x="252" y="10" width="76" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="290.0" y="26.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">4 保留</text>
<text x="290.0" y="41.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">旧 IP 一阵</text>
<text x="8" y="72" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">缓存没过期的用户，仍会访问旧 IP</text>
<text x="8" y="92" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">所以旧 IP 要继续保留一段时间</text>
</svg>
切换 IP 的稳妥顺序：提前调低 TTL，等旧 TTL 过完再切，旧 IP 保留一段时间，接住缓存更长的用户。
**细节。** 记录类型：A / AAAA、CNAME、NS、MX、TXT。默认 UDP 53，响应太大或区域传送用 TCP；加密的有 DoT（TLS 853）和 DoH。CDN 接入是域名 CNAME 到厂商域名，权威 DNS 按解析器位置（或 EDNS 客户端子网）返回最近节点。Java 的 `InetAddress` 自带缓存，默认 30 秒，装了安全管理器则永久，故障切换要设 `networkaddress.cache.ttl`。Kubernetes Pod 里 `ndots:5` 会让外部域名多发无效查询，延迟敏感时写全域名（末尾加点）。
**业务场景。** TTL 3600 秒的域名切新机房：用户 10:00 查过，缓存到 11:00，10:30 改记录后他仍访问旧 IP；各用户到期时间不同，切换被拉得很长。正确做法是先把 TTL 调成 60，等原 3600 秒过完再改，之后最多约 60 秒全部用户解析到新地址。
**容易错。**
- **以为 DNS 一改全网立刻生效：** 各层缓存按 TTL 保存。
- **切换当天才降 TTL：** 降 TTL 也要等旧 TTL 过完才生效。
- **把递归和迭代说反：** 客户端到解析器递归，解析器到各级迭代。
