---
id: pl-rt-linking-found-abi
node: runtime.linking-abi
type: qa
step: 4
---
## Q
ABI 具体包含哪些东西？为什么 C ABI 成了跨语言的通用语，而 Rust 的结构体布局不能跨编译器版本依赖？

## A
**ABI 包含的内容**：
1. **调用约定**：参数放哪些寄存器、多出来的放栈、谁负责清理栈、返回值怎么传。
2. **数据布局**：每个类型占多大、对齐多少、结构体字段按什么顺序排、偏移多少、枚举怎么编码。
3. **符号命名**：函数在目标文件里叫什么名字（C 的 `helper` 对应 `_helper`；Rust/C++ 的名字被重整）。
4. **与运行时/系统的约定**：栈的结构、异常展开的信息、动态链接的格式。

**C ABI 是通用语**：C 的 ABI 在每个平台上都由平台自己规定（ARM64 有 AAPCS64，x86-64 Linux 有 System V），语言本身几乎没有隐藏的东西，结构体按声明顺序排、符号不重整。所以 Rust 的 `extern "C"`、Go 的 cgo、Java 的 FFM、Python 的 ctypes 全都选它作为“和别人说话”的方式：不是因为它好，而是因为**所有人都已经会说它**。

**Rust 没有稳定 ABI**：Rust 编译器允许自己决定结构体的字段顺序，以减少填充。实测：
```rust
struct Rs { a: u8, b: u32, c: u8 }              // size = 8 (compiler reorders fields)
#[repr(C)] struct Rc { a: u8, b: u32, c: u8 }   // size = 12 (declaration order + padding)
```
输出 `Rust layout: size=8` 和 `repr(C): size=12`。Rust 默认布局可能随编译器版本变化，所以不同版本编译的两个 Rust 库不能通过共享库传结构体；要跨边界，就要显式用 `#[repr(C)]` 加 `extern "C"`。

**其他语言各有各的“稳定面”**：
- **Swift** 从 5.0（2019）起在 Apple 平台有稳定 ABI，系统库因此可以作为共享库随 OS 升级，代价是语言要为“库升级后结构体字段可能变化”做间接访问。
- **Go** 的内部 ABI 也不稳定（1.17 起从栈传参改为寄存器传参，汇编函数通过包装对接），对外只承诺源码兼容。
- **Java** 的稳定面是**类文件格式与二进制兼容性规则**，不是机器码 ABI。
- **Python** 的 C 扩展直接依赖解释器内部结构，文件名里带着版本：本机的后缀是 `.cpython-314-darwin.so`，只能被 3.14 加载。只用“受限 C API”（`abi3`，PEP 384）编译的扩展叫 `.abi3.so`，可以跨小版本加载。
