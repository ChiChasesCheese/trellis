---
id: hl-j16-hb-rules
node: java21.j16-concurrency-primitives
type: qa
step: 7
---
## Q
说出 JMM 的七条 happens-before 规则。为什么 `volatile` 标志位能发布数据？

## A
1. **程序顺序**：同一线程里，前面的操作 HB 后面的。
2. **监视器锁**：同一把锁，`unlock` HB 之后对它的 `lock`。
3. **volatile**：同一个 volatile 变量，写 HB 之后的读。
4. **线程启动**：`t.start()` HB `t` 里的所有操作。
5. **线程终止**：`t` 里所有操作 HB 别的线程里 `t.join()` 的返回。
6. **传递性**：X HB Y 且 Y HB Z ⇒ X HB Z。
7. **final 字段**：构造器正常结束后，`final` 字段的值对任何拿到该对象引用的线程可见（安全发布）。

volatile 标志位发布数据：volatile 写之前的数据写入 HB 该写（程序顺序），该写 HB 之后的读（规则 3），传递性使读者读到标志后一定看到数据。
