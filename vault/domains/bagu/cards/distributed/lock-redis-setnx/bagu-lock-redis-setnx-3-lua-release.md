---
id: bagu-lock-redis-setnx-3-lua-release
node: a.distributed.lock-redis-setnx
type: qa
step: 3
---
## Q
**释放锁 · 为什么用 Lua，GET 再 DEL 会怎样**｜必会

面试官：「释放锁为什么要用 Lua 脚本？先 GET 比较一致再 DEL 不行吗？」

## A
**基本回答。** 不行。`GET` 和 `DEL` 是两条命令，中间不是原子的：A 刚 `GET` 发现是自己的，锁恰好过期被 B 拿走，A 的 `DEL` 又把 B 的锁删了。Lua 脚本在 Redis 里整体原子执行，比较和删除之间没有空隙，所以释放锁要用 Lua。脚本见后面的代码一节。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 300">
<rect x="10" y="6" width="80" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="50" y="23" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">客户端 A</text>
<line x1="50" y1="32" x2="50" y2="252" stroke-width="1.2" stroke="currentColor" stroke-dasharray="4 3"/>
<rect x="130" y="6" width="80" height="26" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="170" y="23" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Redis</text>
<line x1="170" y1="32" x2="170" y2="252" stroke-width="1.2" stroke="currentColor" stroke-dasharray="4 3"/>
<rect x="250" y="6" width="80" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="290" y="23" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">客户端 B</text>
<line x1="290" y1="32" x2="290" y2="252" stroke-width="1.2" stroke="currentColor" stroke-dasharray="4 3"/>
<text x="8" y="62" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">①</text>
<text x="54" y="58" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">GET → 是我的</text>
<line x1="50" y1="64" x2="163" y2="64" stroke-width="1.2" stroke="currentColor"/>
<polygon points="170,64 163,67.2 163,60.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="176" y="90" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">② 锁到期</text>
<text x="176" y="106" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">key 消失</text>
<text x="176" y="128" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">③ B 加锁成功</text>
<line x1="290" y1="134" x2="177" y2="134" stroke-width="1.2" stroke="currentColor"/>
<polygon points="170,134 177,130.8 177,137.2" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="184" y="160" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">SET NX → OK</text>
<text x="54" y="186" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">④ DEL</text>
<line x1="50" y1="192" x2="163" y2="192" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="170,192 163,195.2 163,188.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="176" y="210" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">A 以为还是自己的</text>
<text x="176" y="230" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">B 的锁被删了</text>
<rect x="6" y="260" width="328" height="32" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="170" y="280" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Lua：比较和删除一步完成，中间插不进去</text>
</svg>
四步缝隙：A 的 `GET` 确认是自己的，可是还没来得及 `DEL`，锁就到期了，B 抢到，A 的 `DEL` 随后删掉的是 B 的锁。底下的 Lua 把比较和删除合成一步，缝隙就没了。
**代码。** 释放锁的 Lua 脚本：
```lua
if redis.call("get", KEYS[1]) == ARGV[1] then
  return redis.call("del", KEYS[1])   -- 是自己的才删
else
  return 0                            -- 不是自己的，什么也不做
end
```
**容易错。**
- **以为先 GET 比较再 DEL 就够了：** 两条命令之间有缝隙，GET 时是自己的，DEL 时可能已是别人的。
- **以为 Lua 脚本里可以访问任意 key：** 集群下脚本涉及的 key 必须通过 `KEYS` 传入，且落在同一个槽。
- **把 Lua 脚本当成事务回滚：** 它保证的是执行期间不被打断，脚本执行到一半出错并不会自动回滚已经执行的命令。
- **新版本还在手写 Lua：** Redis 8.4.0 起有 `DELEX key IFEQ <value>`。

