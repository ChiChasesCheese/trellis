---
id: craft-rule-chain-pipeline-4-validate-whole-chain-first
node: craft.patterns.rule-chain-pipeline
type: qa
step: 4
---
## Q
**规则链 · 执行前先把整条链「空跑」一遍的元数据**｜模式

流水线 `Resize(100,100) → Crop(200,200)` 的第二步一定会失败，但朴素的 `apply` 要先把第一步（缩放，很贵）算完才会发现。怎样让非法流水线在不处理任何数据的情况下就被拒绝，并指出是第几步？

## A
**要点。** 每个步骤除了 `apply`（动数据）再提供一个便宜的 `output_size`（只推演形状）。流水线先沿着链推演一遍：每步的输出形状是下一步的输入形状，形状不合法的步骤当场抛出，带上步骤序号。通过之后才真正执行。

```python
from dataclasses import dataclass

class StepError(ValueError):
    def __init__(self, index, step, reason):
        super().__init__(f"step {index} {step}: {reason}")

@dataclass(frozen=True)
class Crop:
    h: int; w: int
    def output_size(self, H, W):                # 便宜：只推演形状
        if self.h > H or self.w > W:
            raise ValueError(f"crop {self.h}x{self.w} 大于输入 {H}x{W}")
        return self.h, self.w
    def apply(self, img):                       # 贵：真正处理像素
        print("  (执行 crop)")
        return [row[: self.w] for row in img[: self.h]]

@dataclass(frozen=True)
class Resize:
    h: int; w: int
    def output_size(self, H, W): return self.h, self.w
    def apply(self, img):
        print("  (执行 resize)")
        return [[0] * self.w for _ in range(self.h)]

@dataclass(frozen=True)
class Pipeline:
    steps: tuple
    def output_size(self, H, W):
        """只推演形状，不碰像素：非法的步骤在这里就报出，并带上第几步。"""
        for i, s in enumerate(self.steps):
            try: H, W = s.output_size(H, W)
            except ValueError as e: raise StepError(i, s, str(e)) from e   # from e 保留原因
        return H, W
    def apply(self, img):
        self.output_size(len(img), len(img[0]))    # 先整体校验，再动手
        for s in self.steps: img = s.apply(img)
        return img

p = Pipeline((Resize(100, 100), Crop(200, 200)))   # 第二步必然失败
print("形状推演:", end=" ")
try: p.output_size(8, 8)
except StepError as e: print(e)
print("apply:")
try: p.apply([[1] * 8 for _ in range(8)])
except StepError: print("  拒绝，没有执行任何一步")
```

实际输出：

```
形状推演: step 1 Crop(h=200, w=200): crop 200x200 大于输入 100x100
apply:
  拒绝，没有执行任何一步
```

**为什么。** 省掉的不只是时间：执行到一半失败，留下的是半成品（缓存里多了前缀结果、输出文件写了一半）。前置校验把「失败」变成「没有发生任何事」。`raise ... from e` 保留底层原因，`StepError` 带序号和步骤对象，调用方不用解析消息就能定位。

**代价。** 每个步骤要维护两份逻辑（`apply` 和 `output_size`），它们必须一致；步骤的合法性取决于数据内容（如某个像素值）时，推演不到，只能运行时检查。

**对照。** 数据库的 `EXPLAIN`、编译器的类型检查，都是同一件事：用比执行便宜得多的元数据，提前拒绝执行不了的计划。
