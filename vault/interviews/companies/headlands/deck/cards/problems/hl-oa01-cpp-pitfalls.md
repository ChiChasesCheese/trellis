---
id: hl-oa01-cpp-pitfalls
node: problems.oa01-job-chain
type: qa
step: 17
---
## Q
用 C++ 写任务链报表时，有哪些未定义行为（UB）和边角陷阱？

## A
1. **`std::isspace(char)` 是 UB**：参数必须在 `unsigned char` 范围或为 `EOF`；`char` 通常有符号，字节 `0xE9` 变负数。先转 `unsigned char`，或自己写只认 ASCII 空白的 `is_space`。
2. **有符号整数溢出是 UB**：`total += runtime` 在两个 `LLONG_MAX` 相加时，编译器可以假设它不会发生。三种正确写法：`__builtin_add_overflow`（最好）、加之前预检查、拓宽到 `__int128`。无符号溢出才是定义良好的回绕。
3. **比较器必须是严格弱序**：`a.total >= b.total` 会让 `std::sort` 越界读（UB），要写 `>`；先比总时长降序，相等再比 `start_job` 升序。
4. **不要递归沿链走**：一条链可有 100 万个 job，每层一个栈帧，默认 8 MiB 栈撑不住；循环版 O(1) 栈。
5. **`unordered_map::operator[]` 会插入**：只查用 `find`，「没有才插入」用 `emplace(...).second`（查重复 id）。
6. 输入边角：Windows 换行 `\r\n`（`trim` 要吃掉 `\r`）、最后一行无换行、空输入、行内含 `\0`。
7. `ios::sync_with_stdio(false)` 加 `'\n'`（不用 `endl`）加速大输入输出。
