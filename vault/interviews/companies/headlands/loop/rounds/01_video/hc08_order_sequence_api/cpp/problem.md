# hc08 · Order Sequence API（C++20 版）

交易系统里有一串按到达顺序排好的活跃订单。你要实现一个类，往末尾放订单、删订单，并且很快回答「从序列头数到订单 X，一共有几张订单、总数量是多少」。订单多、查询多，所以查询不能每次从头加一遍（O(n)），要做到 O(log n)。最后一问是内存：删除只留洞、下标只增不减，处理 200 万张订单时数组不能涨到 200 万。题目分 3 个 Part，类和签名都在 `starter.hpp`（命名空间 `oseq`）。

## 读题前你需要知道

- **前缀和**（prefix sum）：前 i 个数的和。每次查询都从头加一遍是 O(n)，数据量大时撑不住。
- **树状数组**（Fenwick tree / BIT）：一个数组，用 `i & -i`（最低位的 1）在 O(log n) 里完成「改一个数、求前缀和」。下标必须从 1 开始。
- **压缩**（compaction）：下标写满时，把活跃订单按原顺序重新编号，让内存跟活跃量走，而不是跟历史总量走。
- **C++ 里的错误映射**：`delete` 是关键字，所以方法叫 `remove`；Java 的几种异常对应 `std::invalid_argument`、`std::out_of_range`、`std::overflow_error`，再加 starter 给出的 `UnknownId`。

## 公共类型（starter 已给出）

```cpp
struct UnknownId : std::runtime_error { using std::runtime_error::runtime_error; };
struct Entry { long long id; long long qty; /* operator== */ };

struct Put { long long id; long long qty; };   struct Delete { long long id; long long qty; };
struct CountUpTo { long long id; };            struct QtyUpTo { long long id; };
struct IdAt { int k; };
using Op = std::variant<Put, Delete, CountUpTo, QtyUpTo, IdAt>;

struct Ok {};  struct Num { long long value; };  struct Err { std::string message; };
using Result = std::variant<Ok, Num, Err>;
```

错误信息是接口的一部分（`ERR` 后面跟的就是这些字符串）：`invalid quantity`、`duplicate id`、`unknown id`、`quantity exceeds remaining`、`index out of range`、`overflow`。

## 语义

- 订单是 `(id, qty)`：`id` 可以是任意 `long long`（0、负数、`LLONG_MIN` 都合法），同一时刻同一个 id 只能有一张活跃订单；`qty` 是正整数。
- 订单按**插入顺序**排列，不是按 id 排。删光之后同一个 id 可以再 `put`，它排到**最后**。
- 全体活跃订单的数量之和不能超过 `LLONG_MAX`。

## Part 1 · 语义做对（允许朴素实现）

| 签名 | 要求 |
|---|---|
| `void put(long long id, long long qty)` | 放到末尾。`qty <= 0` 或 id 已活跃抛 `std::invalid_argument`；总量会超过 `LLONG_MAX` 抛 `std::overflow_error`。失败时对象**完全不变** |
| `long long remove(long long id, long long qty)` | 从订单里删 `qty` 个单位，返回剩余数量，剩余为 0 时订单移除，位置不变。`qty <= 0` 或 `qty >` 剩余抛 `invalid_argument`；未知 id 抛 `UnknownId`。Part 1–2 只整单删除 |
| `long long count_up_to(long long id)` | 从头到该订单（含）的活跃订单数；未知 id 抛 `UnknownId` |
| `long long qty_up_to(long long id)` | 同一范围内剩余数量之和 |
| `long long id_at(int k)` | 第 k 张（从 1 数）活跃订单的 id；越界抛 `std::out_of_range` |
| `size()` · `total_qty()` · `entries()` | 活跃订单数、总量、按插入顺序排好的 `std::vector<Entry>` |

文本接口（同样在 Part 1）：

| 签名 | 要求 |
|---|---|
| `static Op parse(std::string_view)` | `PUT id qty` / `DELETE id qty` / `COUNT id` / `QTY id` / `AT k`；大小写不敏感，空白任意；格式错抛 `invalid_argument` |
| `Result apply(const Op&)` | 执行一条命令；`invalid_argument`、`UnknownId`、`out_of_range`、`overflow_error` 变成 `Err{message}`；其他异常（如 `std::bad_alloc`）继续向外传 |
| `static std::string render(const Result&)` | `Ok` → `OK`，`Num(v)` → `v`，`Err(m)` → `ERR m` |
| `static std::vector<std::string> replay(const std::vector<std::string>&)` | 跳过空行和 `#` 开头的行；格式错的行抛 `invalid_argument`，信息以 `line N`（从 1 数）开头 |

