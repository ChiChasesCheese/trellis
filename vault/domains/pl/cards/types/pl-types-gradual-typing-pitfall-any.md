---
id: pl-types-gradual-typing-pitfall-any
node: types.gradual-typing
type: qa
step: 6
---
## Q
为什么说 `Any` 会在类型检查里「传染」？用 `json.loads` 举一个生产里常见的失败。

## A
`Any` 与所有类型相容，检查器遇到它就放行；一个值是 `Any`，由它派生的值通常也是 `Any`，检查随之一路失效。标准库的 `json.loads` 返回 `Any`，来自外部世界的数据因此直接绕过类型检查：

```python
import json
v: int = json.loads('"text"')
print(v, type(v).__name__)   # text str
```

`mypy` 不报告任何错误，因为右边是 `Any`；运行时输出 `text str`：声明为 `int` 的变量里实际是字符串。

后果在后面才出现：

```python
def load(path: str) -> Any:
    return {"n": "7"}
cfg = load("x")
total: int = cfg["n"] + 1    # mypy 通过
```

配置里的 `n` 是字符串 `"7"`，运行时抛出 `TypeError: can only concatenate str (not "int") to str`。检查器对 `cfg["n"]` 给出的是 `Revealed type is "Any"`，没有任何警告。

为什么危险：类型提示给人「这里已经检查过了」的信心，实际上漏洞就在边界。这比完全没有类型更糟，因为它抑制了本来会写的防御性检查。

对策：

- 在边界把数据校验并转换成具体类型（`pydantic`、`TypedDict` 加手写校验、`int(...)`），不要让 `Any` 进入业务代码。
- 配置检查器禁止显式 `Any` 和隐式 `Any`（如 `disallow_any_explicit`、`disallow_any_generics`），并开启 `warn_return_any`。
- 给自己写的函数写返回类型，不让 `Any` 从你的函数里流出。
