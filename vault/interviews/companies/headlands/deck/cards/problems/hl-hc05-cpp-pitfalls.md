---
id: hl-hc05-cpp-pitfalls
node: problems.hc05-market-order-book
type: qa
step: 21
---
## Q
写 C++ 订单簿时有哪些容易踩的陷阱？

## A
1. 总量溢出：`total += qty` 先加后查（有符号溢出是 UB）；先改后查导致簿被改了一半；
2. **保存的迭代器**：拷贝 `OrderBook`；用 `vector` 保存订单再保存迭代器 / 引用；
3. `pop_front()` 之后继续用 `maker` 引用（悬空）；
4. `std::stoll` 解析接受 `"12abc"`；`std::from_chars("1.5")` 返回成功（读到 `.` 停下），要检查 `end == 末尾`；`toupper` 传负数；
5. `size_t` 和 `int` 比较（`n < 0` 转成巨大无符号数）；
6. `long long` 价格直接 `static_cast<int>`：`2³² + 5` 变成 5。先在 64 位上检查范围再收窄；
7. `TickBook`：回移删除写成直接置空；最优价被吃光后没更新；池满时仍然撮合；
8. `std::function` 作热路径回调：较大的捕获会分配；
9. 价位空了没从 `map` 删，`best_bid` 返回空价位；
10. 限价单溢出检查放在撮合之后；
11. 收窄转换在 C++ 里是静默的（Java 不允许隐式收窄）。

**测零分配**：重载全局 `operator new` 数次数，节点式容器每元素一次分配，预分配数组为零。

C++ 追问：异常安全——所有会失败的检查放修改之前（强保证）；`unordered_map::find` 的迭代器 rehash 后失效，元素引用仍有效；`map` 还是数组：价格带有界且不太稀疏时数组 O(1)、无分配、缓存友好；很大或很稀疏用 `map`（或 B 树 / 跳表）。
