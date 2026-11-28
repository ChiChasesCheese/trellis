---
id: bagu-spike-10x-2-real-or-fake
node: a.protect.spike-10x
type: qa
step: 2
---
## Q
**QPS 突增十倍 · 怎么判断是真实流量还是攻击或重试风暴**｜必会

面试官：「QPS 涨了十倍，你先看什么？怎么判断该扩容还是该封禁？」

## A
**基本回答。** 先验血再开药，三种原因处理相反：攻击在入口封禁或限流，重试风暴要止住上游重试（对出问题的版本限流、回滚、客户端指数退避），确认是真实用户才扩容。前五分钟看三件事：来源（IP、地区、User-Agent 是否集中；真实用户是分散的）、接口分布（真实用户走完整路径，机器流量常只打一两个接口）、独立用户数（最关键：QPS 涨十倍而独立用户数没涨，几乎确定是重试或机器流量）；再看请求头的重试标记占比，并对照近期发布和配置变更，回滚最近的发布往往是最快的止血。重试风暴是调用方自己放大：服务稍慢，客户端超时立刻重试，更慢，更多重试，放大源头在上游，扩容挡不住。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 236">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">QPS 涨十倍，前五分钟看这三件事</text>
<rect x="8" y="30" width="146" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="81.0" y="46.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">来源 IP、UA 集中</text>
<text x="81.0" y="61.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">只打一两个接口</text>
<line x1="154" y1="50" x2="178" y2="50" stroke-width="1.2" stroke="currentColor"/>
<polygon points="178.0,50.0 171.0,46.8 171.0,53.2" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="178" y="30" width="154" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="255.0" y="46.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">攻击或爬虫</text>
<text x="255.0" y="61.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">入口封禁、限流</text>
<rect x="8" y="82" width="146" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="81.0" y="98.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">独立用户数没涨</text>
<text x="81.0" y="113.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">重试标记占比高</text>
<line x1="154" y1="102" x2="178" y2="102" stroke-width="1.2" stroke="currentColor"/>
<polygon points="178.0,102.0 171.0,98.8 171.0,105.2" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="178" y="82" width="154" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="255.0" y="98.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">重试风暴</text>
<text x="255.0" y="113.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">止住上游、回滚发布</text>
<rect x="8" y="134" width="146" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="81.0" y="150.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">独立用户数同比涨</text>
<text x="81.0" y="165.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">来源分散</text>
<line x1="154" y1="154" x2="178" y2="154" stroke-width="1.2" stroke="currentColor"/>
<polygon points="178.0,154.0 171.0,150.8 171.0,157.2" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="178" y="134" width="154" height="40" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="255.0" y="150.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">真实流量</text>
<text x="255.0" y="165.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">保核心，再扩容</text>
<text x="8" y="206" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">同时对照：最近有没有发布、配置变更</text>
<text x="8" y="226" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">回滚最近的发布，往往是最快的止血</text>
</svg>
左边是症状，右边是结论和动作；只有最后一行确认是真实用户才走到扩容。
**业务场景。** 新版客户端有 bug，请求失败后不退避、每秒重试：QPS 从 1 万涨到 10 万，独立用户数几乎没变，绝大部分请求落在同一个失败接口，重试标记占大多数，二十分钟前刚发了新版客户端；服务端先对该版本限流并回滚客户端配置，不扩容，流量几分钟内回落。
**容易错。**
- **只看 QPS 不看用户数。**
- **把重试风暴当攻击去封 IP：** 重试来自正常用户，只会误伤。
- **漏看发布和配置变更。**
