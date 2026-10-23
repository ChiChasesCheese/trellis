---
id: hl-hc06-branch-prediction
node: problems.hc06-cpu-register-bitwise
type: qa
step: 14
---
## Q
为什么解码到 `int[]` 后，随机程序只快 1.5 倍、固定循环程序却快 9 倍？「无分支」到底指什么，还能怎么优化？

## A
实测（200 万条指令，预热后）：
| 程序形态 | `run`（对象 + 模式匹配） | `execute`（`int[]`） |
|---|---|---|
| 随机 18 种指令 | 21 ms | 14 ms |
| 随机，仅 14 种更新型指令 | 17 ms | 11 ms |
| 固定循环的 14 条指令 | 9 ms | **1 ms** |

解读：CPU 流水线同时处理十几条指令的不同阶段，遇到分支（`if`、`switch` 跳转）不知走哪条就**猜**；**分支预测**猜对白赚，猜错则作废，代价约十几个周期。规律序列猜得准，随机序列几乎只能蒙。`switch (ops[pc])` 编译成一次**间接跳转**，操作码随机时预测大量失败，把 `int[]` 省掉的对象指针追逐和类型检查吃掉一大半。

所以「无分支」指**指令语义内部**（移位、位号），不是分发。要诚实说：分支预测才是剩下的瓶颈。

**还能更快**（口头提）：
- 把相邻的 `AND/OR/XOR/NOT/SET/CLEAR/TOGGLE` 融合成一条 `r = (r & a) ^ x`；
- 常量折叠；
- 把整个程序翻译成 JVM 字节码 / `MethodHandle`，让 JIT 去掉分发；
- 批量跑很多寄存器时向量化（`jdk.incubator.vector`）；
- C++：threaded code（computed goto）、超指令、直接生成机器码。

`std::variant` 的 `visit`：备选类型少且内联时，编译器生成按下标的跳转表，开销接近一次 `switch`。
