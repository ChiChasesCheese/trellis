# oa01 · 思路与追问（C++20 版）

算法本身是 O(n) 的哈希加一遍遍历，分数在三件事上：校验清单有没有写全、输出格式是否逐字节正确、C++ 的未定义行为（UB）有没有被你踩到。电面也可能从 OA 延伸追问「环怎么处理、百万行多快」。详细推导和可运行的示例在讲义 [[oa01_job_chain_cpp]]。

## 30 秒版本

- **解析**：`std::from_chars`，检查结束指针；不用 `stoi`，因为 `"12abc"` 它也返回 12。字符判断自己写 ASCII，不用 `std::isspace(char)`。
- **校验分两层**：单行规则放进 `validate(const Job&)`，`parse` 和 `chains` 都调用它；跨行规则（重复、悬空、多前驱、环）在 `chains` 里。
- **拼链**：入度 ≤ 1，从所有没有前驱的节点往下走；走完后没被访问到的节点只可能在环上，一次计数比较就查出环，不用 DFS 染色。
- **溢出**：累加总时长用 `__builtin_add_overflow`，溢出当作 `Malformed`。
- **输出**：`std::variant<Ok, Malformed>` 加 `std::visit`；`Malformed Input` 也以状态 0 退出。
- **排序**：比较器是严格弱序，总时长降序，`start_job` 升序。

## Part 1 · 解析与格式化

**写法**：把一行按逗号切成恰好三段，每段 `trim` 之后用 `from_chars` 解析，最后调 `validate`。

```cpp
auto [ptr, ec] = std::from_chars(first, last, v);
if (ec == std::errc::result_out_of_range) throw MalformedInput("number out of range");
if (ec != std::errc{} || ptr != last)     throw MalformedInput("bad number");
```

`hhmmss` 先判负数，再用 `seconds / 3600`、`seconds / 60 % 60`、`seconds % 60` 三段格式化，小时用 `%02lld` 所以不会被截断。

**面试官在探什么**

1. **为什么不用 `stoi`**：它只要前缀是数字就成功（`"12abc"` → 12，`" 7"` → 7，`"+5"` → 5），错误被悄悄吞掉。`from_chars` 不跳空白、不收 `+`，并通过指针告诉你停在哪里，所以「整个 token 是不是一个整数」可以精确判断。`atoi` 连错误都不报告。
2. **`std::isspace(char)` 为什么是 UB**：参数必须在 `unsigned char` 范围内或为 `EOF`，`char` 通常有符号，字节 `0xE9` 会变成负数。解法是自己写 `is_space`，只认 ASCII 空白，大于 127 的字节一律当格式错。
3. **`Job` 是聚合体，没有紧凑构造器**：Java 里非法对象构造不出来，C++ 里 `Job{0,5,0}` 可以直接写出来。所以规则放进 `validate`，`parse` 和 `chains` 两个入口都调用。
4. **负号为什么在解析时不拒绝**：先让数字解析成功，再由 `validate` 报「负数」，错误信息比「格式错」更准。
5. **`hhmmss(LLONG_MIN)`**：先判 `seconds < 0` 再运算，取相反数会是有符号溢出。`hhmmss(LLONG_MAX)` 的结果是 `2562047788015215:30:07`。

**该说出口的话**：「解析我用 `from_chars` 并检查结束指针，不用 `stoi`；单行规则收在 `validate`，两个入口都调它。」

## Part 2 · 拼链与跨行校验

**写法**：三遍扫描，全部 O(n)。

1. 建 `unordered_map<int, size_t>`（id → 下标），用 `emplace(...).second` 查重复 id。
2. 对每个 `next_id != 0` 的 job：用 `find` 查目标（找不到就是悬空），再检查目标是否已有前驱（有就是多前驱），记下 `next[i]`。
3. 从每个没有前驱的节点循环往下走，累加个数和总时长，同时数一共访问了多少个节点；最后访问数不等于 n，说明有节点在环上。

最后用 `std::ranges::sort` 排序，比较器是 `total != total ? a.total > b.total : a.start < b.start`。

**面试官在探什么**

