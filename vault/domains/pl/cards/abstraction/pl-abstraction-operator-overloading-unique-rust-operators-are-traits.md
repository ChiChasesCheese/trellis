---
id: pl-abstraction-operator-overloading-unique-rust-operators-are-traits
node: abstraction.operator-overloading
type: qa
step: 7
---
## Q
Rust 把运算符做成 trait，而 Python 做成 dunder 方法。两者的差别揭示了什么设计思想？

## A
表面上都是「`a + b` 翻译成调用某个方法」，差别在**这个方法属于什么**。

**Python**：`__add__` 是类上的一个同名方法，属于类的字典。能不能相加，在运行期检查：有没有这个方法、返回的是不是 `NotImplemented`。运算符协议和其他方法没有区别，也不参与类型检查。

**Rust**：`Add` 是一个有契约的 trait，带有关联类型 `Output` 说明结果类型，可以是和输入不同的类型（`Instant + Duration` 得到 `Instant`）。因为它是 trait，就能在泛型函数里作为约束：`fn total<T: Add<Output = T>>(...)`。于是**泛型代码可以对一切「可相加的东西」编程**，不管它是整数、浮点还是用户自定义的向量。Python 里这件事只能靠运行期的鸭子类型。

Rust 的做法还暴露了所有权：`add(self, rhs)` 按值接收，所以每个运算都要考虑所有权，用户要为 `&T` 单独实现。这让运算符的真实成本（移动还是复制）在类型层面可见。

思想上的区别：Python 认为**运算符是对象的行为**，由对象自己决定；Rust 认为**运算符是类型之间的关系**，在编译期被证明、被统一抽象。Python 偏向运行期的灵活，Rust 偏向编译期的可证明与零成本。

Rust 的限制也是有意的：只能重载预定义的那一组运算符，不能发明 `<=>` 之类的新符号，每个运算符对应一个固定的标准库 trait，符号和语义的对应关系是统一的。这样 Rust 保留了数学记号的便利，又不丧失可读性。
