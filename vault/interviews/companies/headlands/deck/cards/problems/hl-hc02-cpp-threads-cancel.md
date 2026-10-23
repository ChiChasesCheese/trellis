---
id: hl-hc02-cpp-threads-cancel
node: problems.hc02-merge-k-streams
type: qa
step: 21
---
## Q
C++20 实现并发合并时，线程、取消、队列、结构化并发分别怎么对应 Java 版？

## A
| 点 | Java | C++20 |
|---|---|---|
| 线程 | 虚拟线程 | `std::jthread`（OS 线程，数量要自己控制） |
| 取消 | `Thread.interrupt`，阻塞调用抛 `InterruptedException` | `std::stop_token`：**协作式**，source 和每次等待都要认它 |
| 队列 | `ArrayBlockingQueue` | 自己写：`mutex` + `condition_variable_any` + `deque` |
| 结构化并发 | `StructuredTaskScope` | 没有现成的：`ThreadGroup`（析构 = 请求停止 + join）+ 记录第一个失败 |

要点：
- C++ 不能杀线程；`jthread` 析构自动 `request_stop` + `join`。
- 用 `condition_variable_any` 是因为只有它的 `wait` 有 `stop_token` 重载；普通 `condition_variable` 要配 `stop_callback`，手动加锁再通知，易写错。条件变量一定配谓词（防虚假唤醒）。
- **线程体里漏出的异常 = `std::terminate`**，必须 `catch (...)` 并用 `std::exception_ptr` 带出来；`merge_all` 里第一个失败记录下来并 `request_stop()`。
- **成员声明顺序决定销毁顺序**：线程组要**最后声明**，最先销毁，析构先请求停止并 join，之后线程用过的队列和 source 才被销毁。
- 生产者结束同样留下 `End` 或 `Failed`；每个 source 最多被读 `capacity + 1` 个。