1. **为什么没访问到的节点一定在环上**：每个节点入度 ≤ 1，不在任何链头的路径上，只可能是某个环的一部分。「好链 + 独立环」是隐藏用例最爱打的点：只从链尾往回走的解法查不出它。
2. **为什么不用递归**：一条链可以有 100 万个 job，递归每层一个栈帧，默认栈撑不住，栈溢出是信号、`catch` 接不住。循环版栈空间 O(1)。
3. **`operator[]` 的陷阱**：只想查就用 `find`；`unordered_map::operator[]` 缺 key 时会插入。查重复用 `emplace(...).second`。
4. **溢出**：总时长累加用 `__builtin_add_overflow`，因为有符号溢出是 UB，编译器可能把加完再判断的代码整个优化掉。溢出时抛 `MalformedInput`。总时长恰好等于 `LLONG_MAX` 是合法的。
5. **`vector<bool>`**：它是按位压缩的特化，`operator[]` 返回代理对象。需要一排标志位时用 `vector<char>`（`has_predecessor`）。
6. **比较器必须是严格弱序**：`a.total >= b.total` 这种带等号的写法会让 `std::sort` 越界读，是 UB。
7. **平均数**：整数除法向零截断，总时长 ≥ 0、个数 ≥ 1，所以 35 / 2 = 17，不需要手工取整。
8. **`unordered_map` 的最坏情况**：`int` 的标准库哈希是恒等映射，所有 key 落进同一个桶时退化为 O(n)。能说出「期望 O(1)，最坏 O(n)，可以换成排序加二分得到确定的 O(n log n)」就够了。

**该说出口的话**：「入度不超过 1，所以我从所有链头往下走，走完还有没访问的节点就一定在环上，一次计数就够，不用 DFS。」

## Part 3 · 整题与 stdin → stdout

**写法**：`analyze` 里 `try { return Ok{chains(parse(lines))}; } catch (const MalformedInput& e) { return Malformed{e.what()}; }`。`render` 用 `std::visit` 配一组 `overloaded` 的 lambda，`Malformed` 返回 `{"Malformed Input"}`，`Ok` 返回每条链六行。`run` 用 `std::getline` 逐行读，逐行输出，返回 0。

**面试官在探什么**

1. **为什么用异常而不是返回值**：校验分布在多层，异常让中间层不必层层透传，在 `analyze` 这一个边界上转成值。非法行是少数情况；如果坏行是常态（每秒百万行里很多坏行），异常每次几微秒，改用 `std::optional`、`std::variant<Job, Error>` 或 C++23 的 `std::expected`。
2. **`std::variant` 的好处**：`std::visit` 要求每种情况都有分支，新增第三种结果时 `render` 编译不过。
3. **只 catch `MalformedInput`**：不要写成 `catch (...)`，否则 `std::bad_alloc` 也会被当成「输入格式错」。
4. **输入的边角**：`\r\n`（所以 `trim` 要吃掉 `\r`）、最后一行没有换行、完全空的输入（输出一行 `-`）、行内的 NUL。
5. **退出状态**：题面要求 `Malformed Input` 也以状态 0 退出，所以 `main` 返回 `run(...)` 的结果，永远是 0。
6. **百万行的开销**：`unordered_map` 每个节点一次堆分配，是最大的开销。更快的做法是先排序去重得到稠密下标，用 `vector` 加二分，或开放寻址哈希表。时间是 O(n) 期望加最后的 O(c log c) 排序（c 是链数）。
7. **能不能边读边处理**：解析可以流式做，但拼链要知道全部 job 才能判断悬空、多前驱、环，所以 job 要存，省掉的只是原始字符串。

**该说出口的话**：「内部一律抛异常，在 `analyze` 这一个边界上转成 `Malformed` 值，渲染用 `std::visit`，进程不管输入好坏都以 0 退出。」

## 和 Java 版的区别

| 话题 | Java | C++ |
|---|---|---|
| 单行校验 | record 紧凑构造器，非法对象构造不出来 | 聚合体，没有构造器；`validate` 在每个入口调用 |
| 整数解析 | 正则加 `Integer.parseInt`，溢出抛 `NumberFormatException` | `from_chars`，检查结束指针和 `result_out_of_range`；不收 `+` |
| 总时长溢出 | `Math.addExact` 抛异常 | `__builtin_add_overflow`，有符号溢出是 UB |
| 结果类型 | `sealed interface` + `record`，模式匹配 `switch` | `std::variant` + `std::visit` |
| 字符分类 | Unicode | 自己写 ASCII 判断，`std::isspace(char)` 传负数是 UB |
| 排序 | `Comparator` 组合子 | 手写比较器，必须是严格弱序 |
| 标志数组 | `boolean[]` | `vector<char>`，`vector<bool>` 是位压缩特化 |
| 长链 | 栈溢出是 `StackOverflowError` | 栈溢出是信号，进程直接死掉；用循环 |
| 入口 | `Main` 读 `System.in` | `main.cpp` 调 `run(std::cin, std::cout)`，返回 0 |