样例（`replay` 的输入和输出，输出每条一行）：

```text
# 样例              PUT 10 5       PUT 20 3       PUT 30 7       COUNT 30   QTY 20     DELETE 20 3
QTY 30     AT 2     (空行)         DELETE 10 5    put 20 4       QTY 20     DELETE 99 1
DELETE 30 9         PUT 30 1       AT 3           AT 2
```

输出依次为：`OK OK OK 3 8 0 12 30 0 OK 11`，然后 `ERR unknown id`、`ERR quantity exceeds remaining`、`ERR duplicate id`、`ERR index out of range`、`20`。

- 序列 `[10:5, 20:3, 30:7]` 上 `COUNT 30` 是 3，`QTY 20` 是 5+3=8；删掉 20 之后 `QTY 30` 是 12；删光 10、再 `put 20 4`，序列变成 `[30:7, 20:4]`，`QTY 20` 是 11。
- 前缀按插入顺序算：依次放入 id 10、5、7，数量 3、4、5，则 `qty_up_to(5) = 7`，`id_at(3) = 7`。
- 总量边界：先放 `LLONG_MAX - 10`，再放 11 抛 `overflow_error` 且大小不变；放 10 则总量恰好是 `LLONG_MAX`。
- `AT -2147483648` 能解析（是 `int` 范围内的数），执行结果是 `ERR index out of range`。

C++ 专属测试：

- 「C++ 专属测试：解析严格」：`from_chars` 会接受合法前缀，所以 `PUT 12abc 1`、`AT 3x`、`COUNT 1e3`、`AT 0x10` 都要拒绝；它不接受 `+`，所以 `PUT +1 2` 也是格式错；`COUNT 9223372036854775808`（`LLONG_MAX + 1`）和 `AT 2147483648` 超范围要拒绝；`PUT 007 0010` 按十进制得到 `Put{7, 10}`。
- 「C++ 专属测试：字符」：命令里有大于 127 的字节（`\xC3\xA9T 1 2`、`PUT \xFF 2`）或 NUL 字符要被拒绝，不能触发 UB；`"\tput\t1\t2\r\n"` 合法。
- 「C++ 专属测试：查询不插入」：对未知 id 调 `count_up_to` / `qty_up_to` / `remove` 抛 `UnknownId` 之后，`size()` 仍是 0，随后 `put` 同一个 id 不能报 `duplicate id`。
- 「C++ 专属测试：失败不留痕」：容量为 2、已放 `(1, LLONG_MAX - 10)` 和 `(2, 5)`、下标空间已满时，`put(3, 11)` 抛 `overflow_error`，`compactions()` 仍是 0，`capacity()` 仍是 2；重复 id 和 `qty = 0` 同理。
- 「C++ 专属测试：`int` 全范围」：`id_at` 对 `INT_MIN`、`-1`、`0`、`INT_MAX` 都抛 `out_of_range`。

## Part 2 · 亚线性查询

| 要求 | 内容 |
|---|---|
| 复杂度 | `count_up_to`、`qty_up_to`、`id_at`、`put`、`remove` 都是 O(log n) |
| 规模 | 50 万次 `put`，再 50 万次随机操作（删除或查询），2 秒内 |

`starter.hpp` 给的提示：每张订单领一个只增不减的插入下标 1..capacity，删除只把它清零（留洞）；两棵 Fenwick 树，一棵数活跃订单，一棵累加剩余数量；用 `std::unordered_map` 从 id 找下标（用 `find`，不要用 `operator[]`）。

- `id_at(k)` 在「活跃数」那棵树上做二分下降，要求容量是 2 的幂。
- 每个 n 从 1 到 70 都要对：大小不是 2 的幂、只剩头、只剩尾，是 Fenwick 最容易出错的地方。
- 40000 步随机操作和一个朴素 `vector` 模型对拍，每步 `size()` 一致。
- 「C++ 专属测试：哈希」：`std::hash<long long>` 是恒等函数，桶数为 2 的幂时只看低位；id 取 `i << 32` 的 20 万张订单要在 2 秒内放完并查完，`starter.hpp` 提示你自己带一个混合高位的哈希。

