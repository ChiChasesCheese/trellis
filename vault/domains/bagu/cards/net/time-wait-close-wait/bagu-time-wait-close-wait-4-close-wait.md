---
id: bagu-time-wait-close-wait-4-close-wait
node: a.net.time-wait-close-wait
type: qa
step: 4
---
## Q
**CLOSE_WAIT · 大量堆积说明什么，常见原因有哪些**｜必会

面试官：「监控显示服务有三万个 CLOSE_WAIT，文件描述符快用完了。这说明什么？」

## A
**基本回答。** CLOSE_WAIT 是被动关闭方收到对端 FIN、内核回 ACK 后的状态，要等应用 `close()` 才发自己的 FIN。关不关由应用决定，内核不会超时清理，所以大量堆积几乎都是应用 bug：异常分支漏了 close（连接泄漏），或线程卡住没处理到关闭；最后文件描述符耗尽，报 `Too many open files`。TIME_WAIT 是正常现象、调参缓解，CLOSE_WAIT 必须改代码。修法：try-with-resources（Java）或 `defer`（Go）保证异常路径也关闭，并设空闲超时与读超时。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 262">
<rect x="8" y="6" width="324" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170.0" y="25.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">对端发来 FIN</text>
<rect x="8" y="50" width="324" height="30" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170.0" y="69.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">内核回 ACK，进入 CLOSE_WAIT</text>
<rect x="8" y="94" width="324" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170.0" y="113.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">应用调用 close() 了吗？</text>
<line x1="170" y1="36" x2="170" y2="50" stroke-width="1.2" stroke="currentColor"/>
<polygon points="170.0,50.0 166.8,43.0 173.2,43.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="170" y1="80" x2="170" y2="94" stroke-width="1.2" stroke="currentColor"/>
<polygon points="170.0,94.0 166.8,87.0 173.2,87.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="86" y1="124" x2="86" y2="144" stroke-width="1.2" stroke="currentColor"/>
<polygon points="86.0,144.0 82.8,137.0 89.2,137.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="254" y1="124" x2="254" y2="144" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="254.0,144.0 250.8,137.0 257.2,137.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<rect x="8" y="144" width="156" height="48" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="86.0" y="164.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">调了：发自己的 FIN</text>
<text x="86.0" y="179.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">LAST_ACK 后关闭</text>
<rect x="176" y="144" width="156" height="48" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="254.0" y="164.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">没调（代码 bug）：</text>
<text x="254.0" y="179.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">一直停在 CLOSE_WAIT</text>
<text x="8" y="216" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">内核不会超时清理，描述符越占越多</text>
<text x="8" y="236" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">最后报 Too many open files</text>
<text x="8" y="254" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">TIME_WAIT 调参缓解，CLOSE_WAIT 必须改代码</text>
</svg>
对端 FIN 到达，内核回 ACK 进入 CLOSE_WAIT；应用调了 `close()` 就正常结束，没调就一直停着，描述符越占越多。
**排查。** `ss -ant` 看各状态数量，CLOSE_WAIT 很多就是连接泄漏；`lsof -p <pid>` 看哪类 fd 最多；再查异常路径是否关闭。
**业务场景。** 文件上传服务读对象存储，读取中抛异常直接返回、没关闭响应体；对端关闭连接后本端停在 CLOSE_WAIT，每出一次异常漏一个，堆到几万个，最后新连接 accept 失败报 `Too many open files`。
**容易错。**
- **以为调内核参数能解决：** 关不关由应用决定。
- **和 TIME_WAIT 搞反：** TIME_WAIT 是主动方的正常现象，CLOSE_WAIT 是被动方没 close。
- **只在正常路径里关闭。**
