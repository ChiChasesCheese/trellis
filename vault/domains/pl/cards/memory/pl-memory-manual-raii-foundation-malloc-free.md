---
id: pl-memory-manual-raii-foundation-malloc-free
node: memory.manual-raii
type: qa
step: 2
---
## Q
C 里的 `malloc` 和 `free` 是怎么用的？“手动管理”具体要程序员做什么？

## A
C 语言没有任何自动回收：向堆要内存用 `malloc(n)`，它返回一个指向 n 字节空间的指针；用完必须调用 `free(p)` 归还，每一次 `malloc` 都要对应恰好一次 `free`。

```c
char *s = malloc(8);       // ask the allocator for 8 bytes
strcpy(s, "hi");
free(s);                   // give it back; s still holds the old address
```

`free` 之后，变量 `s` 里的地址并不会清空，它只是变成了指向“已归还内存”的**悬空指针**（dangling pointer）。接下来三种操作都是错误：再读写 `s`（释放后使用，use-after-free）、再 `free(s)`（重复释放，double free）、或者根本忘了 `free`（泄漏，leak）。

难处不在单个函数，而在于释放的责任：一个指针被传来传去，谁该 `free`？函数中途 `return` 或出错时，别忘了在每条路径上补 `free`。大型项目里这类约定一旦被打破，就会出现崩溃或安全漏洞。

要记住的一个事实：手动管理把“何时释放”完全交给程序员，语言没有任何检查；本领域后面介绍的各种机制（RAII、GC、引用计数、所有权），都是在回答怎样让这件事不再靠人记。
