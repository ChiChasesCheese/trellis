---
id: pl-rt-ffi-found-go
node: runtime.ffi
type: qa
step: 3
---
## Q
Go 的 cgo 是什么？它怎样让 Go 调用 C，为什么 Go 社区常说“cgo 不是 Go”？

## A
**cgo** 是 Go 工具链自带的 C 互操作机制：在 Go 源文件里，紧挨着 `import "C"` 的注释块可以写 C 代码或 `#include`，之后用 `C.函数名` 调用：
```go
/*
#include <string.h>
#include <stdlib.h>
*/
import "C"

cs := C.CString("hello, ffi")        // malloc'd copy of the Go string
defer C.free(unsafe.Pointer(cs))
fmt.Println(C.strlen(cs))
```
输出：`10`。

要点：
1. **`C.CString` 复制到 C 堆**：Go 的字符串由 GC 管理、可能被移动或回收，不能直接把指针交给 C；所以要复制一份用 `malloc` 分配的 C 字符串，用完手动 `C.free`。
2. cgo 在构建时生成转接代码，并调用系统的 C 编译器（gcc/clang）编译 C 部分，所以构建环境必须有 C 工具链。
3. 一次调用要：切换到系统线程的栈（goroutine 的栈太小，C 代码需要大栈）、告知调度器“此 goroutine 将进入 C”（调度器可能把该线程的 P 让出去）、返回时再切换回来。

**为什么说“cgo 不是 Go”**（Go 社区的谚语）：
- **性能**：调用比普通 Go 函数贵一个数量级以上；
- **构建**：失去纯 Go 的快速构建、简单交叉编译和单文件静态链接；
- **运行时**：C 代码里的阻塞会占用一个操作系统线程，C 里 `malloc` 的内存 GC 不知道；
- **工具**：竞争检测、调试、内存分析对 C 部分有限。

所以 Go 生态偏向用纯 Go 重写库（如纯 Go 的 SQLite 实现），只有必需时才用 cgo。
