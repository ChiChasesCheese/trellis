"""图像变换流水线（Image Transform Pipeline）——起始模板。公开的类名、签名和异常与 `solution.py` 一致。"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


class PipelineError(Exception):
    """所有失败路径的公共基类。"""


class StepError(PipelineError):
    """流水线里第 `index` 步（从 0 起）作用在当前形状上不合法；带属性 index、step、reason。"""

    def __init__(self, index: int, step: object, reason: str) -> None:
        super().__init__(f"step {index} ({step!r}): {reason}")
        self.index, self.step, self.reason = index, step, reason


@dataclass(frozen=True)
class Image:
    """灰度图：非空矩形，像素是 0..255 的整数（bool 不算）。传入任何行序列，内部存成元组，所以不可变、可哈希。

    空图、行长不一致、像素类型或范围不对，抛 ValueError。提供 height、width 属性。
    """

    pixels: tuple[tuple[int, ...], ...]

    @property
    def height(self) -> int:
        raise NotImplementedError

    @property
    def width(self) -> int:
        raise NotImplementedError


class Step(Protocol):
    def apply(self, image: Image) -> Image: ...
    def output_size(self, height: int, width: int) -> tuple[int, int]: ...


# 每个步骤都是 frozen dataclass（可比较、可哈希）。步骤自己的参数不合法在构造时抛 ValueError；
# 作用在形状不合适的图上时，apply 和 output_size 抛 ValueError（由 Pipeline 包装成 StepError）。


@dataclass(frozen=True)
class Flip:
    """horizontal=True 左右镜像（每行反转），False 上下翻转（行序反转）。"""

    horizontal: bool

    def apply(self, image: Image) -> Image:
        raise NotImplementedError

    def output_size(self, height: int, width: int) -> tuple[int, int]:
        raise NotImplementedError


@dataclass(frozen=True)
class Rotate:
    """顺时针转 quarter_turns 个 90 度，任意整数，按 4 取模。例：[[1,2,3],[4,5,6]] 转 1 次是 [[4,1],[5,2],[6,3]]。"""

    quarter_turns: int

    def apply(self, image: Image) -> Image:
        raise NotImplementedError

    def output_size(self, height: int, width: int) -> tuple[int, int]:
        raise NotImplementedError


@dataclass(frozen=True)
class Crop:
    """取 [top, top+height) x [left, left+width) 的子矩形。构造时 top、left 必须 >= 0，height、width 必须 >= 1。
    超出图像范围时 apply 和 output_size 抛 ValueError。"""

    top: int
    left: int
    height: int
    width: int

    def apply(self, image: Image) -> Image:
        raise NotImplementedError

    def output_size(self, height: int, width: int) -> tuple[int, int]:
        raise NotImplementedError


@dataclass(frozen=True)
class Brighten:
    """每个像素加 delta（可以为负），再截断到 0..255。"""

    delta: int

    def apply(self, image: Image) -> Image:
        raise NotImplementedError

    def output_size(self, height: int, width: int) -> tuple[int, int]:
        raise NotImplementedError


@dataclass(frozen=True)
class Invert:
    """每个像素变成 255 - v。"""

    def apply(self, image: Image) -> Image:
        raise NotImplementedError

    def output_size(self, height: int, width: int) -> tuple[int, int]:
        raise NotImplementedError


@dataclass(frozen=True)
class Resize:
    """第 2 关：最近邻缩放到 height x width（都 >= 1，否则构造时抛 ValueError）。

    目标 (r, c) 取原图 (r * 原高 // height, c * 原宽 // width)：放大是复制，缩小是抽样。
    例：[[1,2,3,4]] 缩到宽 2 得 [[1,3]]。
    """

    height: int
    width: int

    def apply(self, image: Image) -> Image:
        raise NotImplementedError

    def output_size(self, height: int, width: int) -> tuple[int, int]:
        raise NotImplementedError


@dataclass(frozen=True)
class Pipeline:
    """步骤元组；构造时接受任何步骤序列。不可变，可比较、可哈希。"""

    steps: tuple[Step, ...] = ()

    def apply(self, image: Image) -> Image:
        """从左到右依次作用；某一步抛 ValueError，就包装成 StepError(index, step, reason) 抛出。空流水线原样返回。"""
        raise NotImplementedError

    def then(self, step: Step) -> Pipeline:
        """第 2 关：返回追加了一步的新流水线，原对象不变。"""
        raise NotImplementedError

    def __add__(self, other: Pipeline) -> Pipeline:
        """第 2 关：先 self 后 other 的新流水线。"""
        raise NotImplementedError

    def __len__(self) -> int:
        raise NotImplementedError

    def output_size(self, height: int, width: int) -> tuple[int, int]:
        """第 2 关：只推演形状，不碰像素（输入 10**6 x 10**6 也是瞬间）。不合法的步骤抛 StepError。"""
        raise NotImplementedError

    def simplified(self) -> Pipeline:
        """第 4 关：返回对任何输入都等价、步骤更少（或相同）的流水线。至少要做到：
        相同方向的两个 Flip 抵消；两个 Invert 抵消；相邻 Rotate 合并，转 0 次的丢掉；
        相邻同号（都 >= 0 或都 <= 0）的 Brighten 合并，delta 为 0 的丢掉；合并后要继续与更前面的步骤尝试合并。
        一正一负的 Brighten 不能合并（中途有截断）。
        """
        raise NotImplementedError


class CachedRunner:
    """第 3 关：按 (输入图像, 步骤前缀) 缓存每一步的结果，LRU 淘汰，最多 max_entries 项。"""

    steps_executed: int  # 累计真正执行过的步骤数，命中缓存的不算

    def __init__(self, max_entries: int) -> None:
        """max_entries < 1 抛 ValueError。"""
        raise NotImplementedError

    def cache_size(self) -> int:
        raise NotImplementedError

    def run(self, pipeline: Pipeline, image: Image) -> Image:
        """运行流水线并返回结果，结果与 pipeline.apply(image) 相同。

        - 先用 pipeline.output_size 整体校验：非法则抛 StepError，不执行任何一步、缓存不变。
        - 从最长的已缓存前缀接着往后算（k 从 len(steps) 往下找，命中的那一项标为最近使用）。
        - 每执行一步，把 (图像, 前缀) -> 结果存入缓存，超过容量就淘汰最久未使用的一项。
        - 键按值比较：两个内容相同的 Image 对象共用缓存。
        """
        raise NotImplementedError
