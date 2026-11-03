%% trellis:begin %%
# 健壮性：短 `try` 块、不吞 `Exception`、自定义异常层次与 `warnings`
*工程实践：健壮性、测试与交付*

掌握把 `try` 缩到最小、为库定义根异常隔离调用方、异常变量在块外消失、`assert` 只用于内部假设，以及用 `warnings` 做迁移。

**Requires:** [[domains/python/map/runtime.exceptions|异常：层次结构、`try/except/else/finally`、链式异常与异常组]]

**Unlocks:** [[domains/python/map/craft.patterns.validate-then-commit|先校验后提交：失败不留痕迹（validate-then-commit）]], [[domains/python/map/craft.patterns.idempotency-key-stores-result|幂等键存结果：占位 → 执行 → 保存，重复请求拿到第一次的结果]], [[domains/python/map/craft.patterns.reserve-hold-confirm-with-ttl|预留—确认—过期：带 TTL 的持有（hold / confirm / expire）]], [[domains/python/map/craft.patterns.saga-idempotent-compensation|Saga 与幂等补偿：反向撤销，补偿不能失败也不能重复生效]], [[domains/python/map/craft.patterns.retry-backoff-dead-letter|重试、退避与死信：可靠性写一份，渠道只管怎么发]], [[domains/python/map/craft.patterns.conservation-invariant-reconcile|守恒不变量与对账：总和恒为零、钞票守恒、缓存可核对]], [[domains/python/map/craft.idioms.exception-family|异常家族：基类 + 多重继承 + 携带数据（typed errors）]], [[domains/python/map/craft.architecture.source-of-truth-and-derived-caches|真相与派生缓存：谁是真相、谁是投影、漂移怎么办]], [[domains/python/map/craft.architecture.error-boundaries-and-failure-taxonomy|错误边界与失败分类：哪些吞、哪些抛、哪些变成值]]

## Readings
- [[effective-10-robustness|Effective Python 3e · 第 10 章 健壮性]]
- [[pydocs-warnings-module|warnings 模块：警告控制]]

## Drills
- [[engineering-harden-a-payment-script|Drill：把一段收款脚本改成生产可用的版本]]

## Cards (7)
1. [[robust-assert-internal-invariant-only]]
2. [[robust-except-as-var-cleared]]
3. [[robust-except-exception-specific-first]]
4. [[robust-oserror-hierarchy-catch-root]]
5. [[robust-suppress-vs-bare-except-pass]]
6. [[robust-try-else-minimize-scope]]
7. [[robust-warnings-deprecation-migration]]
%% trellis:end %%

## Notes
