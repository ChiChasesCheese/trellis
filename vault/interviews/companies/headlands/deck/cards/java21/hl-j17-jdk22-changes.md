---
id: hl-j17-jdk22-changes
node: java21.j17-ffm-api
type: qa
step: 16
---
## Q
JDK 21 → JDK 22，FFM API 有哪些要改的地方？

## A
| | JDK 21 | JDK 22（**转正**） |
|---|---|---|
| 状态 | 第三次预览，要 `--enable-preview` | **正式 API**，不需预览参数 |
| 字符串 | `arena.allocateUtf8String(s)` | 改名 `arena.allocateFrom(s)` |
| `MemoryLayout.varHandle` 坐标 | `(MemorySegment, long… 每个开放路径元素一个)` | 多一个**基偏移**坐标，`PX.get(pool, i)` 要写成 `PX.get(pool, 0L, i)` |
| 受限方法 | 不带 `--enable-native-access` 打印一次警告 | 同；新增 JAR 清单属性 `Enable-Native-Access`；未来可能强制要求 |

22 另新增：下行调用可传堆上段、可编程构建 C 函数描述符、更好支持变长数组、本地字符串可用任意字符集。
