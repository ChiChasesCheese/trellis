---
id: hi-sdx-vc-nat-types
node: more.video-conferencing
type: qa
step: 5
---
## Q
**NAT 为什么有时能打洞、有时不能**｜补充 · 视频会议（Zoom） · 必会

两个用户各在一台家用路由器（NAT）后面，浏览器要直连通话。有的用户之间借助 STUN 打洞一次就通，有的组合怎么试都不通，只能走 TURN 中继。NAT 到底做了什么？为什么差别出在 NAT 的类型上？

## A
**结论。** NAT 让内网的很多设备共用一个公网 IP：设备往外发包时，路由器分配一个公网端口并记下映射，外来的包对得上映射才放进来。打洞就是双方同时向对方的公网地址发包，各自路由器都建好映射，对方的包就被当作「回复」放行。同一内网地址不管访问谁都用同一个公网端口的 NAT（锥形）可以打通；每换一个目的地就换一个端口的对称 NAT，STUN 告诉对方的端口对别人无效，打洞会失败。

**要点。**
- **NAT 做了什么：** 内网设备（如 192.168.1.5）出门时，路由器换成「公网 IP + 一个端口」并记表，回包按表转回去；没登记的外来包直接丢，所以外面连不进来。
- **STUN 的作用：** 设备问公网上的 STUN 服务器「你看到我是谁」，得到自己的公网 IP 和端口，再经信令告诉对方。
- **锥形 NAT：** STUN 得到的端口对别的对端同样有效。按过滤从宽到严分三档：完全锥形（谁都能发）、地址受限（只收你发过包的 IP）、端口受限（只收你发过包的 IP 加端口）。
- **对称 NAT：** 每个不同的目的地（IP 加端口）分配一个新的公网端口，STUN 看到的端口只对 STUN 服务器有效，对端照它发包会被丢弃。
- **哪些组合不通：** 对称对对称、对称对端口受限打不通，只能走 TURN；其余组合基本能通，对称一方先发包建立映射，对端从来包里学到真实端口。

**为什么。** 打洞的前提是「我告诉对方的地址，正好就是我发给对方时路由器用的地址」。锥形 NAT 满足它；对称 NAT 对每个目的地换端口，破坏了它；而要求端口也严格匹配的一方，又没法靠猜来补上缺的端口。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 238">
<text x="109" y="22" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">完全锥形</text>
<text x="175" y="22" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">地址受限</text>
<text x="241" y="22" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">端口受限</text>
<text x="307" y="22" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">对称</text>
<text x="4" y="55" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">完全锥形</text>
<rect x="79" y="34" width="60" height="30" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="109.0" y="53.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">能直连</text>
<rect x="145" y="34" width="60" height="30" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="175.0" y="53.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">能直连</text>
<rect x="211" y="34" width="60" height="30" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="241.0" y="53.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">能直连</text>
<rect x="277" y="34" width="60" height="30" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="307.0" y="53.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">能直连</text>
<text x="4" y="93" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">地址受限</text>
<rect x="79" y="72" width="60" height="30" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="109.0" y="91.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">能直连</text>
<rect x="145" y="72" width="60" height="30" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="175.0" y="91.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">能直连</text>
<rect x="211" y="72" width="60" height="30" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="241.0" y="91.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">能直连</text>
<rect x="277" y="72" width="60" height="30" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="307.0" y="91.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">能直连</text>
<text x="4" y="131" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">端口受限</text>
<rect x="79" y="110" width="60" height="30" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="109.0" y="129.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">能直连</text>
<rect x="145" y="110" width="60" height="30" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="175.0" y="129.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">能直连</text>
<rect x="211" y="110" width="60" height="30" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="241.0" y="129.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">能直连</text>
<rect x="277" y="110" width="60" height="30" rx="6" stroke-width="1.2" fill="none" stroke="currentColor" stroke-dasharray="3 3"/>
<text x="307" y="129" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">要中继</text>
<text x="4" y="169" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">对称</text>
<rect x="79" y="148" width="60" height="30" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="109.0" y="167.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">能直连</text>
<rect x="145" y="148" width="60" height="30" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="175.0" y="167.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">能直连</text>
<rect x="211" y="148" width="60" height="30" rx="6" stroke-width="1.2" fill="none" stroke="currentColor" stroke-dasharray="3 3"/>
<text x="241" y="167" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">要中继</text>
<rect x="277" y="148" width="60" height="30" rx="6" stroke-width="1.2" fill="none" stroke="currentColor" stroke-dasharray="3 3"/>
<text x="307" y="167" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">要中继</text>
<text x="8" y="208" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">行和列是通话两端各自的 NAT 类型</text>
<text x="8" y="228" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">对称：每换一个目的地就换一个公网端口</text>
</svg>

**面试里这样说。** 「WebRTC 先用 STUN 拿公网地址再打洞。双方都是锥形 NAT 能直连；对称 NAT 遇到对称或端口受限的对端打不通，这部分通话只能走 TURN 中继，所以中继要当作单独的一层来规划容量，而不是偶尔兜底。」

**易错。**
- **以为有 STUN 就总能直连：** 对称 NAT 下 STUN 给出的端口对别人无效。
- **把 NAT 丢包当成故障：** 丢掉未登记的外来包是 NAT 的正常行为，打洞靠的正是先发包建立映射。
- **只看单端的类型：** 能否打通取决于两端类型的组合。
