---
id: bagu-memory-3-conflict-expire
node: a.agent.memory
type: qa
step: 3
---
## Q
**记忆冲突与过期 · 地址变了旧记忆怎么办**｜必会

面试官：「用户上个月说地址在朝阳，这个月说搬到了海淀，记忆里两条都在，怎么处理？」

## A
**基本回答。** 记忆更新不是简单覆盖，而是带时间戳的状态管理。新旧事实矛盾：旧记忆标记为失效，新记忆成为当前有效版本，保留变更时间和来源。过期记忆退出召回，但归档保留，供审计，不物理删除。多来源矛盾：记录各来源和时间，按可信度与新鲜度加权，判不了就标「不确定」。再用定期离线任务去重合并，清理低分记忆（相关度 × 重要度 × 时间衰减）。
**一句话记住。** 记忆更新像查字典的修订版：新版成为当前通行本，旧版不扔进碎纸机，而是放进档案室，需要考证时还能翻出来。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 226">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">时间线</text>
<line x1="8" y1="100" x2="332" y2="100" stroke-width="1.2" stroke="currentColor"/>
<rect x="60" y="36" width="130" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="125.0" y="52.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">朝阳</text>
<text x="125.0" y="67.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">失效，归档保留</text>
<rect x="194" y="36" width="142" height="40" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="265.0" y="52.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">海淀</text>
<text x="265.0" y="67.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">当前有效</text>
<line x1="60" y1="92" x2="60" y2="108" stroke-width="1.2" stroke="currentColor"/>
<line x1="194" y1="92" x2="194" y2="108" stroke-width="1.2" stroke="currentColor"/>
<text x="60" y="124" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">上月说</text>
<text x="194" y="124" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">本月说</text>
<rect x="4" y="150" width="160" height="44" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="84.0" y="168.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">下单：取当前有效</text>
<text x="84.0" y="183.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">→ 海淀</text>
<rect x="176" y="150" width="160" height="44" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="256.0" y="168.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">售后查旧包裹：</text>
<text x="256.0" y="183.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">从归档查到朝阳</text>
<text x="170" y="216" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">旧版本不删，只是不再被召回</text>
</svg>
同一个「地址」有两个版本：朝阳是上月的，已失效归档；海淀是本月的，当前有效。下单取当前，售后考证才翻归档。
**讲明白。**
- **为什么不能直接覆盖：**覆盖会丢掉「曾经是什么」，售后核对和审计就没了依据；不处理则新旧并存，召回时互相打架。
- **新旧矛盾怎么办：**旧记忆标记为失效，新记忆成为当前有效版本，保留变更时间和来源。
- **过时不等于错误：**过时只是对当前查询无效。过期记忆退出召回，但归档保留，供售后核对和审计，不物理删除。
- **多来源矛盾：**记录各来源和时间，按可信度与新鲜度加权，判不了就标记为「不确定」。
- **别急着固化：**一次反馈不能推成稳定偏好，多次验证后才升级。「我可能会……」这类假设语气，不要固化成偏好。
- **要遗忘，但是软遗忘：**定期离线任务给记忆打分（相关度 × 重要度 × 时间衰减），低分的退出召回并归档，重复的合并。
- **向量库软删除的坑：**软删除可能破坏 HNSW（一种分层的近邻图索引）里图的连通性，要定期重建索引。
**举个例子。** 用户上个月说地址在朝阳，这个月说搬到了海淀。
1. **上月：**写入记忆：地址 = 朝阳，当前有效，带来源和时间。
2. **本月：**用户说「搬到海淀了」，抽取时发现它与现有的「地址」矛盾。
3. **更新：**把朝阳标记为失效，记下变更时间；写入新记忆：地址 = 海淀，当前有效。
4. **下单：**召回只取当前有效的，得到海淀。
5. **售后：**核对一个月前的包裹为什么寄到朝阳时，从归档里还能查到那条旧地址。
**容易错。**
- **新值直接覆盖旧值：**丢掉历史，之后没法考证。
- **新旧两条都留着参与召回：**召回时互相打架，一会儿朝阳一会儿海淀。
- **把失效当成删除：**失效只是退出召回，归档仍保留，供审计。
- **一次说就固化成偏好：**单次反馈和假设语气不能直接升级为稳定偏好。
**业务场景。** 下单时只取当前地址「海淀」；售后核对一个月前的包裹为什么寄到朝阳时，仍能从归档里查到那条旧地址。
**系统设计。** [[links.tt-cache-consistency-hot-keys|缓存一致性与热点 Key]]：数据变了旧缓存怎么失效，与记忆更新相近。差异是缓存要的是只剩最新值，记忆要保留旧版本和时间线，不能一删了之。
**相关题。** LC 981 基于时间的键值存储
**可能问法。**
- 记忆冲突怎么处理？ → 不直接覆盖，而是带时间戳做状态管理：新事实成为当前有效版本，旧记忆标记失效并保留变更时间和来源。多来源矛盾时记录各来源，按可信度和新鲜度加权，判不了就标记为不确定。
- 用户改了偏好，旧记忆怎么办？ → 旧记忆标记为失效，退出召回，但归档保留，供售后核对和审计。新偏好成为当前有效版本。注意一次反馈不要直接推成稳定偏好，多次验证后才升级。
- 记忆要不要遗忘？ → 要，但是软遗忘：定期离线任务给记忆打分（相关度 × 重要度 × 时间衰减），低分的退出召回并归档，重复的合并。向量库软删除可能破坏 HNSW 图的连通性，要定期重建索引。
