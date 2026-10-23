---
id: hl-hc09-cpp-pitfalls
node: problems.hc09-top-trades-by-notional
type: qa
step: 17
---
## Q
C++ 版 top-k notional 有哪些陷阱（`priority_queue` 方向、`string_view`、`set` 更新键、线程异常）？

## A
1. **比较器不是全序**：top-k 结果取决于输入顺序。
2. **`priority_queue` 的 `top()` 是 Compare 下「最大」的**：传错方向堆顶就成了最好的，整个算法反了。以 `better(a, b)` 表示「a 比 b 好」时，堆顶是最差的保留者（Compare 下最大 = 排在最后）。
3. **`reserve(k)`**：k 可以是 `INT_MAX`，传 `min(k, n)`。
4. **`price * volume` 不检查**：UB，不是回绕；`LLONG_MAX * 2` 不会「回绕成 −2」，用 `__builtin_mul_overflow`。
5. **只校验进堆的事件**：后面排在最末的溢出事件被漏掉。
6. **`string_view` 悬空**：指向临时 `std::string`、指向会重新分配的 `vector<string>`、指向已销毁的输入；结果里放 `std::string`。`ranking_` 里放 `string_view` 时，先 `ranking_.erase(...)` 再 `acc_.erase(...)`——先删 map 节点会让 set 条目悬空。
7. **`set` 更新键用 insert 后 erase**：新旧键相等时丢条目（例如一笔 notional 为 0 的成交打到已有 ticker：总额不变，`insert` 因已存在什么也没做，随后 `erase` 把唯一条目删掉，ticker 从排名里消失）。用 `extract` / 改键 / `insert(node)`。
8. **异常从线程函数体里逃出**：`std::terminate`。线程体里 `catch (...)`，保存 `std::current_exception()`，join 之后 `rethrow_exception`。
9. **`std::async` 递归切到 `threshold = 1`**：n 个事件起 n 个线程。
10. **`vector<T>::resize` 需要默认构造**：`TickerTotal` 没有默认构造——截断用 `erase(begin()+k, end())`。

练习题：为什么合并两块的表时溢出与分块方式无关？——所有 notional 非负，部分和单调不减；任意一块或一次合并溢出则真实总和 > `LLONG_MAX`，顺序实现也会溢出；反之总和不超过时所有部分和都不超过。
