---
id: craft-validated-construction-3-cross-object-invariants
node: craft.idioms.validated-construction
type: qa
step: 3
---
## Q
**构造即校验 · 哪些不变量构造函数查不了**｜写法

图像流水线的 `Crop(top, left, height, width)` 在构造时检查「各个数不能是负的」，但「裁剪区域不能超出图像」却到 `output_size` 里才检查。为什么不把后者也放进构造函数？这类检查应该放在哪里？

## A
**要点。** 构造函数只能看到自己的字段。「裁剪框要在图像里面」涉及另一个对象（图像尺寸），构造 `Crop` 的时刻图像还不存在，甚至同一个 `Crop` 会用在不同尺寸的图像上。判据：**只依赖自己的字段，就构造时查；还依赖别的对象，就在拥有这个关系的地方查**，也就是把两者放到一起的那个方法或容器。

```python
class StepError(Exception):
    def __init__(self, index: int, reason: str) -> None:
        super().__init__(f"step {index}: {reason}")

@dataclass(frozen=True, slots=True)
class Crop:
    top: int
    left: int
    height: int
    width: int

    def __post_init__(self) -> None:
        # 自己的字段能查的，构造时就查
        if self.top < 0 or self.left < 0 or self.height < 1 or self.width < 1:
            raise ValueError("crop needs top, left >= 0 and height, width >= 1")

    def output_size(self, height: int, width: int) -> tuple[int, int]:
        # 与「别的对象」（图像尺寸）的关系，构造时还不知道，只能在使用时查
        if self.top + self.height > height or self.left + self.width > width:
            raise ValueError(f"crop reaches outside the {height}x{width} image")
        return self.height, self.width

def run(steps: list[Crop], h: int, w: int):
    for i, s in enumerate(steps):
        try:
            h, w = s.output_size(h, w)
        except ValueError as e:
            raise StepError(i, str(e)) from e     # 带上是第几步，才能定位
    return h, w

try:
    Crop(-1, 0, 2, 2)
except ValueError as e:
    print("构造时拒绝:", e)
c = Crop(0, 0, 8, 8)                             # 单看自己是合法的
print("构造成功:", c)
try:
    run([Crop(0, 0, 4, 4), c], 10, 10)
except StepError as e:
    print("放进流水线才发现:", e)
```

实际输出：

```
构造时拒绝: crop needs top, left >= 0 and height, width >= 1
构造成功: Crop(top=0, left=0, height=8, width=8)
放进流水线才发现: step 1: crop reaches outside the 4x4 image
```

**两种选择的代价。** 全放构造函数：做不到，信息不够，硬做会逼着把图像塞进每个步骤里，对象互相缠住。全放使用处：每个使用方都得记得检查，回到「漏掉一个」的老问题。折中是现在的写法：自己的约束留在构造，关系约束收在**一个**入口（`output_size`），流水线只调它，并且报错时带上是第几步。

**易错。** 关系不变量要能提前检查：流水线另有一个 `output_size`，只推演形状、不碰像素，非法的步骤在这里就以 `StepError` 报出，不必等算完前几步的像素。类似的还有「价格要在菜单里」「费率阶梯的币种要和账户一致」。
