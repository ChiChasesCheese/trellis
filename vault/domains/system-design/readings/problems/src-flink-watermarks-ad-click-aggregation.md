---
nodes: [problems.search.ad-click-aggregation]
url: https://nightlies.apache.org/flink/flink-docs-master/docs/dev/datastream/event-time/generating_watermarks/
tags: []
---
# Generating Watermarks — Apache Flink Documentation

值得读：Flink 官方文档，给出水位线生成的具体机制——bounded-out-of-orderness 策略（当前
观察到的最大时间戳减去一个容忍延迟）、多输入算子取各输入水位线最小值、空闲数据源的
idleness 处理。本题「深入探讨」第 2 节采用的水位线策略描述直接来自这份文档；文档本身还
覆盖了自定义 `WatermarkGenerator` 的实现细节，本题没有用到。
