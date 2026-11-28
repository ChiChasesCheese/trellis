---
id: bagu-network-slow-1-layered
node: b.linux.network-slow
type: qa
step: 1
---
## Q
**网络慢或连不上 · 分层排查**｜必会

面试官：「用户反馈某地区视频加载慢，服务访问慢或连不上，网络上怎么排查？ping 通了但 TCP 连不上，可能是什么原因？」

## A
**基本回答。** 自下而上分层测量：DNS、连通性、端口连接、监听队列、分阶段计时、抓包。ping 通只说明 ICMP 有回应，端口、防火墙或服务都可能不通。
`curl -w` 哪段大就是哪层：dns 大看解析，connect 大看网络或 SYN 被丢，tls 大看证书握手，ttfb 大看服务端处理。`ss -ant` 大量 SYN-SENT 是连不上对端；`ss -lnt` 的 Recv-Q 接近 Send-Q 是全连接队列将满，`netstat -s | grep -i -E 'listen|overflow'` 看溢出。丢包看 `netstat -s | grep -i retrans`、`ip -s link`，抓包看重传、RST、零窗口。`dmesg` 出现 `nf_conntrack: table full, dropping packet`：新连接偶发超时、已建立的正常、ping 也通，调大 `nf_conntrack_max`。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 190">
<rect x="18" y="10" width="76" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="56" y="28" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">① DNS</text>
<rect x="94" y="10" width="76" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="132" y="28" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">② 建连</text>
<rect x="170" y="10" width="76" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="208" y="28" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">③ TLS</text>
<rect x="246" y="10" width="76" height="28" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="284" y="28" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">④ 首字节</text>
<text x="10" y="62" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">① time_namelookup 大：解析慢，用 dig 查</text>
<text x="10" y="80" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">② time_connect 大：网络差，或 SYN 被丢</text>
<text x="10" y="98" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">③ time_appconnect 大：证书与 TLS 握手</text>
<text x="10" y="116" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">④ time_starttransfer 大：服务端处理慢</text>
<text x="10" y="146" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">这些值都是从开头累计的时间</text>
<text x="10" y="164" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">看相邻两段的差值，差最大的那一段就是慢的层</text>
</svg>
先用 `curl -w` 把一次请求切成四段，哪段最长就往哪一层查。
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 280">
<rect x="6" y="6" width="104" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="58" y="24" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">① DNS</text>
<line x1="110" y1="20" x2="115.0" y2="20.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="122,20 115.0,23.2 115.0,16.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="128" y="24" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">dig +short example.com</text>
<line x1="58" y1="34" x2="58.0" y2="37.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="58,44 54.8,37.0 61.2,37.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="6" y="44" width="104" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="58" y="62" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">② 连通性</text>
<line x1="110" y1="58" x2="115.0" y2="58.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="122,58 115.0,61.2 115.0,54.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="128" y="62" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">mtr host：哪一跳丢包</text>
<line x1="58" y1="72" x2="58.0" y2="75.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="58,82 54.8,75.0 61.2,75.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="6" y="82" width="104" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="58" y="100" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">③ 端口</text>
<line x1="110" y1="96" x2="115.0" y2="96.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="122,96 115.0,99.2 115.0,92.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="128" y="100" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">nc -vz host 443</text>
<line x1="58" y1="110" x2="58.0" y2="113.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="58,120 54.8,113.0 61.2,113.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="6" y="120" width="104" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="58" y="138" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">④ 队列与状态</text>
<line x1="110" y1="134" x2="115.0" y2="134.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="122,134 115.0,137.2 115.0,130.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="128" y="138" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">ss -s；ss -lnt；ss -ti</text>
<line x1="58" y1="148" x2="58.0" y2="151.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="58,158 54.8,151.0 61.2,151.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="6" y="158" width="104" height="28" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="58" y="176" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">⑤ 分段计时</text>
<line x1="110" y1="172" x2="115.0" y2="172.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="122,172 115.0,175.2 115.0,168.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="128" y="176" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">curl -w：哪一段大</text>
<line x1="58" y1="186" x2="58.0" y2="189.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="58,196 54.8,189.0 61.2,189.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="6" y="196" width="104" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="58" y="214" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">⑥ 抓包</text>
<line x1="110" y1="210" x2="115.0" y2="210.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="122,210 115.0,213.2 115.0,206.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="128" y="214" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">tcpdump / Wireshark</text>
<line x1="58" y1="224" x2="58.0" y2="227.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="58,234 54.8,227.0 61.2,227.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="6" y="234" width="104" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="58" y="252" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">⑦ 应用层</text>
<line x1="110" y1="248" x2="115.0" y2="248.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="122,248 115.0,251.2 115.0,244.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="128" y="252" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">连接池、线程池、下游、超时</text>
</svg>
没有头绪时按这个顺序逐层往下测，每一步都有对应的命令；蓝色那一步最快定位到出问题的层。
**举个例子。** 某地区用户反馈视频加载慢：
1. **解析：** 在该地区用 `dig +short` 查域名，再对比 `dig @8.8.8.8`，发现解析到的是一个较远的节点。
2. **分段计时：** `curl -w` 的 dns 很小，connect 偏大：解析没问题，往远节点建连的往返时间太长。
3. **逐跳：** `mtr` 看哪一跳延迟或丢包高，确认路径本身偏长。
4. **结论：** 问题出在调度到较远的节点，把该地区的解析调度到更近的节点后恢复。
再看 ping 通连不上：
5. **测端口：** `nc -vz host 443` 如果立刻被拒绝，说明服务没监听或只绑了 127.0.0.1。
6. **如果是超时：** 多半是防火墙或安全组丢了这个端口，或队列、conntrack 满了丢包；`ss -lnt` 与 `dmesg | grep conntrack` 继续区分。
**代码。** 逐层排查的命令：
```bash
dig +short example.com                 # DNS，可对比 dig @8.8.8.8
mtr host                               # 哪一跳丢包或延迟高
nc -vz host 443                        # 端口通不通
ss -s; ss -lnt; ss -ti                 # 状态汇总、监听队列、重传 RTT cwnd
curl -o /dev/null -s -w 'dns=%{time_namelookup} connect=%{time_connect} tls=%{time_appconnect} ttfb=%{time_starttransfer} total=%{time_total}\n' https://example.com/
tcpdump -i eth0 host <ip> and port 443 -w out.pcap
```
**容易错。**
- **ping 通就认为服务没问题：** ping 只证明三层可达，端口、防火墙、服务都可能不通。
- **一上来就抓包：** 抓包信息量太大，先用 `curl -w` 分段计时定位到层，再有针对性地抓。
- **把 curl -w 的时间当成各段耗时：** 这些值是从请求开始累计的，要看相邻两段的差。
- **conntrack 满了当成网络断了：** 现象是新连接偶发失败，已建立的连接和 ping 都正常，要看 `dmesg`。
- **偶发 502 只怪网络：** 常见是上游 keep-alive 超时比网关短，网关复用了已被关闭的连接。
