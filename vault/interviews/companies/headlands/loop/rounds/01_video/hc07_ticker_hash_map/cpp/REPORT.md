# hc07 · 思路与追问（C++20 版）

「为股票代码优化哈希表」的起点是 `std::unordered_map<std::string, long long>`。面试官看四件事：你能不能自己写对一个哈希表（冲突、删除、扩容）；能不能说出通用方案的代价（每个条目一个节点、指针追逐）；能不能利用 key 的结构（至多 8 个大写字母，正好放进一个 `uint64_t`）；以及你怎么测量。下面按 Part 写清怎么写、面试官在探什么、该说出口的话。逐行的实现和可运行的示例在讲义 [[hc07_ticker_hash_map_cpp]]。

## 30 秒版本

- **Part 1**：一个 `std::vector<Slot>`，每个槽是 `Empty / Full / Tomb` 三态；容量取 2 的幂，下标取乘法哈希的高位；删除只留墓碑，装载因子把墓碑算进去，rehash 时清掉。
- **Part 2**：每个字母 5 比特，8 个字母占低 40 比特，key 恒 `> 0`；`0` 当空格、`~0` 当墓碑；哈希不能是 `key & mask`。
- **Part 3**：key 集合固定就用 hash-and-displace 做最小完美哈希；`index_of` 末尾必须比较存下的 key；下标可以缓存，`add_at` 完全不做哈希。
- **Part 4**：一次对齐分配、定长、不增长；移动构造函数手写，把源对象清空；`close()` 幂等。
- **C++ 的雷**：`int` 移位 35 位、`char` 有符号、`off + 8` 回绕、`-1` 转成 `uint64_t` 变成墓碑标记、`std::vector<bool>`、默认移动不清空标量。
- **测量**：同一串更新、预热、多轮取最好、访问序列放在计时外、`-O2` 不开 sanitizer；说清楚哪些没测。

## Part 1 · 手写哈希表

**写法**

```cpp
Probe locate(std::string_view key) const {
    std::size_t i = home(key);
    std::optional<std::size_t> first_tomb;
    for (;;) {
        const Slot& s = slots_[i];
        if (s.state == State::Empty) return {first_tomb.value_or(i), false};
        if (s.state == State::Tomb) { if (!first_tomb) first_tomb = i; }
        else if (s.key == key) return {i, true};
        i = (i + 1) & mask_;
    }
}
```

- 下标 `home(key) = (hash * GOLDEN) >> shift`，容量是 2 的幂，`shift = 64 - countr_zero(cap)`：乘一个奇数常数再取高位（Fibonacci hashing），所以即使 `Hash` 很差也只是变慢，不会错。
- 插入用 `locate` 返回的位置：有墓碑就复用第一个墓碑，否则占空格；占空格之前检查 `(size + tombs + 1) * 2 > cap`（题目只要求不超过 3/4，取 1/2 更保守，探测更短），超了就 rehash，新容量取活条目数的 4 倍向上取 2 的幂，墓碑消失。
- 删除：`state = Tomb`，同时清掉 key。
- `add` 先算 `add_checked(old, delta)`，再把结果写回去，所以溢出时表没动。

**面试官在探什么**

