%% trellis:begin %%
# 代号/版本令牌：识别并拒绝迟到的旧结果（generation token / fencing）
*编码功力（Coding Craft） / 跨题模式（Patterns）*

每次状态转换让代号加一；许可带着领取时的代号，回报时代号不一致就只计数、不改状态。

**Requires:** [[domains/python/map/concurrency.locks-races|竞态条件与同步原语：`Lock`、`RLock`、`Condition`、`Event`、`Semaphore`]]

## Cards (5)
1. [[craft-generation-token-stale-detection-1-breaker-gen]]
2. [[craft-generation-token-stale-detection-2-lease-attempt]]
3. [[craft-generation-token-stale-detection-3-across-problems]]
4. [[craft-generation-token-stale-detection-4-equality-vs-order]]
5. [[craft-generation-token-stale-detection-5-scales-fencing]]
%% trellis:end %%

## Notes
