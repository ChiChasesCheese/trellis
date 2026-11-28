---
id: hi-c-sd-tinder-b03-bloom-sizing
node: sd.problem-breakdowns.tinder.beyond
type: qa
step: 3
---
## Q
**Tinder · 布隆过滤器要多大**｜拓展 · 加分

给一个已滑过 1 万人的用户建误报率 1% 的布隆过滤器，要多少位、几个哈希函数？比直接存 ID 省多少？

## A
```python
import math

def bloom(n: int, p: float) -> tuple[int, int]:
    # 最优位数 m = -n·ln p / (ln 2)^2；哈希个数 k = (m/n)·ln 2
    m = math.ceil(-n * math.log(p) / math.log(2) ** 2)
    k = round(m / n * math.log(2))
    return m, k

m, k = bloom(10_000, 0.01)
print(m, k, round(m / 8 / 1024, 1), "KiB")  # 95851 7 11.7 KiB
```
- **结果：** 约 9.6 位/元素，共 95,851 位，约 11.7 KiB，7 个哈希函数。
- **对比：** 直接存 1 万个 16 字节 UUID 是 160KB，约为过滤器的 13 倍；存 8 字节整数也有 80KB。
- **取舍：** 误报率每降 10 倍，每元素约多 4.8 位。1% 意味着每 100 个没滑过的人会有约 1 个永远看不到，候选池很大时几乎无感。
- **局限：** 位数固定，元素超过设计容量后误报率迅速升高，要按预期历史上限建，或用可扩展的变种；也不能删除，用户"撤销滑动"需要重建。
