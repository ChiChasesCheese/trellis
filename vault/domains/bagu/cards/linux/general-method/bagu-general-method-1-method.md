---
id: bagu-general-method-1-method
node: a.linux.general-method
type: qa
step: 1
---
## Q
**线上排查 · 通用思路**｜必会

面试官：「线上出问题了，你的通用排查思路是什么？」

## A
**基本回答。** 五步：先确认症状和范围；问最近变了什么，能回滚先回滚；止血优先，先恢复服务；再用 USE 方法系统化找根因；最后验证恢复并复盘。
USE 方法：对每种资源（CPU、内存、磁盘、网络）看 Utilization（使用率）、Saturation（有没有排队）、Errors；应用层看黄金指标：延迟、流量、错误、饱和度。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 262">
<rect x="4" y="4" width="116" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="62" y="23" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1 确认症状范围</text>
<text x="126" y="23" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">全部还是一部分？何时开始？</text>
<rect x="4" y="46" width="116" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="62" y="65" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2 问最近变更</text>
<text x="126" y="65" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">发布·配置·活动·依赖方</text>
<line x1="62" y1="35" x2="62" y2="45" stroke-width="1.2" stroke="currentColor"/>
<polygon points="62.0,45.0 58.8,38.0 65.2,38.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="4" y="88" width="116" height="30" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="62" y="107" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3 止血优先</text>
<text x="126" y="107" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">能回滚先回滚，先恢复服务</text>
<line x1="62" y1="77" x2="62" y2="87" stroke-width="1.2" stroke="currentColor"/>
<polygon points="62.0,87.0 58.8,80.0 65.2,80.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="4" y="130" width="116" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="62" y="149" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">4 USE 找根因</text>
<text x="126" y="149" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">使用率·饱和度·错误</text>
<line x1="62" y1="119" x2="62" y2="129" stroke-width="1.2" stroke="currentColor"/>
<polygon points="62.0,129.0 58.8,122.0 65.2,122.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="4" y="172" width="116" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="62" y="191" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">5 验证与复盘</text>
<text x="126" y="191" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">恢复了吗？写下来</text>
<line x1="62" y1="161" x2="62" y2="171" stroke-width="1.2" stroke="currentColor"/>
<polygon points="62.0,171.0 58.8,164.0 65.2,164.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="4" y="220" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">大多数事故和变更有关：先问变更，再敲命令</text>
</svg>
五个格子是五步，高亮的第 3 步最关键：每过一分钟用户都在受损，所以恢复服务排在找根因之前。
**举个例子。** 凌晨收到「支付成功率下降」告警：
1. **确认范围：** 看大盘，成功率从 99% 掉到 90%。按渠道拆开，发现只有渠道 B 掉了，其他渠道正常。
2. **问变更：** 20 分钟前有一次发布，涉及渠道 B 的调用逻辑。
3. **止血：** 先把这次发布回滚，不等根因。
4. **验证恢复：** 几分钟后渠道 B 成功率回到 99%。
5. **找根因：** 回头比对新旧版本的差异，再用 USE 查渠道 B 调用线程池的使用率、排队和错误。
6. **复盘：** 写下时间线和改进项，比如给灰度发布加渠道维度的成功率校验。
**容易错。**
- **一上来就敲命令：** 没确认范围和变更，容易在无关的方向上浪费时间。
- **先找根因再恢复：** 用户一直受损；有变更相关的线索时，回滚比找根因快得多。
- **重启就了事：** 重启会丢现场，根因无从查起，下次还会再来。
- **把 USE 当成只查 CPU：** USE 要对每种资源（CPU、内存、磁盘、网络）都看使用率、饱和度和错误。
