---
id: hi-sdx-infra-canary-baseline
node: more.infra
type: qa
step: 1
---
## Q
**灰度发布怎么自动判定**｜补充 · 平台基础设施：容器、服务网格、发布 · 必会

面试官：「「灰度 5%，然后盯着看板」不算自动化。要把它变成自动的渐进发布，需要哪些部件？」

## A
**结论。** 四个部件：基线对照、自动判定、分级放量、自动回滚。关键是金丝雀不和长期运行的整个集群比，而是和「新部署的、同样规模的旧版本」比。

**要点。**
- **基线配对：** 单独起一组旧版本，规模和流量份额与金丝雀相同。长期运行的旧集群缓存已热、节点分布不同，直接比较会被预热和位置污染。
- **自动判定：** 预先定义指标查询（错误率、延迟分位数、饱和度、关键业务指标），每一级放量都对金丝雀和基线做统计比较（Kayenta、Argo Rollouts 这类工具）。
- **分级放量：** 1% → 5% → 25% → 100%，每次放量前过一道判定。
- **自动回滚：** 判定失败就把流量切回去，不需要人介入，回滚的恢复时间从「有人发现」变成几秒。
- **2026 亮点：** 灰度的对象不只是二进制，规则、配置、特征文件这类内部生成的数据同样要分批生效、可一键回滚到上一个已知良好版本，并像对待用户输入一样校验大小和格式、设上限，关键功能配全局 kill switch；一份坏配置全网同步，爆炸半径就是全站。排障时好坏交替往往是渐进式变更（部分节点已更新）造成的，别先入为主当成攻击。代价是多一层校验和灰度，配置生效更慢。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 264">
<rect x="110" y="8" width="120" height="30" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="170.0" y="27.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">入口流量</text>
<polyline points="170,38 170.0,53.0" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="170,60 166.8,53.0 173.2,53.0" style="fill:var(--accent,#3b6fd4)"/>
<rect x="8" y="60" width="100" height="50" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="58.0" y="74.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">基线 5%</text>
<text x="58.0" y="89.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">新部署的</text>
<text x="58.0" y="104.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">旧版本</text>
<rect x="120" y="60" width="100" height="50" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170.0" y="81.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">金丝雀 5%</text>
<text x="170.0" y="96.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">新版本</text>
<rect x="232" y="60" width="100" height="50" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="282.0" y="74.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">其余 90%</text>
<text x="282.0" y="89.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">长期运行的</text>
<text x="282.0" y="104.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">旧版本</text>
<line x1="58" y1="124" x2="170" y2="124" stroke-width="1" stroke="currentColor" opacity="0.4"/>
<text x="60" y="146" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">同样规模、同样流量：判定只比这两组</text>
<line x1="8" y1="162" x2="332" y2="162" stroke-width="1" stroke="currentColor" opacity="0.4" stroke-dasharray="3 3"/>
<text x="8" y="184" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">逐级放量，每级过一道自动判定：</text>
<text x="8" y="206" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">1% → 5% → 25% → 100%</text>
<text x="8" y="228" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">判定不过就自动把流量切回旧版本，</text>
<text x="8" y="246" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">不靠人盯着看板</text>
</svg>

**面试里这样说。** 「我会同时部署金丝雀和一组同规模的旧版本基线，按错误率、p99 延迟和关键业务指标逐级放量，每级自动判定，不过就自动回滚。」

**易错。**
- **拿金丝雀和整个旧集群比：** 预热和流量差异会造成误报或漏报。
- **只看错误率：** 延迟变差或业务指标下降，请求依然是成功的，要把它们一起纳入判定。
