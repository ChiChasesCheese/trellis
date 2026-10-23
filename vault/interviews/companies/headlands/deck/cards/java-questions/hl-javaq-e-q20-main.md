---
id: hl-javaq-e-q20-main
node: java-questions.e-jit-gc
type: qa
step: 9
---
## Q
什么是逃逸分析（escape analysis）？它带来哪些优化，什么时候会失败？
What is escape analysis? What optimisations come from it, and when does it fail?

## A
一句话：C2 分析对象是否"逃出"当前编译单元（被存到字段 / 静态变量、被返回、传给未内联的方法）；**不逃逸**就可以做：
- **标量替换**（scalar replacement）：对象拆成寄存器里的字段，根本不分配。
- **锁消除**：对这类对象的 `synchronized` 去掉。

例：`new Point(i, i+1).plus(new Point(2, 3))` 内联后三个 Point 都只被读字段，变成 4 个 long 局部变量的算术。

注意：EA 是 **C2** 的优化，C1 没有，所以预热后才出现；它是优化，不是语言保证。
