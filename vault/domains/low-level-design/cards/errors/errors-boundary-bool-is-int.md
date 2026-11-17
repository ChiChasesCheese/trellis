---
id: errors-boundary-bool-is-int
node: errors.boundary-validation
type: qa
step: 2
---
## Q
`isinstance(x, int)` 能挡住非整数的数量、评分、ID 吗？为什么 `True` 会让校验悄悄通过？

## A
**bool 是 int 的子类，要用 `type(x) is int`**

- **事实**：布尔类型在语言里就是整数的一个子类，`True` 当作 1、`False` 当作 0 参与运算，`isinstance(True, int)` 为 `True`；
- **后果**：请求里的 JSON 布尔值 `true` 被当成数量 1、评分 1、编号 1 收下，数据看着没问题，含义却是错的，之后很难查到是谁传的；
- **精确的挡法**：`type(x) is int` 同时拒绝 `bool` 和所有 `int` 子类；想放行子类，就写 `isinstance(x, int) and not isinstance(x, bool)`；
- **float 不用另外处理**：`3.0` 不是 `int`，`isinstance(3.0, int)` 为 `False`；
- **代价**：这条检查写在边界的一个小函数里，所有入口复用，不要每处各写一遍，否则总有一处忘了排除布尔值。

```python
def valid_qty(x) -> bool:
    return type(x) is int and x > 0

print(isinstance(True, int))                 # True，这就是坑
print(valid_qty(True))                       # False
print(valid_qty(2), valid_qty(2.0), valid_qty("2"))   # True False False
```

<details class="pt"><summary>延伸</summary>

`type(x) is int` 也会拒绝 `IntEnum` 成员。入口数据来自 JSON 或表单时这正是想要的；内部代码里传 `IntEnum` 是合法用法，不要把这条检查复制到内部函数里。

</details>

**知识点：**边界校验（Validate at the Boundary）
