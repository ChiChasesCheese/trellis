---
id: pl-trends-effects-foundation-async-keyword
node: trends.effects
type: qa
step: 3
---
## Q
`async` 为什么也是一种效应？为什么 `async` 函数的「染色」问题，本质上是缺少对效应的多态？

## A
`async fn` 的含义是：「这个函数可能挂起，把线程让给别人」。挂起是一种效应，`async` 关键字就是把它写进了函数的签名；`await` 是调用者对这个效应的处理（等它完成）。

染色的根源是：**一个带效应的函数只能在能处理该效应的上下文里调用。**在普通函数里调用 `async` 函数，拿到的只是一个未执行的对象，没有执行器就无法得到结果：

```python
async def fetch(): return 1
def sync_caller():
    x = fetch()
    return x + 1
# RuntimeWarning: coroutine 'fetch' was never awaited
# TypeError: unsupported operand type(s) for +: 'coroutine' and 'int'
```

`fetch()` 返回协程对象，既没有被 `await`，也不是整数。

效应沿调用链向上传染：想调用 `async` 函数，自己也得是 `async`。标准库里每个可能阻塞的函数就需要两套：同步版和异步版（Rust 的 `std::fs` 与 `tokio::fs`，Python 的 `open` 与 `aiofiles`）。库作者要写两遍，使用者要选择。这就是缺少**效应多态**的症状：如果能写一个对「是否异步」通用的函数（`fn read<E>() -> E String`），一份实现就能同时服务两种调用方。

Rust 里同样的问题不止 `async`。语言里有一批「着色」关键字：

- `const fn`：可以在编译期求值；
- `unsafe fn`：调用者必须承担安全义务；
- `async fn`：可能挂起；
- 返回 `Result`：可能失败；
- `&mut self`：会修改自身。

每一种都是一个效应，每一种都有「能调用谁」的传染规则。Rust 社区讨论过「关键字泛型」（keyword generics）这个方向：写一个函数同时对 `const`、`async` 通用；它目前不是稳定语言特性。

有些语言选择**消除颜色**：Go 的协程和 Java 21 的虚拟线程让阻塞调用本身变得便宜，不需要 `async` 关键字，所有函数看起来都是同步的。代价是挂起的位置不再在类型里可见，调用者看不出一个函数是否可能长时间阻塞。

要记住的一点：`async` 的染色不是实现缺陷，是效应被写进类型后的必然结果；要么忍受它，要么用运行时把效应藏起来。
