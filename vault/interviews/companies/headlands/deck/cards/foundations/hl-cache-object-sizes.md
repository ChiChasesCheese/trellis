---
id: hl-cache-object-sizes
node: foundations.cpu-cache-locality
type: qa
step: 16
---
## Q
64 位 JVM 开启压缩指针时，`Integer`、`Long`、`Double`、`HashMap.Node`、数组头各占多少字节？`HashMap<Integer,Integer>` 一个条目大约多大？

## A
- `Integer` 16 B、`Long` 24 B、`Double` 16 B（头 12 B + 值 + 对齐；`Integer` 的 4 B 值刚好填进 4 B 空隙）；
- `Object[]` / `int[]` 的头：16 B（12 B 头 + 4 B 长度）；
- `HashMap.Node`：32 B（头 12 + hash 4 + key / value / next 引用各 4，再对齐）；
- `HashMap<Integer,Integer>` 每条目：约 32 + 16 + 16 + 桶槽 4 ≈ **70 B**，只存 8 字节有效数据。

具体大小可用 OpenJDK 的 JOL 工具打印；面试说「约」。
