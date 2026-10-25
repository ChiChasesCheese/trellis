# hc08 · 思路与追问（C++20 版）

表面上是「前缀 count / quantity 查询」，面试官真正看的是三层：看到前缀和加在线修改能不能想到树状数组，删除只留洞时内存怎么回收，以及 C++ 里那一串容易踩的细节（`operator[]` 会插入、恒等哈希、被移走的对象、`from_chars` 的前缀行为）。一小时里要求会一路加，所以先写对朴素版，再换 Fenwick，再谈压缩，比一上来背 Fenwick 更稳。详细推导和可运行的示例在讲义 [[hc08_order_sequence_api_cpp]]。

## 30 秒版本

- **结构**：每张订单领一个只增不减的插入下标，删除只清零（留洞）；两棵 Fenwick 树，一棵数活跃订单，一棵累加剩余数量；`std::unordered_map` 从 id 找下标。
- **查询**：`count_up_to` / `qty_up_to` 是前缀和，`id_at(k)` 是活跃数那棵树上的二分下降，全部 O(log n)。
- **压缩**：下标写满时按原顺序重编号，新容量是 2 的幂且 ≥ `max(初始, 1.5m + 1)`，摊还 O(1)，并且要 `rehash` 让哈希表的桶数跟着缩小。
- **失败不留痕**：所有会抛异常的检查排在第一次修改之前，失败的 `put` 连压缩都不能触发。
- **C++ 的坑**：`find` 而不是 `operator[]`；自己混合高位的哈希；手写移动构造；`from_chars` 要检查结束指针；`apply` 不要 `catch (const std::exception&)`。

## Part 1 · 语义做对

**写法**：先用 `std::vector` 加线性扫描写出来（测试里的 `Model` 就是这样），同时定下所有边界：重复 id、`qty <= 0`、删除超量、未知 id、总量溢出，以及失败时状态不变。总量用 `__builtin_add_overflow` 检查，因为有符号溢出是 UB，加完再看已经晚了。

```cpp
long long new_total;
if (__builtin_add_overflow(total_qty_, qty, &new_total)) throw std::overflow_error("overflow");
```

文本接口：`parse` 用 `std::from_chars`，`apply` 用 `std::visit` 分发，`render` 把三种结果转成字符串。

**面试官在探什么**

1. **只检查总量为什么够**：所有数量都是正数，任何前缀和都不超过总量，所以守住 `total_qty_` 就保证每个前缀和都不溢出。
2. **失败时状态不变**：先做全部检查，再动数据。顺序反了，抛异常时树已经改了、map 还没改，之后的查询会悄悄给出错误答案。
3. **`from_chars` 的行为**：`"12abc"` 会成功返回 12，结束指针停在 `a`，所以必须检查结束指针等于 token 末尾；`"+1"` 会失败；`"0x10"` 只读到 `0`。这些都是格式错。
4. **`apply` 捕获哪些异常**：只捕获 `invalid_argument`、`UnknownId`、`out_of_range`、`overflow_error` 四种。捕获 `std::exception` 会把 `std::bad_alloc` 也变成一行 `ERR`，内存耗尽被悄悄吞掉。
5. **字符分类**：`std::toupper` 和 `std::isspace` 收到负数 `char` 是 UB，所以字节大于 127 时自己写 ASCII 判断，直接当格式错。

**该说出口的话**：「我先写一个线性扫描的版本把语义和边界定下来，所有会抛异常的检查放在第一次修改之前，这样失败的调用不留任何痕迹。」

## Part 2 · 树状数组

**写法**：下标从 1 开始，`tree[i]` 管区间 `(i - lowbit(i), i]`，其中 `lowbit(i) = i & -i`。

```cpp
for (; i <= capacity_; i += i & -i) tree[i] += delta;   // 更新：向上爬
for (; i > 0; i -= i & -i)          r += tree[i];       // 前缀和：向下走
// id_at(k)：从大步长到小步长，整块活跃数 < k 就整块跳过
for (int pw = capacity_; pw > 0; pw >>= 1)
    if (pos + pw <= capacity_ && cnt_[pos + pw] < rem) { pos += pw; rem -= cnt_[pos]; }
return id_by_idx_[pos + 1];
```

部分删除只改 `sum` 树，订单还活着，`cnt` 树不动；剩余为 0 才把 `cnt` 减 1 并从 map 里删掉。

**面试官在探什么**

1. **为什么用 Fenwick 不用线段树**：只需要单点修改加前缀和，加法有逆元；Fenwick 一个数组、循环里只有加法和位运算，常数小、十几行。要区间最值或区间修改才上线段树。
2. **为什么下标从 1 开始**：`0 & -0` 还是 0，`i += i & -i` 不前进，死循环。
3. **二分下降为什么要求容量是 2 的幂**：每一步的步长是 2 的幂，从 `capacity_` 开始往下减半，能正好覆盖整棵树。
4. **`operator[]` 查 id**：缺 key 时它会插入一个默认值，`size()` 变大，之后同一个 id 的 `put` 报 `duplicate id`。查询一律用 `find`。
5. **恒等哈希**：`std::hash<long long>` 返回自身，libc++ 在桶数是 2 的幂时只用低位。id 是 `i << 32` 时低 32 位全是 0，所有 key 落进同一个桶，每次查找退化成线性扫描。解法是自己带一个混合高位的哈希（splitmix64 的收尾步骤）。
6. **Part 2 的耗时**：朴素线性扫描在 50 万规模下不可行，Fenwick 版是毫秒到几百毫秒量级；这些具体数字以你本机 `perf` 测试的输出为准。
7. **中间插入做不到**：Fenwick 按插入下标建，只能追加。要在中间插，需要平衡树（order-statistic tree）或离线预分配下标。

