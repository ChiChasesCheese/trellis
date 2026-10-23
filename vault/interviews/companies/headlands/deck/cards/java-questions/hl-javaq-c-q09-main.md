---
id: hl-javaq-c-q09-main
node: java-questions.c-languages
type: qa
step: 10
---
## Q
Java 保证了哪些 C++ 不保证的行为（反之亦然）？从未定义行为、整数语义、内存安全几方面说。
What does Java guarantee that C++ does not (and vice versa)? Think undefined behaviour, integer semantics, memory safety.

## A
一句话：Java 的每个行为都有定义；C++ 的**未定义行为**（UB）让优化器更激进，但风险由程序员背。

- **有符号溢出**：Java 按二进制补码回绕（JLS 规定）；C++ 是 UB，编译器可以假设它不发生，甚至删掉你的检查。
- **数组越界**：Java 抛 `ArrayIndexOutOfBoundsException`；C++ 是 UB，可能读到别的数据、崩溃、被利用。
- **空指针**：Java 抛 `NullPointerException`。
- **数据竞争**：C++ 是 UB；Java 有定义但弱——可能读到旧值或乱序，但读到的每个值都是某次写入的值，不会凭空产生。
- 安全不等于免费：边界检查、空检查有成本，但 JIT 大量消除。
