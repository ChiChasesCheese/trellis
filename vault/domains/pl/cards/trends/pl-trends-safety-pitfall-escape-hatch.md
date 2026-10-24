---
id: pl-trends-safety-pitfall-escape-hatch
node: trends.safety-push
type: qa
step: 9
---
## Q
“我们用的是内存安全语言”为什么不等于“我们没有内存安全漏洞”？逃生舱和未检查的假设在生产中怎样出事？

## A
**误区一：整个项目都安全**。安全的范围只覆盖不使用逃生舱的代码。真实情形：

```python
import ctypes; ctypes.string_at(0)
# Fatal Python error: Segmentation fault
```

进程直接崩溃，没有 Python 异常可捕获。大型 Python 应用的核心常常是 C 扩展（NumPy、图像库、数据库驱动），这些库里的缓冲区溢出同样是你的漏洞，即使你的业务代码都是纯 Python。

```rust
let p = v.as_ptr(); drop(v);
let x = unsafe { *p };     // compiles, prints a garbage value
```

Rust 里同样如此：这段代码**编译通过**，运行得到垃圾值（本机一次得到 `4`），既没有 panic 也没有告警，因为 `unsafe` 块是你声明“这里我负责”。

**误区二：安全语言没有崩溃**。越界访问在 Go、Rust、Java、Python 里会变成 panic 或异常，进程停止服务，这是拒绝服务（DoS）。内存安全把“可能被利用的漏洞”降级成“可被利用的崩溃”，对可用性要求高的服务仍需要输入校验和恢复机制。

**误区三：安全语言的运行时本身没有漏洞**。JVM、CPython、Go 运行时都有过内存安全漏洞（它们是 C/C++/汇编写的），所以运行时升级仍然是安全工作。

**误区四：安全意味着正确**。内存安全不防逻辑漏洞（SQL 注入、权限检查缺失、整数溢出导致的业务错误）。

**防线**：
1. 把原生依赖清点出来，纳入漏洞扫描。
2. 封装逃生舱，限制其暴露面，并在 CI 中用 sanitizer、Miri、模糊测试覆盖。
3. 对不可信输入先校验大小和结构，再交给原生代码。
4. 评审时问：这次变更是否新增了 `unsafe`、`cgo`、`ctypes` 或 JNI？
