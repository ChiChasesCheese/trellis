---
id: hl-hc07-cpp-diff
node: problems.hc07-ticker-hash-map
type: qa
step: 21
---
## Q
C++20 版 ticker 哈希表和 Java 版在 key 类型、溢出、位运算、字节缓冲、越界、堆外上有什么差别？

## A
| 点 | Java | C++20 |
|---|---|---|
| key 类型 | `String` / `long`（有符号，> 0 合法） | `std::string_view` / `uint64_t`（`0` 空、`~0` 墓碑；`-1` 的隐式转换是陷阱） |
| 链地址的代价 | `HashMap` 每条目一个对象 + 装箱 | `unordered_map` 每条目一个节点；短 `string`（≤ 15）SSO 不分配，指针追逐才是主要问题 |
| 溢出 | `Math.addExact` | `__builtin_add_overflow`（有符号溢出是 UB，不能事后检查） |
| 位运算 | `Long.compress`、`numberOfTrailingZeros` | `std::countr_zero`、`std::bit_ceil`（`<bit>`），x86 `pext`；字节序用 `std::endian` |
| 字节缓冲 | `VarHandle` 读 `byte[]` | `memcpy` 进 `uint64_t` + `bswap` |
| 越界 | 一律抛 `IndexOutOfBounds` | `operator[]` 是 UB，`at()` 才检查；偏移量计算要防回绕 |
| 分配统计 | `ThreadMXBean` | 重载全局 `operator new` 计数 |
| 堆外 | `Arena`，为了躲 GC | 没有 GC；剩下对齐、定长、地址不变、生命周期 |

C++ 陷阱清单：`hash & mask`；删除置空 / 遇墓碑就插入 / 装载因子不算墓碑；`(c-'A'+1) << 35` 的 `int` 移位；`char` 有符号；`'\0'` 与 `const char*` 截断；`off + 8 > size` 回绕；`put(-1, v)` 变成墓碑标记；`index_of` 不比较原始 key；`h + d*c` 哈希族；`vector<bool>` 当标志数组；编译器生成的移动构造不会清空源对象的标量成员；`operator new[]` / aligned new 和普通 `delete` 混用；`add` 溢出后表被改了一半。

`std::hash<string_view>` 对字符串是正常哈希，但对整数是恒等函数。`unordered_map` 保证元素引用不失效（链地址的优点）。