## Part 3 · 部分删除与压缩

| 签名 | 要求 |
|---|---|
| `explicit OrderSequence(int initial_capacity)` | 下标空间向上取整到 2 的幂（`std::bit_ceil`）；默认构造 = 16。`<= 0` 抛 `invalid_argument`；`INT_MAX`、`(1 << 29) + 1`、`INT_MIN` 也抛 `invalid_argument` |
| `remove(id, qty)` 部分删除 | `qty` 小于剩余量时只减量，订单和位置都还在，活跃数不变 |
| `int capacity()` | 当前下标空间大小，永远是 2 的幂 |
| `int compactions()` | 压缩次数 |
| `std::size_t index_buckets()` | id → 下标的 `unordered_map` 的桶数 |

- 下标写满（再 `put` 就没位置）时压缩：按原顺序给活跃订单重新编号。压缩后的容量是 2 的幂，且 ≥ `max(初始容量, 1.5m + 1)`（m 是活跃订单数）。压缩不改变任何可观察行为。
- 例：`OrderSequence s(8)` 放 1..8，删 1、3、5、7，再放 9：触发 1 次压缩，容量仍是 8，顺序 `2,4,6,8,9`。放 1..9（全活跃）则容量变成 16。
- 部分删除样例：`PUT 1 10`、`PUT 2 10`、`PUT 3 10`、`DELETE 2 4`、`QTY 3`、`COUNT 3`、`DELETE 2 6`、`COUNT 3`、`AT 2` 输出 `OK OK OK 6 26 3 0 2 3`。
- 压缩后容量要能缩回去：放 4000 张、删到只剩 10 张之后继续 put/remove，容量必须小于峰值的 1/4。
- 200 万次「put 一张、删最老的一张」（活跃订单恒为 1000），2 秒内，`capacity() <= 4096`，压缩超过 100 次，`index_buckets() <= 4 * capacity()`。
- 「C++ 专属测试：桶数」：10 万张订单删到剩 10 张后，反复 put/remove 触发压缩，`index_buckets()` 要降到峰值的 1/100 以下。`unordered_map` 自己不会缩小桶数组。
- 「C++ 专属测试：移动与拷贝」：被移走的对象必须是合法的空序列（`size() == 0`、`id_at(1)` 抛 `out_of_range`、可以再 `put`），且不影响目标对象；拷贝是深拷贝，互不影响。
- 「C++ 专属测试：总量到顶」：总量恰好 `LLONG_MAX` 是允许的；部分删除腾出的数量可以再被 `put` 用掉。

## 边界清单

- 空序列上的所有查询；重复 id；`qty <= 0`；删除超过剩余；已删除的 id 再查询
- id 取 `0`、负数、`LLONG_MIN`、`LLONG_MAX`
- 总量到 `LLONG_MAX`；失败的 `put` 既不改数据也不触发压缩
- Fenwick：大小不是 2 的幂、只剩头、只剩尾、洞全堆在前面（永远删最老的）
- 容量 1、2、4、3（取整到 4）这种极小空间下的压缩
- 文本：空白变体、`\r`、`+` 号、前缀合法的数字、超范围数字、非 ASCII 字节

## 怎么跑

在 kit 根目录（`interviews/companies/headlands/`）下：

```bash
python3 tools/cpptest.py start loop/rounds/01_video/hc08_order_sequence_api          # starter.hpp → work.hpp
python3 tools/cpptest.py run   loop/rounds/01_video/hc08_order_sequence_api --tag part1
python3 tools/cpptest.py run   loop/rounds/01_video/hc08_order_sequence_api --tag cpp      # 只跑 C++ 专属边界
python3 tools/cpptest.py run   loop/rounds/01_video/hc08_order_sequence_api                # 全部
```

编译带 `-fsanitize=address,undefined`，一触发 UB 就终止；带 `perf` 标签的测试另编一个不带 sanitizer 的 `-O2` 版本来跑。

## 相关变体

- 只要 `put / delete / count(id) / quantity(id)` 四个 API，没有 `id_at`；或把前缀改成后缀、某个价格区间（后缀 = 总量 − 前缀；价格区间要按离散化后的价格建树）。
- 「多个线程同时 put 和查询怎么办」：`std::mutex`，读多写少用 `std::shared_mutex`，或单线程持有加命令队列。
