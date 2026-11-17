---
id: errors-values-result-object
node: errors.exceptions-vs-values
type: qa
step: 3
---
## Q
图片流水线一次处理一批图，每张图要依次做若干变换。某张图的变换失败，别的图照常处理。这里该抛异常，还是把失败放进返回值？

## A
**失败本身就是数据时，用结果对象**

- **批处理里的失败是正常输出**：调用方要的是“每张图各自的结果”，一张图抛异常会中断整批，别的图的结果也拿不到；
- **结果对象**：`data` 和 `error` 放在同一个值里，调用方遍历结果就够了，不需要 `try`；
- **异常转成值只在一个地方做**：边界函数里统一 `except Exception`，里面的变换代码照常抛；
- **只转 `Exception`**：`KeyboardInterrupt` 和 `SystemExit` 不是这张图的失败，原样冒出去；
- **失败的那张图立即停**：它后面的变换不再执行，`data` 是 `None`。

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class Result:
    data: object = None
    error: str | None = None

def run(steps, x) -> Result:
    try:
        for step in steps: x = step(x)       # 一步失败，后面的不再执行
        return Result(data=x)
    except Exception as e:                   # 转成值只在这一处
        return Result(error=f"{type(e).__name__}: {e}")

print(run([int, abs], "-7"), run([int, abs], "x"), sep="\n")
```

**知识点：**异常与错误值（Exceptions vs Values）