**该说出口的话**：「前缀和加单点修改，我用两棵 Fenwick 树；删除只留洞，`id_at` 在计数树上做二分下降，全部 O(log n)。」

## Part 3 · 压缩

**写法**：`put` 发现 `next_index_ > capacity_` 时调用 `compact()`。

```cpp
const int m = static_cast<int>(index_of_.size());
const int new_cap = std::bit_ceil(static_cast<unsigned>(std::max(min_capacity_, m + m / 2 + 1)));
index_of_.rehash(new_cap);   // 桶数组跟着缩小
// 按原顺序把活跃订单写进 1..m，线性建树：每个节点把自己加到父节点 i + (i & -i)，最后换入新数组
```

**面试官在探什么**

1. **为什么新容量是 `1.5m + 1` 而不是 `m`**：只留 `m` 的话压缩完马上又满，每次 `put` 都压缩一遍，O(m)。`1.5m + 1` 至少腾出约 m/2 个空位，一次压缩 O(m) 摊到 m/2 次 `put` 上，每次 O(1)。活跃订单少时容量缩回去，但不低于初始容量。
2. **数字**：m = 1000 时 `1.5m + 1 = 1501`，向上取到 2 的幂是 2048。200 万次 put/remove、活跃恒为 1000 的循环里，`-O2` 下实测：容量稳定在 2048，压缩 1914 次，`index_buckets()` 是 2048。
3. **`unordered_map` 不会自己缩桶**：`erase` 不改桶数，只有 `rehash`（或销毁）才缩小。不 `rehash`，哈希表的内存就跟着历史峰值走，违背了「内存跟活跃量走」。
4. **失败的 `put` 不能触发压缩**：`qty`、重复 id、溢出三个检查都排在 `compact()` 之前。压缩本身不改变可观察行为，所以放在检查之后、插入之前是安全的。分配新数组放在最前面，最后的交换不会抛异常，压缩中途 `bad_alloc` 时旧结构完好。
5. **移动构造**：编译器生成的移动会搬走 vector，却照抄 `capacity_` 和 `next_index_` 这些整数，被移走的对象声称下标空间已满、存储却是空的，下一次 `put` 越界。手写：`std::exchange` 把整数归零，再清空容器，让它成为合法的空序列，第一次 `put` 时压缩出新的空间。
6. **`std::bit_ceil` 的 UB**：结果装不下 `unsigned` 时是 UB，所以构造函数先检查 `initial_capacity` 在 `[1, 2^29]` 内，再取整。2^29 + 1 抛 `invalid_argument`。
7. **压缩期间的停顿**：一次压缩是 O(容量)。要压低尾延迟，可以增量迁移，或者新旧两个结构交替；代价是复杂度。
8. **并发**：一把 `std::mutex` 最简单也正确；读多写少用 `std::shared_mutex`；或者单线程持有对象加命令队列。不能只靠线程安全的 map，两棵树加一张表的更新不是一个原子操作，查询会读到改了一半的状态。

**该说出口的话**：「下标写满时我按原顺序重编号，新容量取 `1.5m + 1` 以上的 2 的幂，所以摊还 O(1)；哈希表也要 `rehash`，否则内存还是跟着历史走。」

## 和 Java 版的区别

| 话题 | Java | C++ |
|---|---|---|
| 删除方法 | `delete` | 关键字，改名 `remove` |
| 异常 | `NoSuchElementException` 等 | `UnknownId`（自定义）、`out_of_range`、`overflow_error`、`invalid_argument` |
| 总量溢出 | `Math.addExact` | `__builtin_add_overflow`，有符号溢出是 UB |
| 取 2 的幂 | `Integer.highestOneBit(x - 1) << 1` | `std::bit_ceil`，结果装不下是 UB，先检查范围 |
| 查找 | `get` 返回 `null` | `find`；`operator[]` 会插入 |
| 哈希 | 会把高位混进低位 | `std::hash<long long>` 恒等，自己混合 |
| 内存回收 | GC | `unordered_map` 的桶数组要 `rehash` 才缩小 |
| 移动 | 引用，没有这个问题 | 手写移动构造，让被移走的对象合法 |
| 解析 | `Long.parseLong` 接受 `+5` | `from_chars` 拒绝 `+5`，且接受合法前缀，要检查结束指针 |
| 命令类型 | `sealed interface` + `record` | `std::variant` + 小结构体，`std::visit` |
| 异常处理范围 | `catch (A \| B \| C \| D)` | 四个 `catch`，不要 `catch (const std::exception&)` |
