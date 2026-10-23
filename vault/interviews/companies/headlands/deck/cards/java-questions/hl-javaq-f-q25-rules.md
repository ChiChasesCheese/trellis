---
id: hl-javaq-f-q25-rules
node: java-questions.f-concurrency
type: qa
step: 3
---
## Q
列出 JMM happens-before 的主要规则。怎样用 volatile 完成"发布"（先写 data 再写 ready）？

## A
1. **程序顺序**：同一线程内，前面的动作 hb 后面的。
2. **监视器**：`unlock` hb 之后对**同一个**锁的 `lock`。
3. **volatile**：对 volatile 变量的写 hb 之后对它的读。
4. **线程**：`Thread.start()` hb 被启动线程里的任何动作；线程里的所有动作 hb 另一线程从 `join()` 返回。
5. **final 字段**：构造器结束时的冻结语义。
6. **传递性**：A hb B 且 B hb C ⇒ A hb C。

规则 3 + 6 就是"发布"套路：写 `data`（普通写），再写 volatile `ready`；读 `ready`（volatile 读），再读 `data`——保证读到 42。

追问"`synchronized` 给可见性吗"：给——`unlock` hb 随后的 `lock`；进入时重新读、退出时写回。