1. **删除为什么不能置空**：被冲突挤到后面的 key，查找时从家出发会先碰到这个空格，误判不存在。墓碑让探测继续往后走。
2. **墓碑要算进装载因子**：只算活条目的话，反复「插新 key、删旧 key」会把所有空格都变成墓碑，查找一个不存在的 key 就永远找不到终点。测试里的 30 万次 churn 正是在抓这一点，同时要求 `capacity() <= 1024`。
3. **遇到墓碑就插入**：会造成重复 key，因为后面可能还有同一个 key。要走完整条探测链，记下第一个墓碑，再决定是更新还是插入。
4. **复用墓碑要把它从计数里扣掉**：反复 `remove` + `put` 同一个 key 之后 `tombstones()` 必须回到 0，容量不变。
5. **哈希值全相同的 key**：测试用 1024 个 `"Aa"` / `"BB"` 拼出来的 key 配一个永远返回 42 的 `Hash`。正确性不依赖哈希质量，只有速度依赖。
6. **`std::string_view` 和 SSO**：查找参数用 `std::string_view`，传字符串字面量不会临时构造 `std::string`；key 不超过 SSO 上限时，槽位里的 `std::string` 不分配。测试用重载的全局 `operator new` 计数来验证零分配。
7. **NUL**：`std::string_view("AB\0CD", 5)` 是 5 字节的 key，和 `"AB"` 不同。用 C 字符串当参数会在 NUL 处截断。
8. **为什么 `std::unordered_map` 慢**：每个条目一个堆节点，桶数组里存指针，查找要两次间接寻址；元素的引用保持稳定，这是它换来的好处。优化方向是换成扁平的开放寻址表。
9. **开放寻址 vs 链地址**：开放寻址连续内存、缓存友好、没有逐条目分配，但装载因子要低、要处理墓碑、对哈希质量敏感；链地址实现和删除简单，能容忍高装载因子，引用稳定，代价是指针追逐。读多写少、key 小、要低延迟，选开放寻址。
10. **容量为什么是 2 的幂、为什么翻倍**：`&` 代替取模（除法很贵）；翻倍使总搬运量小于 2n，摊还 O(1)。

**该说出口的话**：「开放寻址加线性探测，删除用墓碑而且墓碑算进装载因子，rehash 时清掉；这样 churn 下容量有界，探测永远能碰到空格。」

## Part 2 · 打包成 `uint64_t` + `LongTickerMap`

**写法**

```cpp
const auto c = static_cast<unsigned char>(s[i]);          // char 可能有符号
if (c < 'A' || c > 'Z') return Invalid{Error::BadChar, i};
key |= static_cast<Key>(c - 'A' + 1) << (5 * (7 - i));    // 先转宽，再移位
```

`pack_wire`：用 `memcpy` 把 8 个字节读进一个 `uint64_t`，小端机器上 `__builtin_bswap64` 把第 0 个字节放到最高位；每个字节要么是大写字母，要么是空格（空格之后不能再有字母），取低 5 位拼起来。偏移检查写成 `buf.size() < 8 || off > buf.size() - 8`。

`LongTickerMap`：槽位是 16 字节的 `{Key key; long long value}`，一个 `std::vector<Slot>`；`Key == 0` 是空格，`~0` 是墓碑，所以合法 key 必须严格落在两者之间；下标 `(key * GOLDEN) >> shift`。

**面试官在探什么**

1. **为什么每个字母 5 比特**：26 个字母加一个补位 0，需要 5 比特；8 × 5 = 40 比特，放得进 `uint64_t`，key 恒 `> 0`（不是空串）所以 0 可以当空格。
2. **`key & mask` 为什么是灾难**：`std::hash<uint64_t>` 是恒等函数，`& mask` 只留低位；不足 8 个字符的代码，低位全是补的 0，几乎所有短代码落同一格。乘 `GOLDEN` 再取高位，让每一位输入都影响高位。测试用 17576 个三字母代码检查 `max_probe_length() <= 64`，同时也用随机代码。
3. **`(c - 'A' + 1) << 35`**：`c - 'A' + 1` 是 `int`，把 `int` 左移 35 位是未定义行为。先 `static_cast<Key>` 再移位。
4. **`char` 的符号**：字节 `0xC3` 在有符号 `char` 里是负数，只检查上界 `c > 'Z'` 会放过它；先转 `unsigned char` 再比较。别把负数传给 `isalpha` / `toupper`。
5. **`-1` 变成墓碑**：`static_cast<Key>(-1)` 是 `0xFFFF…FFFF`，正好是 `TOMB`。测试要求 `put` 它时抛 `std::invalid_argument`，不能把它当成合法 key 存进去，更不能和墓碑混淆。
6. **`off + 8` 回绕**：`off` 接近 `SIZE_MAX` 时 `off + 8 > size` 为假，随后就越界读。先保证 `size >= 8`，再写 `off > size - 8`。
7. **稳态零分配**：`add` / `get` 只在已分配好的 `std::vector` 里读写，没有 `std::string`，没有节点。测试用重载的 `operator new` 计数验证：8000 个 key 预留好之后 160 万次 `add` 零次分配，一个扁平表从头到尾只分配一次，而 `std::unordered_map` 至少每个条目一次。
8. **交错布局**：key 和 value 放在同一个 16 字节槽里，一个 64 字节缓存行装 4 个槽，找到 key 就拿到 value；分离成两个数组要读两条缓存行。这个结论要用数据支持，下面「测量」一节会说明。
9. **溢出**：有符号溢出是 UB，`add_checked` 用 `__builtin_add_overflow` 判断，先算后写。

