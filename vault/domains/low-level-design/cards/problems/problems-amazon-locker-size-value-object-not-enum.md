---
id: problems-amazon-locker-size-value-object-not-enum
node: problems.machines.amazon-locker
type: qa
step: 1
tags: [grown]
---
## Q
在快递柜（Amazon Locker）设计里，柜格尺寸用 `IntEnum`（S/M/L 三档）表达有什么隐患？换成什么？

## A
隐患是**档位集合在导入时就封死了**：机考第 4 关加一种超大格时，要改枚举定义、改所有 `if size >= ...`，而枚举值通常已经被序列化进数据库和消息，改它等于一次数据迁移。它还默认尺寸是全序的，可真实柜格不是——又高又窄和又矮又宽哪个更大？

换成带三维的**值对象**（value object，不可变、可哈希、按值相等的小对象）：

```python
@dataclass(frozen=True, slots=True)
class Size:
    name: str
    width: int
    depth: int
    height: int

    def accommodates(self, other: "Size") -> bool:
        return (self.width >= other.width
                and self.depth >= other.depth
                and self.height >= other.height)
```

判据很硬：分配逻辑里不许出现任何一个具体尺寸名，循环跑的是当前有空柜的那些尺寸类。做到了，新增尺寸就是多造一个 `Size` 对象，分配代码一行不改。
