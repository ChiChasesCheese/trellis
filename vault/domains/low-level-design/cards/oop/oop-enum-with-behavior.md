---
id: oop-enum-with-behavior
node: oop.values
type: qa
step: 5
---
## Q
什么时候带行为的 `Enum`（每个成员各自的字段和方法）比类层次更适合表达变体——又有哪些信号说明你已经用不下 `Enum` 了？

## A
- **Enum 胜出**：变体集合小而封闭，且行为是变体的纯函数：

```python
class VehicleType(Enum):
    CAR = "car"
    SUV = "suv"
    def spot_size(self) -> int:
        return {"car": 1, "suv": 2}[self.value]
```

  常量和逻辑放在一起；配合 `match` 语句，`mypy` 这类静态检查器能对分支的穷尽性给出提示，但这不是语言强制的运行期保证。

- **用不下了**的信号：变体需要各自的可变状态、逻辑差异很大、或者需要开放扩展（不改这个 `Enum` 源码就能加新变体）→ 升级成 `Protocol`/`ABC` + 每个变体一个类（strategy）。
