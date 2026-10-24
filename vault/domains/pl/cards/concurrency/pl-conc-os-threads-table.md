---
id: pl-conc-os-threads-table
node: concurrency.os-threads
type: qa
step: 6
---
## Q
Java、Rust、Python 的 OS 线程 API 在「结果和错误怎么回到调用方」「线程能不能比创建者活得久」上做了不同选择，各自反映什么取舍？

## A
| 语言 | 结果与错误 | 线程生命周期 | 取舍 |
|---|---|---|---|
| Java | 裸 `Thread` 无返回值，异常只被打印；线程池 + `Future` 才能拿结果 | 非守护线程会阻止 JVM 退出 | 保持最小原语，高层能力放进 `java.util.concurrent`，代价是新手容易丢异常 |
| Rust | `JoinHandle<T>::join()` 返回 `Result`，panic 变成 `Err` | 主线程返回，子线程即被终止；闭包必须 `'static + Send` | 把「结果、错误、所有权」都放进类型，代价是写法更严格 |
| Python | 裸 `Thread` 无返回值，异常交给 `excepthook` 打印；`Future` 才能拿结果 | 非守护线程会阻止解释器退出 | 与 Java 同源（`threading` 模仿 Java），后来用 `concurrent.futures` 补上 |

规律：
- Java 和 Python 的线程是**任务无关的执行容器**（`run()` 不返回任何东西），把「结果」这一层推给了库。结果是同一个坑在两门语言里都存在：裸线程里的异常默默消失，主线程浑然不觉。
- Rust 把线程当成**有返回值的函数调用**，失败路径是类型的一部分，没有「忘了处理」的余地。
- 生命周期也一样：Rust 要求线程不借用栈上数据（否则编译不过），因为它不愿意让悬空引用成为可能；Java 和 Python 有垃圾回收，不存在悬空，只剩「什么时候结束」的问题。
