%% trellis:begin %%
# 主备切换与状态恢复
*风险、可靠性与运维*

热备（hot standby）、从日志回放恢复状态、交易所会话的序列号恢复；切换时最危险的是重复下单。

**Requires:** [[domains/hft/map/architecture.sequencer-journal|定序器、日志与确定性回放]]

## Readings
- [[lmax-architecture|The LMAX Architecture]]

## Cards (4)
1. [[hft-reliability-failover-hot-standby]]
2. [[hft-reliability-failover-duplicate-orders]]
3. [[hft-reliability-failover-recover-state]]
4. [[hft-reliability-failover-active-passive-vs-active-active]]
%% trellis:end %%

## Notes
