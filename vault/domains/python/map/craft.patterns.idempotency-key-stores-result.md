%% trellis:begin %%
# 幂等键存结果：占位 → 执行 → 保存，重复请求拿到第一次的结果
*编码功力（Coding Craft） / 跨题模式（Patterns）*

用 (调用方, 键) 原子地占一条记录；重复请求等拥有者出结果，原样返回；同键不同内容报错；失败要释放。

**Requires:** [[domains/python/map/concurrency.locks-races|竞态条件与同步原语：`Lock`、`RLock`、`Condition`、`Event`、`Semaphore`]], [[domains/python/map/engineering.robustness|健壮性：短 `try` 块、不吞 `Exception`、自定义异常层次与 `warnings`]]

## Cards (5)
1. [[craft-idempotency-key-stores-result-1-claim-run-store]]
2. [[craft-idempotency-key-stores-result-2-store-rejection-and-fingerprint]]
3. [[craft-idempotency-key-stores-result-3-same-id-across-problems]]
4. [[craft-idempotency-key-stores-result-4-owner-failure-release]]
5. [[craft-idempotency-key-stores-result-5-scales-stripe]]
%% trellis:end %%

## Notes
