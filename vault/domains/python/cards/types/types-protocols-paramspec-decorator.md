---
id: types-protocols-paramspec-decorator
node: types.protocols-generics
type: qa
source: python-docs
---
## Q
写一个保持被装饰函数原始参数签名的装饰器（decorator），为什么普通 `TypeVar` 不够用，需要 `ParamSpec`？

## A
普通 `TypeVar` 只能代表单个具体类型，没法表示「任意一组参数」这种可变形状的签名。`ParamSpec`（如 `def with_lock[**P, R](f: Callable[Concatenate[Lock, P], R]) -> Callable[P, R]`）专门用来把一个可调用对象的参数列表原样转发给另一个可调用对象，配合 `P.args`/`P.kwargs` 在装饰器内部转发调用，这样装饰后返回的函数签名仍与原函数（去掉/加上某些参数后）保持一致，检查器能继续校验调用方传的参数。
