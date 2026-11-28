---
id: bagu-mem-oom-5-protect
node: a.linux.mem-oom
type: qa
step: 5
---
## Q
**预防与保护 · 怎么保护关键进程**｜追问

面试官：「怎么避免关键服务被 OOM Killer 杀掉？」

## A
**基本回答。** 分两层：先预防，再保护。预防是别触发：容器限制要大于堆加非堆的总和，JVM 用 `-XX:MaxRAMPercentage=70` 之类留出余量；限制并发和本地缓存大小；对 `available` 和 RSS 趋势设告警；开 `-XX:+HeapDumpOnOutOfMemoryError`（堆溢出时自动留下堆转储）。保护是触发了也别杀关键的：关键进程调低 `oom_score_adj`（范围 -1000 到 1000，越低越不容易被选中）。
Kubernetes 靠 QoS：`requests` = `limits` 的 Guaranteed 最后被杀，什么都不设的 BestEffort 最先被杀，中间是 Burstable。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 256">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">Kubernetes 的 QoS 等级决定被杀先后</text>
<rect x="30" y="26" width="280" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170" y="42.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">BestEffort · 最先被杀</text>
<text x="170" y="57.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">没设 requests / limits</text>
<line x1="170" y1="66" x2="170" y2="71" stroke-width="1.2" stroke="currentColor"/>
<polygon points="170,78 166.8,71 173.2,71" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="30" y="78" width="280" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170" y="94.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Burstable · 居中</text>
<text x="170" y="109.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">介于两者之间</text>
<line x1="170" y1="118" x2="170" y2="123" stroke-width="1.2" stroke="currentColor"/>
<polygon points="170,130 166.8,123 173.2,123" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="30" y="130" width="280" height="40" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="170" y="146.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Guaranteed · 最后被杀</text>
<text x="170" y="161.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">requests = limits</text>
<text x="8" y="194" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">进程级：oom_score_adj 越低越安全</text>
<rect x="14" y="202" width="84" height="20" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="56" y="216" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">支付服务</text>
<rect x="242" y="202" width="84" height="20" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="284" y="216" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">离线对账</text>
<line x1="14" y1="236" x2="326" y2="236" stroke-width="1.2" stroke="currentColor"/>
<line x1="14" y1="231" x2="14" y2="241" stroke-width="1.2" stroke="currentColor"/>
<line x1="326" y1="231" x2="326" y2="241" stroke-width="1.2" stroke="currentColor"/>
<text x="8" y="254" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">-1000</text>
<text x="332" y="254" text-anchor="end" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">1000</text>
</svg>
上半是 Kubernetes 里的三档 QoS（服务质量等级）：越往下越晚被杀，关键服务要做到最下面一档。下半是进程级的刻度：`oom_score_adj` 越靠左越不容易被选中，关键进程放左边，离线任务放右边。
**举个例子。** 离线对账任务和支付服务部署在同一台 8 GB 的机器上（演示用的假设值）：
1. **出事前：** 支付服务占约 5 GB，对账任务突然涨到约 3.5 GB，合计超过 8 GB。
2. **OOM Killer 打分：** 支付服务占得最多，分数最高，被杀。
3. **加保护：** 支付设为 Guaranteed（`requests` 等于 `limits`），并调低它的 `oom_score_adj`。
4. **加隔离：** 给对账任务设内存上限，比如 3 GB，它再涨就在自己的上限上被杀，不再波及支付服务。
**代码。** 查看和调整进程的评分：
```bash
cat /proc/<pid>/oom_score        # 当前得分，越高越先被杀
cat /proc/<pid>/oom_score_adj    # 人为调整值，范围 -1000 到 1000
echo -500 > /proc/<pid>/oom_score_adj   # 调低，更不容易被选中（需要权限）
```
**容易错。**
- **以为调高容器内存就万事大吉：** 内存迟早会被用满。要限制并发和缓存，并设告警，否则只是推迟事故。
- **容器限制只按堆大小设：** 堆外、线程栈、元空间都要算进去。
- **把所有进程的 `oom_score_adj` 都调成 -1000：** 缺内存时没有可牺牲的进程，整台机器会更糟。
- **以为 Burstable 和 Guaranteed 一样安全：** 只有 `requests` 等于 `limits` 才是 Guaranteed，最后被杀。
**业务场景。** 离线对账和支付服务同机部署，对账吃光内存，OOM Killer 先杀了占内存最大的支付进程。支付设为 Guaranteed，对账设内存上限，超限只杀自己。
