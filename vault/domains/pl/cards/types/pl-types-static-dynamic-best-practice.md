---
id: pl-types-static-dynamic-best-practice
node: types.static-dynamic
type: qa
step: 8
---
## Q
在静态类型语言里，怎样让类型系统真正替你挡 bug？在 Python 里，怎样补上动态类型缺失的检查？

## A
核心做法：让类型表达业务含义，使非法状态在类型上不可表示。

- 静态语言：用「新类型」（newtype）包装原始类型，不要到处传裸的 `int` 或 `String`。`UserId` 和 `OrderId` 底层都是整数，但混用是业务错误：

```rust
struct UserId(u64);
struct OrderId(u64);
fn cancel(order: OrderId) { /* ... */ }
// cancel(UserId(7)) 编译失败：expected `OrderId`, found `UserId`
```

- C++ 的陷阱：`using UserId = std::uint64_t;` 只是别名，不是新类型，`UserId` 与 `OrderId` 仍然可以互相传。要真正区分，必须包成结构体：
```cpp
using UserId = std::uint64_t;  using OrderId = std::uint64_t;   // aliases: cancel(UserId{7}) compiles
struct UserId2 { std::uint64_t v; };  struct OrderId2 { std::uint64_t v; };
// cancel2(UserId2{7}) -> error: no matching function for call to 'cancel2'
```
- 避开类型系统的逃生口：Java 的 `Object` 和原始类型 `List`，Go 的 `any`（即 `interface{}`），都会把检查推回运行期，只在边界（序列化、插件）使用。
- Python：给公共接口加类型提示，在 CI 里跑 `mypy` 或 `pyright`，新代码启用严格模式。`NewType` 能得到同样的区分，但只对检查器有效：

```python
UserId = NewType("UserId", int)
OrderId = NewType("OrderId", int)
def cancel(order: OrderId) -> None: ...
cancel(UserId(7))   # mypy: incompatible type "UserId"; expected "OrderId"
```

`mypy` 会报错，但直接运行 `python` 不报错，输出 `cancel 7`。所以不可信的输入（HTTP 请求、JSON、配置）要在边界用运行时校验（手写检查或 `pydantic` 这类库），因为类型提示不会在运行时检查。

何时可以破例：一次性脚本不必加类型；性能分析后少数热点可以放宽类型换取速度。其余场合，类型越早加成本越低，补一个二十万行的无类型代码库比从头写难得多。
