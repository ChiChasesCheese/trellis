%% trellis:begin %%
# 行情抓取与存储规模
*研究与数据基础设施*

在网卡上抓下所有原始包（pcap）并加硬件时间戳，每天 TB 级；原始包为什么比解码后的数据更值得保存。

**Requires:** [[domains/hft/map/protocols.feed-handler|feed handler 的职责]]

**Unlocks:** [[domains/hft/map/research-infra.time-series-db|时序与列式存储：kdb+/q、ClickHouse、Parquet 与 Arrow]]

## Readings
- [[clickhouse-intro|ClickHouse 简介]]

## Drills
- [[research-infra-backtest-gap|练习：回测很漂亮，实盘第一周就差了]]

## Cards (4)
1. [[hft-research-infra-tick-capture-raw-packets]]
2. [[hft-research-infra-tick-capture-volume]]
3. [[hft-research-infra-tick-capture-hw-timestamps]]
4. [[hft-research-infra-tick-capture-gaps]]
%% trellis:end %%

## Notes
