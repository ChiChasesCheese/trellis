"""图像变换流水线（Image Transform Pipeline）：不可变图像、可组合的步骤、尺寸推演、前缀缓存、化简。

核心思路：`Image` 和每个步骤都是不可变的值对象（frozen dataclass），所以它们天然可以比较、可以做字典的键。
流水线就是一个步骤元组，`apply` 从左到右折叠；"尺寸推演"（`output_size`）只算形状不碰像素，所以可以在
真正干活前把非法的流水线整条拒绝。缓存以 (输入图像, 步骤前缀) 为键：两条流水线只要前几步相同，后一条就
直接从缓存里的最长前缀接着算。化简只做"保证等价"的改写，混合正负的亮度调整因为有截断，不能合并。
"""

from __future__ import annotations

from collections import OrderedDict
from dataclasses import dataclass
from typing import Protocol


class PipelineError(Exception):
    """所有失败路径的公共基类。"""


class StepError(PipelineError):
    """流水线里第 `index` 步（从 0 起）作用在当前形状上不合法。"""

    def __init__(self, index: int, step: object, reason: str) -> None:
        super().__init__(f"step {index} ({step!r}): {reason}")
        self.index, self.step, self.reason = index, step, reason


# ---------------------------------------------------------------- 第 1 关：图像与步骤


@dataclass(frozen=True, slots=True)
class Image:
    """灰度图：非空矩形，像素是 0..255 的整数。内部存元组，所以不可变、可哈希。"""

    pixels: tuple[tuple[int, ...], ...]

    def __post_init__(self) -> None:
        rows = tuple(tuple(r) for r in self.pixels)
        if not rows or not rows[0] or any(len(r) != len(rows[0]) for r in rows):
            raise ValueError("image must be a non-empty rectangle")
        if any(type(v) is not int or not 0 <= v <= 255 for r in rows for v in r):
            raise ValueError("pixels must be ints in 0..255")
        object.__setattr__(self, "pixels", rows)

    @property
    def height(self) -> int:
        return len(self.pixels)

    @property
    def width(self) -> int:
        return len(self.pixels[0])


class Step(Protocol):
    def apply(self, image: Image) -> Image: ...
    def output_size(self, height: int, width: int) -> tuple[int, int]: ...


@dataclass(frozen=True, slots=True)
class Flip:
    horizontal: bool  # True 左右镜像，False 上下翻转

    def apply(self, image: Image) -> Image:
        rows = image.pixels
        return Image(tuple(r[::-1] for r in rows) if self.horizontal else rows[::-1])

    def output_size(self, height: int, width: int) -> tuple[int, int]:
        return height, width


@dataclass(frozen=True, slots=True)
class Rotate:
    quarter_turns: int  # 顺时针转几个 90 度，任意整数，按 4 取模

    def apply(self, image: Image) -> Image:
        rows = image.pixels
        for _ in range(self.quarter_turns % 4):
            rows = tuple(zip(*rows[::-1]))  # 顺时针转 90 度：先上下翻转再转置
        return Image(rows)

    def output_size(self, height: int, width: int) -> tuple[int, int]:
        return (width, height) if self.quarter_turns % 2 else (height, width)


@dataclass(frozen=True, slots=True)
class Crop:
    top: int
    left: int
    height: int
    width: int

    def __post_init__(self) -> None:
        if self.top < 0 or self.left < 0 or self.height < 1 or self.width < 1:
            raise ValueError("crop needs top, left >= 0 and height, width >= 1")

    def output_size(self, height: int, width: int) -> tuple[int, int]:
        if self.top + self.height > height or self.left + self.width > width:
            raise ValueError(f"crop reaches outside the {height}x{width} image")
        return self.height, self.width

    def apply(self, image: Image) -> Image:
        self.output_size(image.height, image.width)
        return Image(tuple(r[self.left:self.left + self.width] for r in image.pixels[self.top:self.top + self.height]))


@dataclass(frozen=True, slots=True)
class Brighten:
    delta: int  # 可以为负；每个像素加上它再截断到 0..255

    def apply(self, image: Image) -> Image:
        return Image(tuple(tuple(min(255, max(0, v + self.delta)) for v in r) for r in image.pixels))

    def output_size(self, height: int, width: int) -> tuple[int, int]:
        return height, width


@dataclass(frozen=True, slots=True)
class Invert:
    def apply(self, image: Image) -> Image:
        return Image(tuple(tuple(255 - v for v in r) for r in image.pixels))

    def output_size(self, height: int, width: int) -> tuple[int, int]:
        return height, width


