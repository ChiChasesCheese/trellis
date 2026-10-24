---
id: pl-abstraction-bounds-variance-best-practice
node: abstraction.bounds-variance
type: qa
step: 9
---
## Q
资深工程师在设计泛型 API 时怎样处理约束与型变？

## A
**约束**的通用规则：**只写函数体真正用到的最小约束**。约束越多，能调用它的类型越少，也越难演进；约束的改动是破坏性变更。

- **Rust**：约束写在需要它的地方。结构体定义上少放约束，只在 `impl` 块或方法上加，这样不用的方法不会强迫用户满足无关的 trait。多个约束较长时用 `where`，可读性更好。
- **Go**：优先用标准库约束（`cmp.Ordered`、`comparable`），不要自己重新列类型并集；自定义约束保持小。
- **Java**：API 的参数尽量用通配符以提高灵活性：只读用 `? extends T`，只写用 `? super T`；**返回值不要用通配符**，否则调用者得处理未知类型。用得简洁的方法是先写出不带通配符的版本，再根据读写方向放宽参数。
- **Python**：被调用者只读参数时，类型写成协议或抽象类型（`Sequence[T]`、`Iterable[T]`），而不是 `list[T]`；这样调用者传 `tuple` 或 `list[Dog]` 都能通过，因为只读的抽象类型是协变的。

何时打破：公开的稳定 API 里，宁可约束稍严、型变稍保守，因为以后放宽是兼容的，收紧不是。
