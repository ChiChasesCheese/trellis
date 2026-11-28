---
id: hi-sdx-s3-conditional-write
node: sd.patterns.large-blobs.more
type: qa
step: 2
---
## Q
**S3 条件写：不靠数据库的协调**｜补充 · 大文件（Blob）处理 · 追问

面试官：「S3 的一致性模型这些年变了两次。现在你能得到什么？条件写让哪一类系统成为可能？」

## A
**结论。** 2020 年起 S3 对读和列举都是强一致（写入后立刻读到最新）；2024 年起支持条件写：`If-None-Match: *` 只在对象不存在时创建，`If-Match: <ETag>` 只在对象没变时覆盖。这相当于对象上的比较并交换（CAS），多个写者可以不靠额外数据库安全地竞争。

**要点。**
- **强一致：** 写入（含覆盖）之后的 GET 和 LIST 都看到最新版本，「最终一致」的老顾虑已经过时。
- **创建条件：** `If-None-Match: *`，对象已存在就失败，用来「抢占创建」：选主、抢租约、提交日志的下一个版本号。
- **更新条件：** `If-Match`，带上读到的 ETag 覆盖写，别人在你之后改过就失败，用来原子地更新一个指针对象。
- **失败的写者：** 拿到 412 Precondition Failed，重读最新状态再重试；并发请求冲突时也可能是 409，同样重试。
- **能做什么：** 表格式的元数据指针原子切换、租约和锁、只依赖 S3 的队列或日志。
- **2026 亮点：** 条件写现已覆盖 PutObject、CompleteMultipartUpload 和 CopyObject，通用桶还支持带 `If-Match` 的条件删除，且不额外收费，所以「抢占创建、比较并交换、只删自己读到的那个版本」都只靠 S3 就能做。边界是只保证单个 key 的原子性，不是跨 key 事务；还要用桶策略拒绝不带条件的 PutObject，否则有写者绕过。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 290">
<rect x="90" y="8" width="160" height="36" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170.0" y="22.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">对象 manifest</text>
<text x="170.0" y="37.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">ETag = e1</text>
<rect x="10" y="110" width="140" height="40" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="80.0" y="126.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">写者 A</text>
<text x="80.0" y="141.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">PUT If-Match e1</text>
<rect x="190" y="110" width="140" height="40" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="260.0" y="126.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">写者 B</text>
<text x="260.0" y="141.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">PUT If-Match e1</text>
<polyline points="80,110 135.3,49.2" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="140,44 137.7,51.3 132.9,47.0" style="fill:var(--accent,#3b6fd4)"/>
<polyline points="260,110 204.7,49.2" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="200,44 207.1,47.0 202.3,51.3" style="fill:var(--accent,#3b6fd4)"/>
<rect x="10" y="190" width="140" height="40" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="80.0" y="206.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">200 成功</text>
<text x="80.0" y="221.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">ETag 变成 e2</text>
<rect x="190" y="190" width="140" height="40" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="260.0" y="206.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">412 失败</text>
<text x="260.0" y="221.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">e1 已过期</text>
<polyline points="80,150 80.0,183.0" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="80,190 76.8,183.0 83.2,183.0" style="fill:var(--accent,#3b6fd4)"/>
<polyline points="260,150 260.0,183.0" fill="none" stroke-width="1.3" stroke-dasharray="4 3" stroke="currentColor"/>
<polygon points="260,190 256.8,183.0 263.2,183.0" fill="currentColor"/>
<text x="8" y="262" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">B 重读最新 ETag 再决定是否重试</text>
<text x="8" y="280" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">If-None-Match: * 用于抢占创建</text>
</svg>

**面试里这样说。** 「S3 现在强一致，还支持 `If-None-Match` 和 `If-Match` 条件写，等于对象上的 CAS。我可以用它抢租约或原子切换元数据指针，输的一方收到 412，重读状态再试，不需要另外的协调服务。」

**易错。**
- **还按最终一致设计补偿逻辑：** 强一致之后读不到刚写的数据不是问题。
- **条件写失败直接放弃：** 412 表示别人已经赢了，应该读取最新状态后决定是否重试。
