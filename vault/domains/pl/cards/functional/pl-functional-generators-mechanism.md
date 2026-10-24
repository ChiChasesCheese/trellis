---
id: pl-functional-generators-mechanism
node: functional.generators
type: qa
step: 6
---
## Q
无栈协程和有栈协程在实现上有什么不同？为什么 Python 递归遍历树要写 `yield from`？

## A
**无栈**（Python 生成器、Rust `async`、C++20 协程）：暂停时只保存**这一个函数**的局部状态，调用它的和它调用的普通函数不在保存范围内。Python 的生成器对象持有一个帧对象（局部变量 + 下一条指令的位置）；Rust 的状态机是编译期生成的枚举；C++ 的编译器生成一块协程帧（保存局部变量和暂停位置的结构），默认在堆上分配，生命周期可见时会被优化到栈上。恢复时，把这个帧放回执行。

结果是：`yield` 只能出现在生成器函数自己的函数体里。要递归遍历树，每一层递归都得是生成器，并且把子层产出的值转手交上去，这就是 `yield from`：

```python
def walk(t):
    if t is None: return
    yield from walk(t[0])
    yield t[1]
    yield from walk(t[2])
list(walk(tree))            # [1, 2, 3, 4]
```

如果漏写 `yield from`，只是调用 `walk2 = bad(t[0])` 而不迭代，子树被完全跳过，结果不报错但少了数据（上面的输出会只有 `[2]`）。这个设计的代价是明确的：递归深度 n 时，每个值要穿过 n 层生成器才送到调用者，成本是 O(深度)。

**有栈**（goroutine、Go 的 `iter.Pull`、虚拟线程）：每个协程有独立的栈。暂停时保存整条调用链，所以 `yield` 可以出现在任意深度的函数里。代价是栈的内存（goroutine 初始约 2 KB，虚拟线程按需增长）和切换时保存 / 恢复寄存器与栈指针。

选择的权衡：无栈更省内存、切换快，适合编译期就能看清结构的场景（`async` 状态机可以精确计算大小）；有栈更灵活、对程序员透明，不需要给函数「染色」。这也是 Go 与 Java 选有栈、Rust、Python 与 C++ 选无栈的深层原因。
