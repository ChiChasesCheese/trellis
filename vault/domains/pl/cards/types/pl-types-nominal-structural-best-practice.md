---
id: pl-types-nominal-structural-best-practice
node: types.nominal-structural
type: qa
step: 5
---
## Q
设计接口或 trait 时，资深工程师遵循哪些规则？Go、Java、Rust、Python 各自的做法是什么？

## A
共同的原则是：依赖尽量小的抽象，让接口描述「调用方需要什么」，而不是「实现方是什么」。

- Go：接口要小（一两个方法），在使用方的包里定义，函数「接受接口，返回具体类型」。这样调用方只依赖它真正用到的能力，测试时也容易换成假实现。为防意图悄悄失效，在类型旁加 `var _ Speaker = (*Dog)(nil)` 这样的编译期断言。
- Java：面向接口编程，保持接口小；第三方类要适配时写适配器，而不是复制代码；用 `sealed` 接口表达「只有这几种实现」的封闭集合。
- Rust：默认用泛型加 trait 约束，静态分派没有运行时开销；只有需要把不同类型放进同一个集合时才用 `dyn Trait`。trait 要小而专，能用已有的标准 trait（`Display`、`From`、`Iterator`）就不要自己造。
- Python：参数的类型提示写最小的协议，例如 `Iterable[str]` 或自定义的 `Protocol`，而不是具体的 `list`。抽象基类只在需要强制子类实现或运行时注册时用。

`Protocol` 把鸭子类型变成可检查的契约：

```python
class SupportsClose(Protocol):
    def close(self) -> None: ...

shutdown(Conn())    # 通过
shutdown(Bad())     # mypy: Expected def close(self) -> None; Got def close(self, force: bool) -> None
```

`Bad` 的 `close` 多了参数，签名不吻合，`mypy` 在运行前报错并列出差异。

何时可以破例：只有一个实现、且短期不会有第二个时，不必先抽象出接口（过早抽象的成本是无处不在的间接层）；等第二个使用场景出现再提取，这在 Go 里尤其容易，因为不用改已有类型。
