---
id: trust-center-scanner-packages
node: security.trust-center-posture
type: qa
tags: [grown]
---
## Q
Snowflake 的信任中心（Trust Center）是什么？它是怎样发现账户里的安全错误配置的？

## A
信任中心是 Snowsight 中内置的安全态势管理功能：它按计划运行扫描器（scanner），扫描器被组织成扫描器包（scanner package），每个包针对一类规范检查账户配置——例如基于 CIS Snowflake 基准（CIS Benchmark）的检查、以及威胁情报类检查。扫描结果汇总为发现项（finding），附带严重程度和修复建议，形成按优先级排序的风险清单，不需要导出配置到外部工具去分析。
