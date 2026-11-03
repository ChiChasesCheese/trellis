---
id: hi-lld-amazon-locker-9-extend-fallback-maint
node: lld.problem-breakdowns.amazon-locker.exam
type: qa
step: 9
---
## Q
**扩展：尺寸降级与故障格口**｜低层设计 · 题目拆解

快递柜设计完成后，面试官追问两个扩展：中格口满了能否用大格口代替；格口门损坏或维护时怎么处理。请说明对类的改动。

## A
**尺寸降级。** 只改 `get_available_compartment`：按尺寸顺序先找请求的尺寸，找不到再往更大的尺寸找（中件先中后大，小件先小后中再大），永不向下降级，因为放不进去。

```python
ORDER = [Size.SMALL, Size.MEDIUM, Size.LARGE]

def get_available(self, size: Size) -> Compartment | None:
    for s in ORDER[ORDER.index(size):]:
        for c in self.compartments:
            if c.size == s and c.is_available():
                return c
    return None
```

**维护状态。** 用状态枚举（AVAILABLE、OCCUPIED、OUT_OF_SERVICE）取代布尔的 `occupied`，加上 `mark_out_of_service` 和 `mark_in_service`；分配时只认 `is_available()`，故障格口自然被跳过。

**要点。** 好的设计让这类变化只落在一处，分配逻辑收在一个方法里。
