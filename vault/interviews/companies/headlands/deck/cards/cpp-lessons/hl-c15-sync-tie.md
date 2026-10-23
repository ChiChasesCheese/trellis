---
id: hl-c15-sync-tie
node: cpp-lessons.c15-io-performance
type: qa
step: 2
---
## Q
面试问：`ios::sync_with_stdio(false)` 和 `cin.tie(nullptr)` 是做什么的？有什么副作用？
Interview question: What do `sync_with_stdio(false)` and `cin.tie(nullptr)` do?

## A
```cpp
std::ios::sync_with_stdio(false);
std::cin.tie(nullptr);
```
- 默认 `cin/cout` 与 C 的 `stdin/stdout` **同步**（`printf` 与 `cout` 混用时顺序才正确），同步意味着每次操作无法缓冲。`cin` 还默认与 `cout` **绑定**（读之前先刷新 `cout`）。
- `sync_with_stdio(false)`：放弃同步，必须在任何 I/O 之前调用；之后**不能再混用** `printf/scanf` 与 `cin/cout`（输出顺序错乱）。
- `cin.tie(nullptr)`：读之前不再刷新 `cout`；**交互式程序不要用**。
- 效果取决于标准库实现；最稳妥的快速读入是**一次读全部输入，自己解析**。