**该说出口的话**：「key 打包成 `uint64_t`，0 和全 1 留给空格和墓碑；哈希用乘法取高位，因为打包后的低位是零；这样热路径里没有分配，也不比较字符串。」

## Part 3 · 完美哈希

**写法**（hash-and-displace，CHD 的简化）

1. 用 `splitmix64` 之类的混合函数对每个 key 求哈希，分成大约 n/4 个桶（计数排序）。
2. 桶按大小从大到小处理：对每个桶找位移 `d`，让桶里每个 key 的候选槽 `slot(hash, d)` 都空着且互不相同；找到就占用，没找到就试下一个 `d`。
3. 只有一个 key 的桶最后处理：直接取下一个空槽，把 `~slot` 存进位移表。
4. 一个种子试遍所有位移仍失败，就换种子重来。
5. `index_of`：算桶号，读位移，算槽号，**最后比较 `keys_[slot] == key`**。

`FrozenTickerMap` = `SymbolIndex` + 一个 `std::vector<long long>`；`add_at(index, delta)` 直接按下标累加，不做哈希。

**面试官在探什么**

1. **为什么最后要比较 key**：完美哈希只保证集合内的 key 互不冲突；集合外的 key 也会被映射到某个槽。不比较就会把它误认成那个槽里的 key。
2. **为什么大桶先放**：大桶最难找到全空的候选槽，趁空槽多时先放；单 key 桶什么位置都行，留到最后。
3. **哈希族怎么选**：用 `h + d * c` 这种等差候选，在小表上可能永远放不进去；把 `d` 混进哈希里，候选才表现得彼此独立。
4. **`std::vector<bool>`**：它是按位压缩的代理容器，`used[s]` 返回的不是 `bool&`。标志数组用 `std::vector<std::uint8_t>`。
5. **完美哈希一定更快吗**：不一定。单次 `add(key)` 要碰三块内存（位移表、`keys_`、`values_`），调好的开放寻址只碰一个 16 字节槽。完美哈希的收益是：最坏情况确定、内存紧凑（每条目约 17 字节，没有空槽）、可以缓存下标。
6. **越界下标**：`add_at(-1, …)` 和 `add_at(size, …)` 抛 `std::out_of_range`；用 `at()` 或自己检查，`operator[]` 越界是 UB。
7. **默认值**：在集合里但还没写过的 key 值是 0，不是不存在。`put` 一个集合外的 key 返回 `false`，`add` 则抛 `std::invalid_argument`，因为静默忽略一条成交会丢数据。

**该说出口的话**：「key 集合开盘前就知道，所以做最小完美哈希，把 key 变成 0..n-1 的下标；集合外的 key 也会落在某个槽，所以 `index_of` 必须比较原始 key；订阅时缓存下标，之后每条消息不再哈希。」

## Part 4 · 定长对齐内存

**写法**

```cpp
const std::size_t bytes = capacity_ * sizeof(Slot);
void* raw = ::operator new(bytes, std::align_val_t{64});
std::memset(raw, 0, bytes);                         // key == 0 表示空格
slots_.reset(static_cast<Slot*>(raw));              // unique_ptr 带一个调用对齐版 delete 的删除器
```

- 槽位数 `std::bit_ceil(std::max<std::size_t>(8, 2 * max_entries))`，装载因子不超过 1/2。
- 新 key 先检查 `size_ == max_entries_`，满了抛 `std::length_error`；已有 key 照常更新。
- 移动构造函数手写，用 `std::exchange` 把源对象的指针和所有计数清成 0。

