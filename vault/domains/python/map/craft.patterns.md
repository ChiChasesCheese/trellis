%% trellis:begin %%
# 跨题模式（Patterns）
*编码功力（Coding Craft）*

反复出现在不同题目里的机制：同一个思路在每道题里怎么用、哪里不同、新题看到什么信号要想到它。

## Topics
- [[domains/python/map/craft.patterns.validate-then-commit|先校验后提交：失败不留痕迹（validate-then-commit）]]
- [[domains/python/map/craft.patterns.atomic-claim-check-then-act|原子占位：检查与占用在同一个临界区（claim, not check-then-act）]]
- [[domains/python/map/craft.patterns.idempotency-key-stores-result|幂等键存结果：占位 → 执行 → 保存，重复请求拿到第一次的结果]]
- [[domains/python/map/craft.patterns.notify-outside-the-lock|锁内记事件、锁外派发（collect under lock, dispatch outside）]]
- [[domains/python/map/craft.patterns.external-call-outside-the-lock|外部调用不持锁：占位 → 调用 → 提交（claim, call, commit）]]
- [[domains/python/map/craft.patterns.transition-table-state-machine|转移表状态机：把「哪个状态能去哪」写成数据（State machine as a table）]]
- [[domains/python/map/craft.patterns.injected-clock-three-forms|注入时钟的三种形态：Clock 参数 / 时间戳参数 / tick 步进]]
- [[domains/python/map/craft.patterns.append-only-log-derived-state|只追加日志 + 派生状态：事实不可变，余额/视图可重算（event-sourced state）]]
- [[domains/python/map/craft.patterns.lazy-expiry-settle-on-access|惰性过期：每次访问先结清，不起后台线程（settle on access）]]
- [[domains/python/map/craft.patterns.lazy-deletion-heap|惰性删除堆：墓碑 + 压实（lazy deletion with tombstones and compaction）]]
- [[domains/python/map/craft.patterns.generation-token-stale-detection|代号/版本令牌：识别并拒绝迟到的旧结果（generation token / fencing）]]
- [[domains/python/map/craft.patterns.hash-map-plus-ordered-structure|哈希表 + 有序结构：O(1) 定位，O(log n) 或 O(1) 取序]]
- [[domains/python/map/craft.patterns.condition-wait-predicate-loop|条件变量：谓词 while 循环 + 精确通知（Condition wait loop）]]
- [[domains/python/map/craft.patterns.ordered-multi-lock-acquisition|按全局固定顺序拿多把锁（lock ordering）]]
- [[domains/python/map/craft.patterns.per-key-and-sharded-locks|每个对象一把锁与分片锁：把竞争限制在真正冲突的范围]]
- [[domains/python/map/craft.patterns.immutable-snapshot-publish|不可变快照 + 整体替换发布（copy-on-write publish）]]
- [[domains/python/map/craft.patterns.reserve-hold-confirm-with-ttl|预留—确认—过期：带 TTL 的持有（hold / confirm / expire）]]
- [[domains/python/map/craft.patterns.saga-idempotent-compensation|Saga 与幂等补偿：反向撤销，补偿不能失败也不能重复生效]]
- [[domains/python/map/craft.patterns.dry-run-on-a-copy|在副本上试运行：预测与实际共用同一份逻辑]]
- [[domains/python/map/craft.patterns.dependency-graph-cycle-detection|依赖图与环检测：拓扑排序、可达性、祖先链]]
- [[domains/python/map/craft.patterns.recursive-descent-parsing|递归下降解析：优先级 = 调用层次，分词与求值分离]]
- [[domains/python/map/craft.patterns.rule-chain-pipeline|规则链/流水线：统一接口，引擎只负责按序跑]]
- [[domains/python/map/craft.patterns.policy-seam|策略接缝：把会变的规则做成注入的纯函数/对象]]
- [[domains/python/map/craft.patterns.effective-dated-versions|生效时间版本表：按事件发生时刻取规则（effective-dated lookup）]]
- [[domains/python/map/craft.patterns.single-flight-coalescing|单飞/请求合并：同一件事只做一次，后到者等结果]]
- [[domains/python/map/craft.patterns.bounded-containers-every-dict-has-an-exit|每个只增不减的容器都要有出口：purge / sweep / compact / maxlen]]
- [[domains/python/map/craft.patterns.backpressure-overflow-policy|背压与溢出策略：丢最旧 / 阻塞 / 拒绝，必须当场选并可观测]]
- [[domains/python/map/craft.patterns.retry-backoff-dead-letter|重试、退避与死信：可靠性写一份，渠道只管怎么发]]
- [[domains/python/map/craft.patterns.derived-not-stored|派生状态不存储：算出来，不要存一份第二真相]]
- [[domains/python/map/craft.patterns.conservation-invariant-reconcile|守恒不变量与对账：总和恒为零、钞票守恒、缓存可核对]]
- [[domains/python/map/craft.patterns.make-unmake-undo-log|可逆变更：make/unmake、撤销日志、Edit.invert]]
- [[domains/python/map/craft.patterns.boundary-slicing-and-marginal-tiers|边界切分与边际阶梯：沿规则变化点切段，每段单价固定]]
- [[domains/python/map/craft.patterns.prefix-sum-bisect-timeline|前缀和 + 二分：把「某一时刻/某一站的累计值」变成 O(log n)/O(1)]]
- [[domains/python/map/craft.patterns.predicate-algebra-three-valued|谓词代数与三值逻辑：可组合的小对象 + NULL 传播]]
- [[domains/python/map/craft.patterns.deterministic-tie-break|确定性 tie-break：排序键里写全规则，输出可复现]]
- [[domains/python/map/craft.patterns.half-open-intervals|区间一律左闭右开：[start, end)]]
%% trellis:end %%

## Notes
