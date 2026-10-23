---
id: hl-hc11-cpp-diff
node: problems.hc11-order-interval-overlap
type: qa
step: 14
---
## Q
C++ 版订单区间重叠和 Java 版有哪些差异和陷阱（`span`、`variant`、`map::operator[]`、`enum class`、`std::sort`）？

## A
| Java | C++ | 为什么 |
|---|---|---|
| `long[][]`，检查 `length == 2`、`null` | `span<const Interval>` | 固定两字段；只读视图，不会是 null |
| record + 紧凑构造器校验 | `struct` + 构造函数里 `throw` | 对象存在就代表不变量成立 |
| sealed + switch 模式匹配 | `std::variant` + `std::visit(overloaded{...})` | 都是闭合层级 + 编译期穷尽检查 |
| `enum Side` | `enum class Side`（可装别的值） | C++ enum 不保证值域；`static_cast<Side>(7)` 会让 `lanes[7]` 越界，入口检查 |
| `TreeMap.firstEntry()/floorEntry()` | `begin()` / `upper_bound` + `prev` | 要自己处理「没有」（迭代器等于 begin/end） |
| `TreeMap.compute(...)` 删 0 计数 | `find` + 减一 + `erase` | `operator[]` 会插入 |
| `Arrays.sort(long[])` | `std::sort`（严格弱序比较器） | 比较器写错是 UB，不是结果不对 |
| `int` 溢出静默回绕 | 有符号溢出是 UB | `end + 1`、`end - start` 都不能写 |

陷阱：
1. 同一时刻开始排在结束前面：`[1,3)`+`[3,5)` 变成 2；
2. `std::sort` 比较器写成 `<=`：`comp(x,x)` 为 true 不是严格弱序，UB；
3. 闭区间转半开 `end + 1`：`LLONG_MAX` 处有符号溢出；
4. `end - start`、`(a+b)/2`：大时间戳溢出；
5. **`std::map::operator[]` 当读用**：`history[t]` 在 `const` 成员函数里不能写（非 const，会插入），在非 const 函数里写会给不存在的时刻插入记录，让 map 增长并编造「活跃数为 0」的阶梯；
6. `prev(upper_bound(t))` 不检查 `begin()`：在第一条记录之前查询是 UB；
7. 同一时间戳内 place 后 cancel 污染最大值；
8. 线段树查询时下推标记；`exact_index` 在改树之后才检查。

`OnlineOverlap` 深拷贝 / 移动：值语义，拷贝出来的在线对象互相独立。

C++ 小题：为什么 `max_so_far` 要「追溯修正」——被撤的订单区间为空从没活过，时间戳没「过去」时最大值不是最终的，只在时钟离开该时间戳时才并进 `committed_max`。
