---
id: bagu-cap-base-2-cp-ap
node: a.distributed.cap-base
type: qa
step: 2
---
## Q
**CP 与 AP · 分区时各自怎么表现**｜必会

面试官：「网络分区时，CP 系统和 AP 系统分别怎么表现？举一个你用过的例子。」

## A
**基本回答。** CP 系统：为保证一致，少数派一侧拒绝服务，如 ZooKeeper，写请求走 ZAB 协议，要过半数节点确认：5 个节点切成 3 + 2，3 个的一侧还能写和选主，2 个的一侧不能写也选不出主。AP 系统：两侧都继续响应，数据可能暂时不一致，恢复后靠冲突合并、版本号、读修复（Read Repair，读时发现副本不一致顺手修好）收敛，如服务注册中心 Eureka，宁可返回过期的实例列表，也不拒绝查询（心跳大量丢失时进入自我保护，不再剔除实例）。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 214">
<text x="8" y="14" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">CP：ZooKeeper 5 个节点被切成 3 + 2</text>
<rect x="8" y="24" width="150" height="48" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="83" y="44.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">多数派 3 个节点</text>
<text x="83" y="59.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">可写、可选主</text>
<rect x="182" y="24" width="150" height="48" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="257" y="44.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">少数派 2 个节点</text>
<text x="257" y="59.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">拒绝写，返回错误</text>
<line x1="158" y1="48" x2="182" y2="48" stroke-width="1.2" stroke="currentColor" stroke-dasharray="4 3"/>
<line x1="164" y1="42" x2="176" y2="54" stroke-width="1.8" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="164" y1="54" x2="176" y2="42" stroke-width="1.8" style="stroke:var(--accent,#3b6fd4)"/>
<text x="8" y="100" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">AP：Eureka 分区后两侧都继续服务</text>
<rect x="8" y="110" width="150" height="48" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="83" y="130.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">A 侧继续服务</text>
<text x="83" y="145.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">返回自己的列表</text>
<rect x="182" y="110" width="150" height="48" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="257" y="130.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">B 侧继续服务</text>
<text x="257" y="145.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">列表可能稍旧</text>
<line x1="158" y1="134" x2="182" y2="134" stroke-width="1.2" stroke="currentColor" stroke-dasharray="4 3"/>
<line x1="164" y1="128" x2="176" y2="140" stroke-width="1.8" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="164" y1="140" x2="176" y2="128" stroke-width="1.8" style="stroke:var(--accent,#3b6fd4)"/>
<text x="8" y="186" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">CP：宁可没数据，也不给错数据</text>
<text x="8" y="204" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">AP：宁可给旧数据，也不拒绝</text>
</svg>
同样是网络被切开：CP 的少数派一侧闭嘴，AP 的两侧都继续回答。
**容易错。**
- **以为 CP 就是「不会出错」：** CP 是不出错的数据，代价是出现不可用。
- **以为 AP 就是「数据会丢」：** AP 是暂时不一致，恢复后通过合并、版本号、读修复收敛，不是丢。
- **以为一个系统只能整体属于 CP 或 AP：** 同一个系统里读和写可以不同，如功能开关读选可用、改开关才要求一致。
- **以为 ZooKeeper 读到的永远是最新：** 默认读本地副本，要最新值得先 `sync`。

**业务场景。** 功能开关服务读取开关值：分区时客户端用本地缓存的旧开关继续服务（AP），短时间内个别用户看到旧功能；若强求读到最新值（CP），分区会让所有读取失败，整个业务停摆。
