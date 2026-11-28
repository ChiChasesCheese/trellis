---
id: bagu-consistent-hashing-1-ring-vnodes
node: b.distributed.consistent-hashing
type: qa
step: 1
---
## Q
**一致性哈希 · 扩容为什么只迁一小部分、虚拟节点解决什么**｜追问

面试官：「缓存集群从 10 台扩到 11 台，取模哈希会怎样？一致性哈希怎么解决？虚拟节点解决什么问题，数量怎么取？」

## A
**基本回答。** `key % N` 在 N 变化时几乎所有 key 都换节点：模拟 20 万个 key，10 台变 11 台，约 91% 要迁移。一致性哈希把节点和 key 都哈希到 0 到 2^32−1 的环上，key 顺时针遇到的第一个节点负责它；增删节点只影响环上相邻的一段，约 1/N。节点少会倾斜，所以让每台机器在环上占多个虚拟节点（key 先找虚拟节点再映射真实机器）：模拟 10 台，每台 1 个点时最忙节点是平均的 2.3 倍，160 个点降到 1.14 倍；一般每台 100 到 200 个（Nginx 是权重 160），强机器多放点就是加权重，宕机时负载也散到许多台上。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 252">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">哈希环 0~99（示意）</text>
<circle cx="100" cy="120" r="60" fill="none" stroke="currentColor" stroke-width="1.2"/>
<circle cx="157.1" cy="101.5" r="10" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="157.1" y="106.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">A</text>
<circle cx="100.0" cy="180.0" r="10" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="100.0" y="184.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">B</text>
<circle cx="42.9" cy="101.5" r="10" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="42.9" y="106.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">C</text>
<circle cx="51.5" cy="155.3" r="10" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="51.5" y="159.8" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">D</text>
<circle cx="148.5" cy="155.3" r="3.5" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="163.1" y="169.8" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">k1</text>
<circle cx="64.7" cy="71.5" r="3.5" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="54.2" y="60.9" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">k2</text>
<circle cx="64.7" cy="168.5" r="3.5" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="54.2" y="187.1" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">k3</text>
<text x="188" y="40" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">key 顺时针找第一个节点</text>
<text x="188" y="58" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">k1(35) → B(50)</text>
<text x="188" y="76" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">k2(90) → 绕回 A(20)</text>
<text x="188" y="104" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">新增 D(65)：</text>
<text x="188" y="122" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">只接管 (50,65] 的 key</text>
<text x="188" y="140" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">k3(60) 从 C 搬到 D</text>
<text x="188" y="158" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">其余 key 不动</text>
<text x="188" y="188" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">取模：N 变，几乎全搬</text>
<text x="188" y="206" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">10→11 台约 91% 迁移</text>
<text x="8" y="242" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">虚拟节点：每台在环上放 100~200 个点</text>
</svg>
环上有节点 A、B、C，key 顺时针找到的第一个节点负责它（图里为方便取的 0~99 的假哈希值）。新增 D(65) 后，只有 50 到 65 之间的 key 从 C 搬到 D，其余不动。
**容易错。**
- **以为一致性哈希完全不迁移：** 只是迁约 1/N，迁移的数据仍要搬。
- **以为虚拟节点只是为了加节点：** 它主要解决节点少时的分布倾斜，也让宕机的负载分散。
- **以为越多虚拟节点越好：** 太多会让有序结构变大、查找变慢，一般每台 100 到 200 个。
- **以为一致性哈希能做范围查询：** 哈希之后相邻的 key 散在环上各处，范围查询要用范围分片。
- **混淆哈希槽和一致性哈希：** 哈希槽是先固定映射到槽，再把槽分给节点。

**业务场景。** 缓存从 10 台扩到 11 台，若用取模，约九成请求同时穿透到数据库，把库打穿；换成一致性哈希，只有约 1/11 的 key 需要重新加载。
