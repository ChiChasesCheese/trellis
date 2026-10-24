---
id: pl-errors-panics-foundation-java-python
node: errors.panics
type: qa
step: 4
---
## Q
Java 的 `Error` 和 Python 的 `BaseException` 是什么？它们怎样表示“不该被普通代码捕获”的问题？

## A
Java 和 Python 没有独立的 panic 机制，而是在异常的类层次里划出一层“严重”的分支：

**Java**：`Throwable` 有两个直接子类：`Exception`（应用层可处理的，包含受检异常和 `RuntimeException`）和 `Error`（虚拟机层面的严重问题：`OutOfMemoryError`、`StackOverflowError`、`AssertionError`）。约定是应用代码不应捕获 `Error`——内存耗尽了，catch 之后继续跑也不可靠。

```java
try { Object[] o = new Object[Integer.MAX_VALUE]; }
catch (Throwable t) { System.out.println(t.getClass().getName() + " is Error: " + (t instanceof Error)); }
// java.lang.OutOfMemoryError is Error: true
```

未捕获的异常终止所在线程；主线程终止后进程以状态码 1 退出。

**Python**：所有异常继承 `BaseException`。`Exception` 是常规错误的基类；`SystemExit`（`sys.exit()` 抛出）、`KeyboardInterrupt`（Ctrl+C）、`GeneratorExit` 直接继承 `BaseException`，目的是让 `except Exception:` 不会拦住退出和中断。

```python
try: sys.exit(3)
except Exception: print("not reached")
except BaseException as e: print("caught", type(e).__name__, e.code)   # caught SystemExit 3
```

裸 `except:` 和 `except BaseException:` 会拦住一切，包括 Ctrl+C。

要记住的一个事实：这两门语言用异常类的继承位置来区分“可处理”和“不该拦”，靠约定而不是机制保证。
