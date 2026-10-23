---
id: hl-javaq-rubric-f-weak
node: java-questions.rubric
type: qa
step: 10
---
## Q
回答并发与内存模型的问题时，"一般"和"弱"的答案分别是什么样？

## A
- **一般**：背得出 `volatile` 保证可见性，知道 `ConcurrentHashMap` 比 `synchronizedMap` 好，但说不出机制；对 happens-before 只能给定义，给不出规则或例子。
- **弱**：
  - "`volatile` 保证线程安全"；
  - "`synchronized` 很慢所以不用"；
  - "`ConcurrentHashMap` 分段锁"（Java 7 的设计）；
  - 不知道线程池无界队列的问题；
  - DCL（双重检查锁）不加 `volatile`。
