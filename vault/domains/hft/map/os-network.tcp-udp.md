%% trellis:begin %%
# TCP 与 UDP 组播在交易中的分工
*操作系统与网络*

行情用 UDP 组播（一对多、无重传）、下单用 TCP（可靠、有序）；Nagle 算法与 TCP_NODELAY、延迟确认。

**Requires:** [[domains/hft/map/os-network.kernel-stack|内核网络栈的代价]]

## Readings
- [[wiki-nagle|Nagle 算法]]

## Cards (4)
1. [[hft-os-network-tcp-udp-market-data-multicast]]
2. [[hft-os-network-tcp-udp-orders-over-tcp]]
3. [[hft-os-network-tcp-udp-nagle-nodelay]]
4. [[hft-os-network-tcp-udp-gap-recovery-ab-feeds]]
%% trellis:end %%

## Notes
