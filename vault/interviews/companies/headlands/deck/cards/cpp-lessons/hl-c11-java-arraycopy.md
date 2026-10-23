---
id: hl-c11-java-arraycopy
node: cpp-lessons.c11-copy-vs-memcpy
type: qa
step: 2
---
## Q
Java 里什么对应 C++ 的 `memmove`/`std::copy`？`Arrays.copyOf` 做了什么？

## A
- `System.arraycopy(src, sp, dst, dp, n)`：JIT 内联的内部函数（intrinsic），语义等价 `memmove`（重叠安全），带边界与类型检查，**对象数组复制的是引用**。
- `Arrays.copyOf` = 新分配 + 清零 + 拷贝。
- Java 里没有「错误类型的拷贝」这个问题；C++ 有（对非平凡类型 `memcpy` 是 UB）。
