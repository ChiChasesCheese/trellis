---
id: bagu-microservice-governance-1-split-config-session
node: b.distributed.microservice-governance
type: qa
step: 1
---
## Q
**微服务治理 · 拆分粒度、配置中心、分布式 Session**｜追问

面试官：「把单体支付系统拆成账户、订单、渠道三个服务，粒度怎么定，什么时候不该拆？配置中心要解决什么，推送怎么设计？登录态怎么跨实例共享？」

## A
**基本回答。** 按业务能力和限界上下文（DDD 的 bounded context）拆，同时看团队规模和复杂度：一个服务要小到一两个人能讲清细节，边界还受组织结构影响（康威定律）。不按数据表拆；多个服务总是一起改、一起发布、共用库表，就是分布式单体。配置变更下发有推（实时但要维护连接）、拉（简单但有延迟）、长轮询（主流，Apollo 约挂 60 秒，兼顾实时和简单）；客户端要内存、本地快照、代码默认值多级兜底，配置中心挂了仍能用快照启动。登录态跨实例最常用集中存 Redis，实例无状态，设过期和续期；粘性会话实例挂了就丢。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 280">
<text x="8" y="14" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">配置中心：长轮询</text>
<rect x="20" y="22" width="100" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="70.0" y="38.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">客户端</text>
<rect x="210" y="22" width="120" height="24" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="270.0" y="38.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">配置中心</text>
<line x1="70" y1="46" x2="70" y2="150" stroke-width="1.2" stroke="currentColor" stroke-dasharray="4 3"/>
<line x1="270" y1="46" x2="270" y2="150" stroke-width="1.2" stroke="currentColor" stroke-dasharray="4 3"/>
<line x1="70" y1="70" x2="268" y2="70" stroke-width="1.2" stroke="currentColor"/>
<polygon points="268.0,70.0 261.0,73.2 261.0,66.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="170" y="64" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">请求，服务端挂起约 60 秒</text>
<line x1="268" y1="100" x2="72" y2="100" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="72.0,100.0 79.0,96.8 79.0,103.2" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="170" y="94" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">有变更：立即返回</text>
<line x1="70" y1="130" x2="268" y2="130" stroke-width="1.2" stroke="currentColor"/>
<polygon points="268.0,130.0 261.0,133.2 261.0,126.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="170" y="124" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">处理完，再发下一次</text>
<text x="8" y="170" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">登录态：集中存 Redis（最常用）</text>
<rect x="10" y="182" width="96" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="58.0" y="199.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">实例 1</text>
<line x1="58" y1="208" x2="58" y2="238" stroke-width="1.2" stroke="currentColor"/>
<polygon points="58.0,238.0 54.8,231.0 61.2,231.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="122" y="182" width="96" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170.0" y="199.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">实例 2</text>
<line x1="170" y1="208" x2="170" y2="238" stroke-width="1.2" stroke="currentColor"/>
<polygon points="170.0,238.0 166.8,231.0 173.2,231.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="234" y="182" width="96" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="282.0" y="199.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">实例 3</text>
<line x1="282" y1="208" x2="282" y2="238" stroke-width="1.2" stroke="currentColor"/>
<polygon points="282.0,238.0 278.8,231.0 285.2,231.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="40" y="240" width="260" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="170.0" y="258.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Redis：会话 + 过期时间，续期</text>
</svg>
上半部分是配置中心的长轮询：客户端发请求，服务端挂起约 60 秒，有变更立即返回，处理完再发下一次；下半部分是登录态：多个实例都把会话存进同一个 Redis，实例本身无状态。
**容易错。**
- **按数据表拆服务：** 一个业务动作会跨好几个服务，应按业务能力拆。
- **以为拆得越小越好：** 调用链越长，超时、重试、一致性问题越多；团队小时先别拆。
- **以为拆完就解耦了：** 多个服务总是一起改一起发，是分布式单体。
- **以为配置变更一定会自动生效：** 注入到普通字段的值不一定自动刷新。
- **以为 JWT 吊销很容易：** 无状态令牌难吊销，要靠短期过期加黑名单。

**业务场景。** 拆分后下单调账户服务超时，订单侧重试，账户被扣两次，所以扣款接口必须带幂等键；渠道开关通过配置中心灰度下发，出问题一键回滚。
