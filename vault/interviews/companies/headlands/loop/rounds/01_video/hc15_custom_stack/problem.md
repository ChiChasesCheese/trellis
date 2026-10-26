# hc15 · 带批量加法的栈

面试官让你实现一个容量固定的栈，除了 push 和 pop，还有一个「给栈底的 k 个元素都加上同一个数」的操作。第一版直接用数组，加法循环 k 次就行；真正的考点是追问「加法能不能 O(1)」，答案是懒标记（lazy propagation）。后面的口头追问会问到溢出、区间加法的一般做法和线程安全。Java 和 C++ 的签名都在下面，选面试官要的那种语言。

## 面试官会怎么说

> "Maintain an initially empty stack that can hold at most maxSize integers. `push(x)` adds x on top unless the stack is full, in which case it does nothing. `pop()` removes and returns the top, or -1 if the stack is empty. `increment(k, val)` adds val to the bottom k elements of the stack, or to all of them if there are fewer than k."
> 接着会问："Can increment be O(1)?" "What if the values get large?" "What if you needed to add to an arbitrary range?"

## 40 分钟怎么分

| 时间 | 做什么 |
|---|---|
| 0–3 分钟 | 复述题目，问清：「栈底的 k 个」是最先 push 的 k 个吗？k 大于栈内元素数怎么办？值的范围多大？ |
| 3–15 分钟 | **Part 1**：数组版，increment 是 O(k) |
| 15–30 分钟 | **Part 2**：increment 改成 O(1)（懒标记） |
| 30–40 分钟 | **Part 3**：口头追问，不写代码 |

## Part 1 · 数组版（约 12 分钟）

| 语言 | 签名 |
|---|---|
| Java | `new CustomStack(int maxSize)` · `void push(long x)` · `long pop()` · `void increment(int k, long val)` |
| C++ | `CustomStack(int max_size)` · `void push(long long x)` · `long long pop()` · `void increment(int k, long long val)`（命名空间 `customstack`） |

- 栈满时 `push` 什么都不做；栈空时 `pop` 返回 `-1`。
- `increment(k, val)` 给最先进栈的 `min(k, size)` 个元素各加 `val`；`k = 0` 或空栈时什么都不做。
- 例子：容量 3，依次 push 2、3、4，再 push 5（被忽略），`increment(5, 100)` 得到 102 103 104，`increment(2, 100)` 得到 202 203 104；接着连续 pop 得到 104、203、202、-1。

## Part 2 · increment 改成 O(1)（约 15 分钟）

签名不变，只改内部实现：增加一个数组 `inc`，`inc[i]` 表示「还没加给栈里第 i 个元素的增量，同时它也属于 i 以下的所有元素」。

- `increment(k, val)`：只做 `inc[min(k, size) - 1] += val`。
- `pop()`：返回 `a[i] + inc[i]`，再把 `inc[i]` 加到 `inc[i - 1]` 上，并把 `inc[i]` 清零。
- 例子：push 1、2、3，`increment(3, 10)`，pop 得到 13；这时再 push 7，pop 必须得到 7（旧增量不能留在这个位置），再 pop 得到 12 和 11。
- 值要用 64 位：对同一个元素加三次 2000000000，结果是 6000000000，`int` 放不下。
- 10 万次 push、10 万次 `increment(100000, 1)`、10 万次 pop 要在 2 秒内跑完（O(k) 版要做 10^10 次加法）。

## Part 3 · 口头追问（不写代码，答案在 solution.md）

1. 懒标记为什么是对的？pop 的时候为什么要把增量下推？
2. 为什么 pop 之后要把 `inc[i]` 清零？
3. 值会溢出怎么办？为什么用 `long`？「栈空返回 -1」会有什么问题？
4. 如果要给任意区间 [l, r] 加一个数，怎么做？
5. 多线程同时调用，要怎么保证正确？

## 边界

- `maxSize = 1`，`k = 0`，`k` 大于栈内元素数，空栈上的 `increment`
- pop 到空之后再 push、再 increment
- 同一个位置先 pop 再 push（旧增量不能残留）

## 怎么跑

在 kit 根目录（`interviews/companies/headlands/`）下：

```bash
python3 tools/jtest.py start   loop/rounds/01_video/hc15_custom_stack       # Java：starter/ → work/
python3 tools/jtest.py run     loop/rounds/01_video/hc15_custom_stack --tag part1
python3 tools/cpptest.py start loop/rounds/01_video/hc15_custom_stack       # C++：cpp/starter.hpp → cpp/work.hpp
python3 tools/cpptest.py run   loop/rounds/01_video/hc15_custom_stack --tag part1
```
