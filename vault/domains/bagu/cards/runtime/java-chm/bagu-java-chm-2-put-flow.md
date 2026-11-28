---
id: bagu-java-chm-2-put-flow
node: a.runtime.java-chm
type: qa
step: 2
---
## Q
**ConcurrentHashMap · put 的流程：空桶 CAS、非空桶锁头节点**｜必会

面试官：「详细讲讲 ConcurrentHashMap 的 put：什么时候用 CAS，什么时候加锁？为什么这样设计？」

## A
**基本回答。** key 或 value 为 null 抛空指针（`get` 返回 null 时分不清是没有 key 还是值为 null，所以禁止）；算 hash；表没建就先初始化（多个线程靠 CAS 协调，只让一个建表）；目标桶为空就 CAS 放入，失败重试；桶头是 ForwardingNode（该桶已搬到新表、整表在扩容）就去协助搬迁；否则对桶头 `synchronized`，锁内先再确认桶头仍是原来那个节点（`tabAt(tab, i) == f`，拿锁期间可能被替换或搬迁），再遍历链表或树，key 相同覆盖、不同尾插；桶里已有 8 个再插第 9 个且数组长度至少 64 才转树；最后更新计数（baseCount 加分散的 cell，同 LongAdder）并检查扩容。多步遍历加修改 CAS 做不到，所以锁；用 `synchronized` 而非 `ReentrantLock`：不用给每个桶建锁对象，省内存，且 JDK 6 后有锁升级优化。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 306">
<rect x="60" y="6" width="220" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170.0" y="24.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">算 hash，表没建就先初始化</text>
<line x1="170" y1="36" x2="170" y2="52" stroke-width="1.2" stroke="currentColor"/>
<polygon points="170.0,52.0 173.2,45.0 166.8,45.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="60" y="52" width="220" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170.0" y="69.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">找到目标桶 i</text>
<line x1="110" y1="80" x2="58" y2="100" stroke-width="1.2" stroke="currentColor"/>
<polygon points="58.0,100.0 65.7,100.5 63.4,94.5" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="170" y1="80" x2="170" y2="100" stroke-width="1.2" stroke="currentColor"/>
<polygon points="170.0,100.0 173.2,93.0 166.8,93.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="230" y1="80" x2="282" y2="100" stroke-width="1.2" stroke="currentColor"/>
<polygon points="282.0,100.0 276.6,94.5 274.3,100.5" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="6" y="100" width="104" height="50" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="58.0" y="113.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">桶是空的</text>
<text x="58.0" y="128.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">CAS 放入</text>
<text x="58.0" y="143.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">失败就重试</text>
<rect x="118" y="100" width="104" height="50" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170.0" y="113.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">桶头是</text>
<text x="170.0" y="128.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">正在扩容的标记</text>
<text x="170.0" y="143.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">去协助搬迁</text>
<rect x="230" y="100" width="104" height="50" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="282.0" y="113.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">其他情况</text>
<text x="282.0" y="128.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">synchronized</text>
<text x="282.0" y="143.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">锁桶头节点</text>
<line x1="282" y1="150" x2="282" y2="170" stroke-width="1.2" stroke="currentColor"/>
<polygon points="282.0,170.0 285.2,163.0 278.8,163.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="170" y="170" width="164" height="52" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="252.0" y="184.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">锁内先确认桶头</text>
<text x="252.0" y="199.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">没被换掉，再遍历</text>
<text x="252.0" y="214.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">相同覆盖，否则尾插</text>
<line x1="252" y1="222" x2="252" y2="240" stroke-width="1.2" stroke="currentColor"/>
<polygon points="252.0,240.0 255.2,233.0 248.8,233.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="60" y="240" width="220" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170.0" y="257.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">≥8 个节点且表 ≥64 转树</text>
<line x1="170" y1="268" x2="170" y2="278" stroke-width="1.2" stroke="currentColor"/>
<polygon points="170.0,278.0 173.2,271.0 166.8,271.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="170" y="296" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">最后更新计数，检查是否扩容</text>
</svg>
定位到桶之后分三条路：空桶 CAS、正在扩容就帮忙、其他情况锁桶头；右边高亮的是唯一需要加锁的路径。
**业务场景。** 进程内缓存商品详情，大量请求同时 put 不同商品，各落不同的桶，几乎全是 CAS 成功；撞上扩容的线程先帮忙搬再继续；只有同一个商品被并发回源写入才在桶上排队。要让同一个 key 只有一个线程回源，用 `putIfAbsent`（先不加锁检查桶头，命中直接返回）或 `computeIfAbsent`。
**容易错。**
- **以为 put 全程加锁，或锁整张表：** 空桶 CAS 不加锁，加锁也只锁桶头。
