---
id: pl-errors-exceptions-best-practice
node: errors.exceptions
type: qa
step: 5
---
## Q
在 Java 和 Python 里使用异常的最佳实践是什么？为什么？

## A
1. **捕获尽可能具体的类型**。`catch (Exception e)` 或 `except Exception` 会吞掉你没预料到的 bug（空指针、类型错误），把它们伪装成「处理过的错误」。Python 里绝不要 `except:` 或 `except BaseException`，它们会拦住 `KeyboardInterrupt` 和 `SystemExit`，让程序无法被中断。
2. **保留原因**。包装异常时一定带上 cause：Java `new ServiceException("load user", e)`，Python `raise ServiceError("load user") from e`。否则丢失了真正的根因。
3. **在能做决定的层处理，其他层不捕获**。不要每层都 `catch` 再 `throw`。中间层只在需要加上下文或翻译异常类型时才捕获。
4. **一次处理，一次记录**。不要「记录日志再抛出」，同一个错误会出现在多处日志里。
5. **异常类型表达调用者的决策**。设计异常层次时问：调用者会据此做什么不同的事（重试、提示用户、放弃）？只对这些区别设立类型。
6. **资源用作用域语法**：Java 的 try-with-resources、Python 的 `with`，而不是手写 `finally`。
7. **异常用于例外，不用于控制流**（Java 中尤其重要，见性能代价）。Python 里 EAFP 是惯用的，但前提是失败确实少见。
8. **在边界转换**：HTTP 层把领域异常翻译成状态码，不把内部异常的原始消息暴露给用户。
9. **Java 受检异常**：自己的新 API 默认用非受检异常；只有调用者合理地可以并且应该恢复的情形（例如「文件不存在，换个路径」）才用受检异常。
10. **Python 3.11 起**：并发中可能同时出现多个错误，用 `ExceptionGroup` 和 `except*` 分别处理。

什么时候违反：命令行脚本里，让异常直接传播到顶层并打印栈追踪，往往就是正确的错误处理。
