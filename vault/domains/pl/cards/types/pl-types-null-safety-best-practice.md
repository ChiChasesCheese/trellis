---
id: pl-types-null-safety-best-practice
node: types.null-safety
type: qa
step: 5
---
## Q
在有 `null` 的语言里，资深工程师用哪些规则把空值的风险控制住？Rust 里又怎样避免滥用 `unwrap`？

## A
通用原则：让「可能缺失」在类型或契约里可见，让「不可能缺失」在构造时就保证。

- 集合返回空集合，不返回 `null`。调用方遍历就行，不用先判断。
- Java：只在返回值里用 `Optional`，不要用于字段、参数或集合元素；公共方法入口用 `Objects.requireNonNull` 尽早失败；给字段和参数加 `@Nullable`/`@NonNull` 注解，并用 NullAway、Checker Framework 等静态分析在编译时检查。
- Go：构造函数保证返回的对象字段已初始化；返回 `(T, bool)` 或 `(T, error)`，不要用 `nil` 指针表示「没找到」；写 map 之前确认已经 `make`。
- Python：缺失的值在类型提示里写 `str | None`，用 `mypy` 检查。类型检查器会强制你先判断：

```python
def upper(d: dict[str, str], k: str) -> str:
    return d.get(k).upper()
# mypy: Item "None" of "str | None" has no attribute "upper"
```

- Rust：库代码不使用 `unwrap()`，用 `?` 向上传播，用 `ok_or` 把 `Option` 转成 `Result`，用 `if let` 或 `match` 处理缺失。`unwrap()` 只留给测试、示例，或者你能证明不会失败的地方，此时用 `expect("原因")` 写下为什么。
- 不要让 `None`/`null` 同时代表几种含义（未设置、已清空、出错）；需要时用枚举或专门的状态类型。

何时可以破例：热路径上的内部数据结构为避免装箱用 `null` 做哨兵值，是合理的，但要把它封在一个类的内部，不暴露给调用方。