**面试官在探什么**

1. **为什么移动构造函数不能 `= default`**：默认的移动对 `size_`、`capacity_` 这类标量只是拷贝，源对象指针被清空而计数还是旧值，之后访问会解引用空指针。手写并把源对象清成空状态；测试要求 `a.size() == 0`、访问抛 `std::logic_error`。
2. **对齐的用处**：16 字节的槽位对齐后不会跨缓存行，一次探测只触碰一条缓存行；多线程时，把不同线程写的数据放到不同缓存行，避免 false sharing。
3. **对齐分配要配对**：`operator new(size, align_val_t)` 必须用 `operator delete(ptr, align_val_t)`。和普通 `delete` 混用是 UB。
4. **没有 GC，堆外是什么意思**：Java 里堆外是为了躲开 GC；C++ 没有这个问题，剩下的是对齐、定长、地址不变、对象生命周期。
5. **线程**：对象没有线程亲和性，`join` 建立了 happens-before，所以另一个线程写、主线程读是安全的。同时读写同一张表需要自己加同步；每个线程一张表最后合并，或者对固定数组的元素用 `std::atomic_ref<long long>`。
6. **满了怎么办**：定长表不增长，满了拒绝新 key，是为了地址和延迟可预期；容量要在构造时按 `max_entries` 定好。
7. **`close()`**：幂等，释放之后任何访问都抛异常，而不是读到悬空内存。

**该说出口的话**：「一次对齐分配，槽位 16 字节，64 字节对齐，容量定死不增长；对象只能移动，移动之后源对象必须是空的。」

## 你怎么知道更快：测量

**做法**：同一串更新喂给每种实现；预热一轮；多轮取最好；访问序列预先生成，不放进计时循环；`-O2`，不开 sanitizer；输出每次操作的纳秒数。

**实测**（clang，`-O2`，这台 Mac，均匀随机访问，每轮 2000 万次更新，5 轮取最好，只跑了一次，数字有抖动）：

| 实现（ns/op） | 8,000 个代码 | 2,000,000 个代码 |
|---|---|---|
| `std::unordered_map<std::string, long long>` | 20.5 | 102.5 |
| `TickerMap`（字符串 key，扁平开放寻址） | 18.0 | 55.5 |
| `LongTickerMap`（打包成 `uint64_t`） | 5.3 | 15.9 |
| `FrozenTickerMap::add(key)` | 3.5 | 27.6 |
| `FrozenTickerMap::add_at(index)` | 1.0 | 5.9 |

**怎么读**

- **打包成整数是实打实的胜利**：8000 个代码时约快 4 倍，200 万个时约快 6 倍。表大了以后缓存未命中占主导，16 字节的扁平槽位和不比较字符串的优势更明显。
- **只把节点式换成扁平数组、key 仍是字符串**：小表上差别不大（短字符串比较便宜），大表上约快 2 倍。
- **完美哈希的单次 `add(key)` 不一定比调好的开放寻址快**：小表上更快，200 万个 key 时反而更慢。真正的收益是确定性、紧凑、可缓存下标（`add_at` 比开放寻址快数倍）。
- **没测**：多线程、偏斜访问（热门代码占大头）、真实行情分布、尾延迟、其他 CPU 和编译器、冷启动。这些结论不能外推到它们。
- 装载因子会直接改变 ns/op，所以对比两种布局或两种实现时，要把装载因子固定住再比。

**该说出口的话**：「我把同一串更新喂给每种实现，预热后多轮取最好，访问序列在计时外生成；打包 key 的收益在数据上站得住，完美哈希单次更新不一定更快，它的价值在可缓存下标；多线程和真实分布我没测。」

## C++ 专属陷阱

每条的格式是「错误写法 → 后果 → 改法」。

