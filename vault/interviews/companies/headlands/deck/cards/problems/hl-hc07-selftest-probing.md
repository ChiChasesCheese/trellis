---
id: hl-hc07-selftest-probing
node: problems.hc07-ticker-hash-map
type: qa
step: 20
---
## Q
练习：容量 8 的线性探测表，`A`（家 3）、`B`（家 3）、`C`（家 4）依次插入各住哪格？删除 `A` 后置空会怎样？`LongTickerMap` 用 `(int) key & mask` 会怎样？

## A
- `A` 住 3；`B` 家 3 被占 → 住 4；`C` 家 4 被占 → 住 5。
- 删除 `A` 若直接置空：查 `C` 从 4 开始（B 不是它）→ 5 找到，没出错；但查 `B`：家 3 → 空格 → **误判不存在**。放墓碑就不会。
- 线性探测 α = 0.75 时失败查找平均 `(1 + 1/(1−0.75)²)/2 = 8.5` 次，α = 0.5 时 2.5 次。线性探测有聚集，探测次数按 `1/(1−α)²` 增长；链地址法冲突只影响同一条链，α=1 时平均链长也只有 1。
- 把 `LongTickerMap` 哈希改成 `(int) key & mask`：`"AAPL"` 与 `"AAPM"` 只差第 4 个字段（比特 20–24），而 `& mask`（mask 通常 ≤ 2²⁰）只看低位，这两个 key 的低位全是 0，都落在下标 0 → 冲突；所有 ≤ 6 个字符的代码低 10 比特都是 0。
- `pack("AB ")` → `Invalid`（空格不是 A–Z）；`packWire("AB      ")` 合法，等于 `pack("AB")`（尾部空格是 wire 格式补位）。
- C++ 小题：`std::string_view("AB\0CD", 5)` 是 5 个字节（含 NUL），`std::string_view("AB\0CD")` 从 C 字符串构造，在第一个 NUL 截断，长度 2；`std::string_view` 里有 `'\0'` 或用 `const char*` 构造会截断。
- C++ 小题：`FixedTickerMap` 的移动构造函数不能 `= default`：默认的移动对 `size_`、`capacity_` 这类标量只是拷贝，被移走对象指针为空而计数还是旧值，之后访问会解引用空指针，要手写并清空源对象。
