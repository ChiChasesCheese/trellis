---
id: hl-hc08-cpp-pitfalls
node: problems.hc08-order-sequence-api
type: qa
step: 14
---
## Q
C++ 版订单序列有哪些容易踩的陷阱（哈希、移动构造、`unordered_map` 内存）？

## A
1. **`index_of_[id]`** 查询：缺 key 时 `operator[]` 会插入默认值；只查用 `find`。
2. **`std::hash<long long>` 恒等 + 2 的幂桶数**：桶号只用低位，`i << 32` 的 id 低 32 位全是 0，全部落进同一个桶，查找退化成线性扫描；自己提供混合哈希（splitmix64）。Java 的 `HashMap` 会把高位混进低位。
3. **编译器生成的移动构造函数**搬走 vector 但拷贝 `capacity_` / `next_index_` 这类标量：`OrderSequence b = std::move(a);` 后 `a` 声称下标空间是满的却没有存储，`a.put(1,1)` 越界写。手写移动构造，让被搬走的对象是合法的空序列（`capacity_ = 0`，第一次 `put` 触发压缩重新分配）。
4. **溢出检查放在 `compact()` 之后**：失败的 `put` 也触发压缩（失败的操作不应有任何可见副作用，包括 `compactions()` 和容量）。
5. **`std::bit_ceil` 参数太大**（结果超过 `unsigned` 范围）是 UB，先检查范围。
6. Fenwick 下标从 0 开始死循环；删除后下标被回收破坏插入顺序。
7. **`unordered_map` 删光后桶数组不自动缩小**：`erase` 不改桶数，只有 `rehash`（或销毁）才会缩；压缩里要 `rehash(new_cap)`，否则内存跟历史峰值走。
8. `k < 1` 的判断放在转 `size_t` 之后：负数变成巨大的无符号数，只是碰巧也被拒绝。
9. `catch (const std::exception&)` 把 `bad_alloc` 变成 `ERR`。
10. `std::unordered_map` 是节点式（每个元素一次分配，引用稳定），id 数量大时缓存不友好；扁平开放寻址表更快但要自己处理删除（墓碑 / 回移），哈希函数都要混合高位。
