---
id: hl-javaq-d-q11-cost-follow-ups
node: java-questions.d-memory
type: qa
step: 5
---
## Q
Java 分配"便宜不等于免费"的证据是什么？热路径上怎么减少分配？常见对象的大小是多少？
How do you reduce allocation in a hot path?

## A
- **证据**：没逃逸的对象被 JIT 消除（稳态分配 0 字节）；关掉逃逸分析后每次迭代分配 **96 字节**，5000 万次迭代共 **4.8 GB**，慢约 8 倍。
- **减少分配**：复用对象、用原始类型数组、避免装箱、避免捕获型 lambda、复用 `StringBuilder`。
- **对象大小**：`new Object()` = 16 字节；`record P2(int x,int y)` = 24；`P3(long×3)` = 40；`Integer` = 16；`new int[10]` = 56。
