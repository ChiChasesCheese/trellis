---
id: errors-boundary-parse-once
node: errors.boundary-validation
type: qa
step: 1
---
## Q
为什么外部输入要在边界处一次性校验、转成可信类型，而不是在每个用到它的函数里各查各的？

## A
**边界解析一次，内部直接信任**

- **边界**：HTTP 处理器、构造函数、配置读取、文件解析，凡是外部数据进来的地方；
- **可信类型**：校验通过后换成已满足约束的值（`int`、冻结的 dataclass），类型本身就是证明；
- **内部**：后面的函数不再重查，只靠类型提示和 `assert` 保护不变量；
- **分散校验的下场**：每层各查一半，总有一条路径漏掉；同一条规则写成几个版本，边界值上互相打架。

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class Limit:
    value: int
    def __post_init__(self):
        if type(self.value) is not int or not 1 <= self.value <= 50:
            raise ValueError("limit must be an int in 1..50")

def recommend(user: str, limit: Limit) -> list[int]:
    return list(range(limit.value))      # 拿到 Limit 就是合法的，不再检查

print(len(recommend("bob", Limit(3))))
```

<details class="pt"><summary>延伸</summary>

“边界”按调用方是谁来定，不按文件位置：一个公共函数既被 HTTP 层调用、又可能被别的模块单独调用，它自己就是边界，要自己校验。只有私有辅助函数才可以信任上一层。

</details>

**知识点：**边界校验（Validate at the Boundary）
