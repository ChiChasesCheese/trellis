---
id: hl-c09-ub-list
node: cpp-lessons.c09-ub-sanitizers
type: qa
step: 3
---
## Q
列出 C++ 中常见的未定义行为，并说明 Java 里对应的行为。

## A
- **有符号整数溢出**（`INT_MAX + 1`）：Java 回绕。
- **越界访问**（`v[v.size()]`）：Java 抛异常。
- **悬空指针/引用、use-after-free、double free**：Java 不可能。
- **空指针解引用**：Java 抛 NPE。
- **数据竞争**：Java 定义弱语义。
- **读未初始化变量**：Java 局部变量必须赋值。
- **严格别名违规**（`int*` 当 `float*` 读）。
- **移位过大/负数移位**（32 位 int 的 `1 << 32`）：Java 移位量取模。
- **`INT_MIN / -1`、除零**：Java 除零抛异常。
- **非 void 函数没有 return 就走到末尾**：Java 编译错误。
- 违反 `memcpy` 不重叠、修改 `const` 对象。
