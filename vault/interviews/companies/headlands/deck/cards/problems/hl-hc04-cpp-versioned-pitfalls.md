---
id: hl-hc04-cpp-versioned-pitfalls
node: problems.hc04-queue-mean-snapshot
type: qa
step: 20
---
## Q
C++ 版持久化队列和均值实现有哪些容易踩的陷阱？

## A
1. **`Version v = at(version);` 按值拷贝，而不是 `const Version& v = at(version);`**：`new_version` 里的 `versions_.push_back` 可能重新分配，旧引用悬空；按值拷贝只有 32 字节。更一般：`push_back` 之后继续用旧引用 / 迭代器是 UB。
2. **默认的移动构造函数**对 `int / size_t / __int128` 成员只是拷贝，移动后源对象 `buf_` 为空但 `size_` 还是旧值。
3. **`-x`、`std::abs(x)` 对 `LLONG_MIN` 是 UB**；用无符号类型取绝对值。
4. **`(double)sum / n` 对大和舍入两次**；用「粘滞位」处理平局：被丢弃的位全 0 才是平局（取偶），略大于一半必须进位。
5. **环形缓冲扩容直接复制整个数组**：`head` 不在 0 时顺序错乱。容量 8、`head=5`、`size=5` 扩到 16：先复制 `[head, 容量)`（3 个）再复制 `[0, head)`（2 个），新 `head=0`。
6. **读者读普通变量**：数据竞争，UB。
7. 为什么 running sum 用 `__int128` 不用 `long double`：`long double` 宽度因平台而异，尾数最多 64 位，装不下 2¹²⁷ 范围的精确和。
8. `std::vector<bool>`、`std::map::operator[]` 这类「看起来像普通容器」的坑，面试会问。