1. **下标取 `hash & mask`** → libc++ 的 `std::hash<整数>` 是恒等函数，打包后的 key 低位全是 0，所有 key 落到同几个槽，探测退化成 O(n) → 乘法哈希（Fibonacci hashing）后取**高位**。
2. **墓碑的三种错法**：
   - 删除时把格子直接置空 → 探测链断掉，后面的 key 查不到了。
   - 还没确认 key 不存在，就插进路上遇到的第一个墓碑 → 同一个 key 出现两份。
   - 装载因子只算活条目 → 反复插入、删除之后，表里没有空格，查找不存在的 key 会死循环。
   - 改法：查到空格才算「不存在」，再回头复用第一个墓碑；墓碑计入装载因子，rehash 时清掉。
3. **`(c - 'A' + 1) << 35`** → 这里的移位是在 `int` 上做的，移 35 位超过了位宽，是 UB → 先转成 `std::uint64_t` 再移位。
4. **`char` 有符号** → 字节 `0xC3` 是负数，只检查上界 `c <= 'Z'` 会放过它；`isalpha` / `toupper` 传负数是 UB → 先转成 `unsigned char`。
5. **用 `const char*` 构造 `std::string_view`** → 在第一个 `'\0'` 处截断，`"AB\0C"` 变成 `"AB"`，和别的 key 撞上 → 用带长度的构造函数，并且拒绝含 `'\0'` 的 key。
6. **边界检查写成 `off + 8 > size`** → `off` 接近 `SIZE_MAX` 时加法回绕，检查通过，然后越界读 → 写成 `off > size || size - off < 8`。
7. **`put(-1, v)`** → `-1` 隐式转换成 `0xFFFF…FFFF`，正好是墓碑标记，这个条目会被当成已删除 → 在入口拒绝哨兵值。
8. **`SymbolIndex::index_of` 不比较原始 key** → 完美哈希对集合外的 key 也会算出一个合法的下标，于是集合外的 key 被当成集合内的某个 → 每个槽保存原始 key，查到后比一次。
9. **用 `std::vector<bool>` 当标志数组** → 它是按位压缩的代理对象，取不到元素地址，逐位访问慢；两个线程写相邻的位是数据竞争 → 用 `std::vector<std::uint8_t>`。
10. **用编译器生成的移动构造函数** → 它不会把源对象的指针、大小这类标量清零，源对象析构时再释放一次，就是 double free → 自己写移动构造函数，用 `std::exchange` 把源对象置空。
11. **对齐分配配普通 `delete`** → `operator new(size, std::align_val_t)` 必须配对应的对齐版 `operator delete`，混用是 UB，可能弄坏堆 → 用带自定义删除器的 `std::unique_ptr` 把分配和释放绑在一起。
12. **`add` 先改表再检查溢出** → 溢出抛异常时表已经被改了一半，强异常保证（strong exception guarantee）被破坏 → 先用 `__builtin_add_overflow` 算出新值，确认不溢出后再写入。

## 和 Java 版的区别

| 话题 | Java | C++ |
|---|---|---|
| key 类型 | `String` / `long`（有符号，`> 0` 才合法） | `std::string_view` / `uint64_t`（`0` 空、`~0` 墓碑；`-1` 的隐式转换是陷阱） |
| 链地址的代价 | `HashMap` 每条目一个对象加装箱 | `std::unordered_map` 每条目一个节点；短字符串有 SSO 不分配，主要代价是指针追逐 |
| 溢出 | `Math.addExact` | `__builtin_add_overflow`，有符号溢出是 UB，不能事后检查 |
| 位运算 | `Long.compress`、`Integer.numberOfTrailingZeros` | `std::countr_zero`、`std::bit_ceil`（`<bit>`）；字节序用 `std::endian` |
| 字节缓冲 | `VarHandle` 读 `byte[]` | `memcpy` 进 `uint64_t` 再 `bswap` |
| 越界 | 一律抛 `IndexOutOfBoundsException` | `operator[]` 是 UB，`at()` 才检查；偏移量计算要防回绕 |
| 分配统计 | `ThreadMXBean.getThreadAllocatedBytes` | 重载全局 `operator new` 计数 |
| 堆外 | `Arena` / `MemorySegment`，为了躲 GC | 没有 GC；剩下对齐、定长、地址不变、对象生命周期 |
| 失败 | 异常 | 异常；热路径也可以返回 `std::optional` / 错误码 |
