---
id: pl-functional-recursion-tco-table
node: functional.recursion-tco
type: qa
step: 8
---
## Q
Go、Java、Rust、Python 对递归深度与尾调用的处理有什么区别？

## A
| 语言 | 尾调用优化 | 超深时的表现 | 能否恢复 |
|---|---|---|---|
| Go | 不保证 | 栈可增长到 1 GB，再超则 `fatal error` | 不能（进程退出） |
| Java | 不做 | `StackOverflowError`，约几万层 | 可以捕获，但不建议 |
| Rust | 不保证，release 下偶尔被 LLVM 改写成循环 | 栈溢出后进程中止 | 不能 |
| Python | 不做（明确拒绝） | `RecursionError`，默认 1000 层 | 可以捕获，状态完好 |

规律：**Python 的限制最保守但最友好**（早早抛出异常，程序还能继续）；**Go 最宽松**（几乎不用在意深度）；Java 与 Rust 取决于栈大小，崩溃的形式不同。

Python 的设计者 Guido 明确不要 TCO，理由是它会让栈回溯不完整，并且 Python 的风格是"用循环写循环"。Java 的 HotSpot 依赖完整的调用栈（栈回溯、栈遍历），一直没有实现 TCO。Rust 在底层语言的立场下，倾向保持每个调用的栈帧可见，析构语义也使"尾位置"含糊。Go 把栈管理交给运行时，使深递归成为库开发者不需要思考的事。

对工程师来说，实用含义是：不要依赖 TCO；对"深度由输入决定"的递归，要么限制深度，要么写成迭代。
