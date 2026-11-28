---
id: hi-mock-uber-08-dive-location
node: sd.problem-breakdowns.uber.mock
type: qa
step: 8
---
## Q
**网约车 · 第 8 步 · 深入一：司机位置怎么存**｜模拟面试

面试官：「你的位置服务现在把每次上报都写进数据库。我们来聊聊这里，你觉得会有什么问题？」

你会怎么回答？白板上画到哪一步？

## A
**你说。**
- **两个问题：** 写太多，查太慢。1000 万司机 ÷ 5 秒 = 每秒 200 万次写（DynamoDB 约 21.6 万美元/天，PostgreSQL 扛不住或贵到不可行）；按经纬度查附近司机没有索引就全表扫，B 树只能一维范围，二维坐标效果很差。
- **方案一，直接写库：** 就是现在这个，否掉。
- **方案二，批量写加地理库：** 攒一小段再批量写，用 PostGIS 这类带空间索引（R 树、四叉树）的库查近邻；写少了查快了，但批量间隔让位置变旧，匹配次优。可行，不是最好。
- **方案三，Redis 地理类型（选这个）：** 经纬度编码成 geohash（52 位整数）当有序集合的分数，司机 ID 作成员；`GEOADD` 覆盖该司机上一次位置，`GEOSEARCH` 按半径查，取中心格加相邻 8 格再按真实距离过滤，交界处不会漏。全在内存，不用批处理。
- **清理掉线：** 再维护按最后更新时间排序的有序集合 `drivers:ts`，定期删掉超过 30 秒没更新的，同时从地理集合删。
- **风险是持久性：** 内存会丢；开 RDB 或 AOF，用 Sentinel 主从切换；就算丢了，司机每 5 秒重新上报，约 5 秒重建，切换期间只是暂时少看到几位司机。
- **容量：** 单实例按约 10 万次/秒估（要实测），200 万次要约 20 个实例；司机端按速度和方向自适应上报，静止少报，可降约三分之一到约 133 万次/秒，14 个左右。按区域分片，同一城市的司机在同一实例、查询只访问一片；不按司机 ID 哈希，否则每次查询问所有实例。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 630">
<rect x="18" y="8" width="100" height="36" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="68" y="22.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">乘客客户端</text>
<text x="68" y="37.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">Rider Client</text>
<rect x="18" y="72" width="304" height="28" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="170" y="90" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">API 网关 · 鉴权 · 限流 · 路由</text>
<rect x="18" y="164" width="96" height="40" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="66" y="180.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">叫车服务</text>
<text x="66" y="195.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">Ride Service</text>
<rect x="132" y="164" width="72" height="40" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="168" y="180.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">地图 API</text>
<text x="168" y="195.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">距离耗时</text>
<rect x="222" y="8" width="100" height="36" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="272" y="22.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">司机客户端</text>
<text x="272" y="37.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">Driver Client</text>
<rect x="222" y="164" width="100" height="40" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="272" y="180.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">位置服务</text>
<text x="272" y="195.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">Location</text>
<path d="M18,248 a50,6 0 0 1 100,0 v74 a50,6 0 0 1 -100,0 z" stroke-width="1.2" fill="none" stroke="currentColor"/>
<path d="M18,248 a50,6 0 0 0 100,0" fill="none" stroke-width="1.2" stroke="currentColor"/>
<text x="68" y="266" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">数据库</text>
<rect x="26" y="282" width="84" height="20" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="68" y="296" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Fare 表</text>
<rect x="26" y="304" width="84" height="20" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="68" y="318" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Ride 表</text>
<path d="M222,248 a50,6 0 0 1 100,0 v74 a50,6 0 0 1 -100,0 z" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<path d="M222,248 a50,6 0 0 0 100,0" fill="none" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<text x="272" y="266" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Redis</text>
<rect x="230" y="282" width="84" height="20" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="272" y="296" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">drivers:geo</text>
<rect x="230" y="304" width="84" height="20" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="272" y="318" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">drivers:ts</text>
<rect x="222" y="368" width="100" height="60" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="272" y="394.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">匹配服务</text>
<text x="272" y="409.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">Matching</text>
<polyline points="68,44 68,72" fill="none" stroke-width="1.3" stroke="currentColor"/>
<polygon points="68,72 64.8,65.0 71.2,65.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<polyline points="272,44 272,72" fill="none" stroke-width="1.3" stroke="currentColor"/>
<polygon points="272,72 268.8,65.0 275.2,65.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<polyline points="68,100 68,164" fill="none" stroke-width="1.3" stroke="currentColor"/>
<polygon points="68,164 64.8,157.0 71.2,157.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<polyline points="272,100 272,164" fill="none" stroke-width="1.3" stroke="currentColor"/>
<polygon points="272,164 268.8,157.0 275.2,157.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="266" y="148" text-anchor="end" font-size="12" font-family="sans-serif" fill="currentColor">POST /drivers/location</text>
<text x="74" y="118" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">POST /fare, /rides</text>
<text x="74" y="133" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">PATCH /rides/:id</text>
<polyline points="114,184 132,184" fill="none" stroke-width="1.3" stroke="currentColor"/>
<polygon points="132,184 125.0,187.2 125.0,180.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<polyline points="34,204 34,242" fill="none" stroke-width="1.3" stroke="currentColor"/>
<polygon points="34,242 30.8,235.0 37.2,235.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="40" y="228" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">写库</text>
<polyline points="18,184 10,184 10,26 18,26" fill="none" stroke-width="1.3" stroke-dasharray="4 3" stroke="currentColor"/>
<polygon points="18,26 11.0,29.2 11.0,22.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<polyline points="272,204 272,242" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="272,242 268.8,235.0 275.2,235.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="278" y="228" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">GEOADD</text>
<polyline points="250,368 250,328" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="250,328 253.2,335.0 246.8,335.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="256" y="352" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">GEOSEARCH</text>
<polyline points="112,204 112,222 170,222 170,378 222,378" fill="none" stroke-width="1.3" stroke="currentColor"/>
<polygon points="222,378 215.0,381.2 215.0,374.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="164" y="352" text-anchor="end" font-size="12" font-family="sans-serif" fill="currentColor">触发匹配</text>
<rect x="222" y="490" width="100" height="44" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="272" y="508.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">通知服务</text>
<text x="272" y="523.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">APNs · FCM</text>
<polyline points="322,512 332,512 332,26 322,26" fill="none" stroke-width="1.3" stroke="currentColor"/>
<polygon points="322,26 329.0,22.8 329.0,29.2" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<polyline points="272,428 272,490" fill="none" stroke-width="1.3" stroke="currentColor"/>
<polygon points="272,490 268.8,483.0 275.2,483.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="278" y="480" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">推送</text>
<text x="210" y="62" text-anchor="end" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">按速度自适应间隔</text>
<text x="8" y="556" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">Redis 取代位置表：GEOADD 覆盖上一次位置，</text>
<text x="8" y="572" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">GEOSEARCH 查半径内的司机；</text>
<text x="8" y="588" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">drivers:ts 记最后更新时间，定期清 30 秒没更新的；</text>
<text x="8" y="604" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">RDB/AOF 持久化 + Sentinel 主从，丢了 5 秒重建</text>
</svg>
白板上新增：右侧的位置表换成 Redis（地理键 drivers:geo、时间键 drivers:ts）；两条调用改成 `GEOADD` 和 `GEOSEARCH`；司机端旁加一句自适应间隔。

**常见失分。**
- **不先算数：** 没有 200 万次/秒和 21.6 万美元/天，换存储缺理由。
- **只给一个答案：** 不比较前两个方案，看不出懂取舍。
- **回避风险：** Redis 丢数据是最大弱点，主动说缓解办法比被追问好。
- **按司机 ID 分片：** 近邻查询要扫所有分片。
