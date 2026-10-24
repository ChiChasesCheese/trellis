---
id: pl-binding-calling-convention-best-practice
node: binding.calling-convention
type: qa
step: 9
---
## Q
理解了栈帧和调用约定之后，资深工程师在 Go、Java、Rust、Python 里写递归、设置栈大小和处理热点函数时有哪些实践？

## A
**不要为了省调用而扭曲代码。**一次调用只是几条指令，函数该拆就拆；热点函数小而简单，编译器和 JIT 会内联。判断是否有问题，用剖析器看数据，不凭直觉。

**递归的实践**
- 深度由输入决定（树、图、用户给的嵌套数据）时，改用显式栈循环，或限制深度并在入口校验。理由：这四门语言都不保证尾调用优化，攻击者可以用深层嵌套的输入把栈撑破（拒绝服务）。
- Python：不要靠 `sys.setrecursionlimit` 加大深度，调到很大时，经过 C 代码的递归路径（如 `json`、`repr` 处理深层嵌套）仍可能撑破 C 栈，进程直接崩溃；改循环。
- Java：深度可预期时用递归，必要时线程用 `new Thread(group, task, "name", stackSize)` 指定栈大小；框架的深层调用链（Spring、ORM）本身就占深度，别把栈调得太小。
- Rust：给需要深递归的任务单独开线程，用 `std::thread::Builder::new().stack_size(…)`；大数组放堆上（`Box`、`Vec`），不要当局部变量。
- Go：通常无需关心栈大小；无限递归的症状是内存涨到 1 GB 上限后 `fatal error: stack overflow`，同样是 bug，不会被 `recover` 捕获。

**热点函数的实践**
- Go：用 `go build -gcflags=-m` 看哪些函数被内联；热点小函数保持短小就能内联；除非有测量依据，不要手工拆分或合并。
- Java：让热点方法短小，避免过深的类层次，JIT 才能内联；不要手工内联。
- Rust：默认交给编译器；跨 crate 的小函数加 `#[inline]`；`#[inline(always)]` 只在测量证明有益时用。

**需要和 C 互操作时**：用 `extern "C"`（Rust）、cgo（Go）、JNI/Panama（Java）、`ctypes`（Python）；这些都是跨 ABI 边界的调用，每次穿过都有额外成本（Go 的 cgo 调用每次约几十纳秒，远高于普通调用），应批量调用而不是在循环里逐个穿越。

什么时候违反：脚本和一次性工具里直接用递归，数据规模可控时最清楚。
