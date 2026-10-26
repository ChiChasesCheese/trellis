# hc13 · 定长内存池

面试官让你实现一个池：启动时准备好 `capacity` 个等大的块，块用编号（index）表示，运行时只借和还，不再向系统要内存。Part 1 是最基本的借还，要求 O(1)，并且拒绝重复归还和越界编号。Part 2 是面试官的自然追问：块被还掉又被别人借走之后，旧的编号还在手里，怎么发现它已经过期。线程安全、对齐、为什么池比 `new` / `malloc` 快放在口头追问里。

## 面试官会怎么说

> "Implement a pool containing `capacity` equal-size blocks. Blocks are represented by indices. `allocate()` returns a free block index, or -1 when the pool is full. `release(i)` gives it back. Reject a double release and an out-of-range index."
> 接着会问："How do you find a free block in O(1)?" "What if someone releases a block, another caller gets the same index, and the first caller releases again?" "Is it thread safe?"

## 40 分钟怎么分

| 时间 | 做什么 |
|---|---|
| 0–3 分钟 | 复述题目，问清：池满时返回什么？重复归还是抛异常还是忽略？分配顺序有没有要求？ |
| 3–15 分钟 | **Part 1**：用数组串起空闲链表 |
| 15–30 分钟 | **Part 2**：带版本号的 handle |
| 30–40 分钟 | **Part 3**：口头追问，不写代码 |

## Part 1 · 空闲链表（约 12 分钟）

| 语言 | 签名 |
|---|---|
| Java | `new IndexPool(int capacity)` · `int allocate()` · `void release(int block)` |
| C++ | `pool::IndexPool(int capacity)` · `int allocate()` · `void release(int block)` |

- `allocate()` 返回空闲块的编号，池满返回 `-1`。`release` 把块放回去。两个操作都是 O(1)，不能为了找空闲块去扫数组。
- 初始依次分配 `0, 1, 2, …`；刚归还的块最先被再次分配（后进先出）。
- 越界编号：Java 抛 `IllegalArgumentException`，C++ 抛 `std::out_of_range`。重复归还（块当前不在用）：Java 抛 `IllegalStateException`，C++ 抛 `std::logic_error`。`capacity < 1`：Java 抛 `IllegalArgumentException`，C++ 抛 `std::invalid_argument`。
- 例子：`IndexPool(2)` 连续分配得到 `0, 1`，第三次得到 `-1`；`release(0)` 之后再分配得到 `0`；再 `release(0)` 两次，第二次抛异常。

## Part 2 · 带版本号的 handle（约 15 分钟）

| 语言 | 签名 |
|---|---|
| Java | `new GenPool(int capacity)` · `long allocate()` · `void release(long handle)` · `static int indexOf(long handle)` |
| C++ | `pool::GenPool(int capacity)` · `uint64_t allocate()` · `void release(uint64_t handle)` · `static uint32_t index_of(uint64_t handle)` |

- handle 是 64 位：高 32 位是版本号（generation），低 32 位是槽位下标，即 `handle = generation << 32 | index`。每个槽位有自己的版本号，初始为 0，每归还一次加 1。
- `allocate()` 池满返回 `-1L`（C++ 是 `GenPool::NONE`，64 位全 1）。
- `release(handle)`：下标越界抛「越界」异常（同 Part 1）；版本号和槽位当前版本号不一致，或者槽位根本不在用，抛「状态」异常（同 Part 1 的重复归还）。
- 例子：`GenPool(1)`，第一次分配得到 `0`；归还后再分配得到 `1L << 32`（同一槽位，版本号 1）；此时拿旧的 `0` 去归还要被拒绝，拿新的 `1L << 32` 归还成功。

## Part 3 · 口头追问（不写代码，答案在 solution.md）

1. 怎样让这个池线程安全？加锁和无锁的 Treiber 栈（Treiber stack）各有什么代价？
2. 无锁版本里的 ABA 问题是什么，版本号为什么能解决它？
3. 块的对齐（alignment）怎么保证？伪共享（false sharing）是什么？
4. 池为什么比每次 `new` / `malloc` 快？它自己又带来什么新问题？
5. 版本号只有 32 位，回绕了怎么办？
6. 池要存的是真正的对象而不只是编号，怎么做？

## 边界

- `capacity = 1`；池满再分配
- 编号 `-1`、`capacity`
- 同一个 handle 归还两次
- 归还后别人已经借走同一槽位，再用旧 handle 归还
- 低 32 位当 `int` 是负数的 handle（`-1L`）：不去掉符号扩展就会错

## 怎么跑

在 kit 根目录（`interviews/companies/headlands/`）下：

```bash
python3 tools/jtest.py start   loop/rounds/01_video/hc13_fixed_memory_pool       # Java：starter/ → work/
python3 tools/jtest.py run     loop/rounds/01_video/hc13_fixed_memory_pool --tag part1
python3 tools/cpptest.py start loop/rounds/01_video/hc13_fixed_memory_pool       # C++：cpp/starter.hpp → cpp/work.hpp
python3 tools/cpptest.py run   loop/rounds/01_video/hc13_fixed_memory_pool --tag part1
```