@dataclass(frozen=True, slots=True)
class Resize:
    """最近邻缩放（第 2 关）：目标 (r, c) 取原图 (r*H//新高, c*W//新宽)。放大是复制，缩小是抽样。"""

    height: int
    width: int

    def __post_init__(self) -> None:
        if self.height < 1 or self.width < 1:
            raise ValueError("resize target must be at least 1x1")

    def apply(self, image: Image) -> Image:
        h, w = image.height, image.width
        cols = [c * w // self.width for c in range(self.width)]
        return Image(tuple(tuple(image.pixels[r * h // self.height][c] for c in cols) for r in range(self.height)))

    def output_size(self, height: int, width: int) -> tuple[int, int]:
        return self.height, self.width


@dataclass(frozen=True, slots=True)
class Pipeline:
    steps: tuple[Step, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, "steps", tuple(self.steps))

    def apply(self, image: Image) -> Image:
        for i, step in enumerate(self.steps):
            try:
                image = step.apply(image)
            except ValueError as err:
                raise StepError(i, step, str(err)) from err
        return image

    # ---------------------------------------------------------------- 第 2 关：组合与尺寸推演

    def then(self, step: Step) -> Pipeline:
        return Pipeline(self.steps + (step,))

    def __add__(self, other: Pipeline) -> Pipeline:
        return Pipeline(self.steps + other.steps)

    def __len__(self) -> int:
        return len(self.steps)

    def output_size(self, height: int, width: int) -> tuple[int, int]:
        """只推演形状，不碰像素：非法的步骤在这里就以 StepError 报出。"""
        for i, step in enumerate(self.steps):
            try:
                height, width = step.output_size(height, width)
            except ValueError as err:
                raise StepError(i, step, str(err)) from err
        return height, width

    # ---------------------------------------------------------------- 第 4 关：化简

    def simplified(self) -> Pipeline:
        """返回一个对任何输入都等价、步骤更少（或相同）的流水线。"""
        out: list[Step] = []
        for step in self.steps:
            cur: Step | None = step
            while out and cur is not None and (m := _merge(out[-1], cur)) is not _NO_MERGE:
                out.pop()
                cur = m  # type: ignore[assignment]  # None 表示两步抵消
            if cur is not None and not _is_identity(cur):
                out.append(cur)
        return Pipeline(tuple(out))


_NO_MERGE = object()


def _merge(a: Step, b: Step) -> Step | None | object:
    """相邻两步能合并就返回合并结果（None 表示互相抵消），否则返回 _NO_MERGE。"""
    match a, b:
        case Flip(h1), Flip(h2) if h1 == h2:
            return None
        case Invert(), Invert():
            return None
        case Rotate(n), Rotate(m):
            return Rotate((n + m) % 4)
        # 亮度调整带截断：同号时 min(255, min(255, x+a)+b) == min(255, x+a+b)，可以合并；
        # 一正一负（先 +200 再 -100）截断发生在中途，合并会得到不同的结果。
        case Brighten(d1), Brighten(d2) if d1 * d2 >= 0:
            return Brighten(d1 + d2)
        case _:
            return _NO_MERGE


def _is_identity(step: Step) -> bool:
    return (isinstance(step, Rotate) and step.quarter_turns % 4 == 0) or (isinstance(step, Brighten) and step.delta == 0)


# ---------------------------------------------------------------- 第 3 关：前缀缓存


class CachedRunner:
    """按 (输入图像, 步骤前缀) 缓存每一步的结果，LRU 淘汰，最多 `max_entries` 项。"""

    def __init__(self, max_entries: int) -> None:
        if max_entries < 1:
            raise ValueError("max_entries must be at least 1")
        self._max = max_entries
        self._cache: OrderedDict[tuple[Image, tuple[Step, ...]], Image] = OrderedDict()
        self.steps_executed = 0

    def cache_size(self) -> int:
        return len(self._cache)

    def run(self, pipeline: Pipeline, image: Image) -> Image:
        pipeline.output_size(image.height, image.width)  # 先整体校验：非法流水线不执行任何一步、不污染缓存
        steps = pipeline.steps
        start, current = 0, image
        for k in range(len(steps), 0, -1):               # 从最长的前缀往短找
            hit = self._cache.get((image, steps[:k]))
            if hit is not None:
                self._cache.move_to_end((image, steps[:k]))
                start, current = k, hit
                break
        for k in range(start, len(steps)):
            current = steps[k].apply(current)
            self.steps_executed += 1
            self._cache[(image, steps[:k + 1])] = current
            if len(self._cache) > self._max:
                self._cache.popitem(last=False)
        return current
