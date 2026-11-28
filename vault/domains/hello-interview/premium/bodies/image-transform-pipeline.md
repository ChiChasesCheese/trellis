---
slug: image-transform-pipeline
kind: low-level-design
---
## Q
**设计图像变换流水线（并发与分布式扩展）**｜低层设计

一个图片目录里有上万张图（分大图、小图两个子目录），另有一个目录存放变换定义：每个 JSON 文件是一个变换列表，形如 `[{"transform": "mirror", "arg": []}, ...]`，每个文件有若干步。要求对每张图应用每个变换文件，保存结果。分三步给：先写串行版本；再用线程、进程等并发提速；最后讨论百万张图、图片和输出分散在不同位置时怎么分布式处理（队列、多个工作进程）。面试官看重的是：图像和变换怎么建模、能不能提前发现非法变换、并发为什么用进程不用线程、重复劳动怎么省，以及分布式的任务切分和幂等。

给出完整解答：需求、核心实现、逐步扩展、深入问题、取舍、不同级别的期望。

## A
**一句话。** 图像和每个变换都是不可变的值对象，变换列表按名字注册、从 JSON 构造成流水线；串行版先写正确，再用"一张图 x 全部流水线"当作并发的任务单位，进程池并行；规模放大后把图片清单切成批、放进队列，输出位置由内容决定，重复投递也安全。

**60 分钟路线。**

| 时间 | 做什么 |
|---|---|
| 0–6 分 | 问清：变换种类和参数、图的格式与大小、输出放哪、出错怎么办；估算总量 |
| 6–12 分 | 定实体：`Image`、`Step`、`Pipeline`、注册表；画"图 x 变换文件"的循环 |
| 12–38 分 | 写核心实现：值对象、几种变换、流水线、从 JSON 构造 |
| 38–42 分 | 跑例子：旋转、镜像加旋转、越界裁剪的错误、JSON 构造 |
| 42–60 分 | 追问：并发（为什么是进程）、提前校验、前缀缓存、分布式 |

**需求。**
- 功能：
  - 变换文件是列表，每项 `{"transform": 名字, "arg": 参数列表}`，按顺序依次作用；
  - 变换有镜像、翻转、旋转、裁剪、调亮度等，新增一种变换不改流水线；
  - 某一步不合法（例如裁剪超出图的范围）要报出是第几步，不影响其他图；
  - 对每张图应用每个变换文件，各自保存结果。
- 非功能：
  - 先串行正确，再并行；
  - 不可变数据：缓存、跨进程传递都安全；
  - 规模：10,000 张图 x 200 个变换文件 = 2,000,000 个输出；百万张图时 1,000,000 x 200 = 2 亿个输出。
- **单输出约 20 ms：** 假设（每个输出平均 20 ms，含全部步骤；用现成的图像库时的量级）：
  - 串行 10,000 x 200 x 0.02 s = 40,000 s ≈ 11.1 小时；8 个进程理想情况约 1.4 小时；
  - 百万张图：1,000,000 x 200 x 0.02 s = 4,000,000 核秒 ≈ 1,111 核小时；1,000 个并行核约 1.1 小时。

**核心实体与接口。**
- `Image`：灰度图，像素是元组的元组，构造时拷贝并校验；不可变、可哈希、可 pickle。
- `Step`（`Protocol`）：只要求有 `apply(image) -> Image`，步骤不必继承任何基类。
- 变换：`Flip`、`Rotate`、`Crop`、`Brighten`，各是 `frozen=True, slots=True` 的数据类，参数是字段，自动得到按值比较和哈希。
- `Pipeline`：步骤元组，`apply` 从左到右折叠；失败统一包装成 `StepError(index, step, reason)`。
- **REGISTRY 加变换只加一行：** `REGISTRY` 与 `Pipeline.from_json`：名字到类的映射，加一种变换只加一行。
- 约定：参数自己的合法性（例如裁剪高度至少 1）在构造时校验；依赖图像形状的合法性（裁剪是否越界）在应用时校验。

**整体设计。** 外层是两层循环：图 x 变换文件。
1. 读一张图，解码成 `Image`（只做一次）；
2. 对每个变换文件，`Pipeline.from_json(json.loads(path.read_text()))`（每个文件只构造一次，不要在图的循环里重复解析）；
3. `pipeline.apply(image)`，成功就保存，失败记下 `StepError` 的 `index` 和原因；
4. 并发时，任务单位是"一张图 x 全部流水线"，见逐步扩展 1。

真实任务里图像库（例如 Pillow）会替你做像素运算：把它包进同一个 `Step` 接口的 `apply` 里，类型、流水线、校验、并发、缓存的结构完全一样；面试官允许用任何库时，这是更省时间的做法。下面的代码用纯 Python 写像素，是为了自包含、可运行。

**核心实现。** 约 30 分钟，下面是全部要写的代码：

```python
from dataclasses import dataclass
from typing import Protocol


class PipelineError(Exception): ...


class StepError(PipelineError):
    """第 index 步（从 0 起）作用在当前图上不合法。"""
    def __init__(self, index: int, step: object, reason: str) -> None:
        super().__init__(f"step {index} ({step!r}): {reason}")
        self.index, self.step, self.reason = index, step, reason


@dataclass(frozen=True, slots=True)
class Image:
    """灰度图。内部存元组的元组：不可变、可哈希、可跨进程传递。"""
    pixels: tuple[tuple[int, ...], ...]

    def __post_init__(self) -> None:
        rows = tuple(tuple(r) for r in self.pixels)             # 拷贝：调用方之后改自己的列表伤不到图像
        if not rows or not rows[0] or any(len(r) != len(rows[0]) for r in rows):
            raise ValueError("image must be a non-empty rectangle")
        if any(type(v) is not int or not 0 <= v <= 255 for r in rows for v in r):
            raise ValueError("pixels must be ints in 0..255")
        object.__setattr__(self, "pixels", rows)                # 冻结对象里做一次规范化

    @property
    def height(self) -> int:
        return len(self.pixels)

    @property
    def width(self) -> int:
        return len(self.pixels[0])


class Step(Protocol):                                           # 结构化类型：步骤不必继承任何基类
    def apply(self, image: Image) -> Image: ...


@dataclass(frozen=True, slots=True)
class Flip:
    horizontal: bool                                            # True 左右镜像，False 上下翻转

    def apply(self, image: Image) -> Image:
        rows = image.pixels
        return Image(tuple(r[::-1] for r in rows) if self.horizontal else rows[::-1])


@dataclass(frozen=True, slots=True)
class Rotate:
    quarter_turns: int                                          # 顺时针转几个 90 度，任意整数按 4 取模

    def apply(self, image: Image) -> Image:
        rows = image.pixels
        for _ in range(self.quarter_turns % 4):
            rows = tuple(zip(*rows[::-1]))                      # 顺时针转 90 度：先上下翻转再转置
        return Image(rows)


@dataclass(frozen=True, slots=True)
class Crop:
    top: int
    left: int
    height: int
    width: int

    def __post_init__(self) -> None:                            # 只看参数自己的校验放构造时
        if self.top < 0 or self.left < 0 or self.height < 1 or self.width < 1:
            raise ValueError("crop needs top, left >= 0 and height, width >= 1")

    def apply(self, image: Image) -> Image:                     # 依赖图像形状的校验放应用时
        if self.top + self.height > image.height or self.left + self.width > image.width:
            raise ValueError(f"crop reaches outside the {image.height}x{image.width} image")
        return Image(tuple(r[self.left:self.left + self.width] for r in image.pixels[self.top:self.top + self.height]))


@dataclass(frozen=True, slots=True)
class Brighten:
    delta: int                                                  # 可以为负；加完截断到 0..255

    def apply(self, image: Image) -> Image:
        return Image(tuple(tuple(min(255, max(0, v + self.delta)) for v in r) for r in image.pixels))


@dataclass(frozen=True, slots=True)
class Pipeline:
    steps: tuple[Step, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, "steps", tuple(self.steps))    # 传列表也行：规范成元组才可比较、可哈希

    def apply(self, image: Image) -> Image:
        for i, step in enumerate(self.steps):
            try:
                image = step.apply(image)
            except ValueError as err:
                raise StepError(i, step, str(err)) from err     # 统一包装成带第几步的错误
        return image

    @classmethod
    def from_json(cls, spec: list[dict]) -> "Pipeline":
        """[{"transform": "mirror", "arg": []}, ...]：名字到类的注册表，加一种变换只加一行。"""
        return cls(tuple(REGISTRY[d["transform"]](*d.get("arg", [])) for d in spec))


REGISTRY = {"mirror": lambda: Flip(True), "flip": lambda: Flip(False), "rotate": Rotate, "crop": Crop, "brighten": Brighten}
```

**运行。**
- **Rotate 与 mirror 示例：** `Rotate(1)` 把 `[[1,2,3],[4,5,6]]` 变成 `[[4,1],[5,2],[6,3]]`；先 `mirror` 再 `rotate` 一次（`from_json` 构造）得到 `[[6,3],[5,2],[4,1]]`；
- **StepError 带 index：** 三步流水线 `mirror`、`crop [0,0,3,1]`、`brighten [5]` 作用在 2 x 3 的图上：抛 `StepError`，`index` 是 1，原因 `crop reaches outside the 2x3 image`；
- **构造时校验参数：** `Crop(-1, 0, 1, 1)` 在构造时就抛 `ValueError`；
- **Image 防御性拷贝：** 传进 `Image` 的列表之后被改（`raw[0][0] = 99`），图像不受影响；相同像素的两个图像哈希相等；
- **Brighten 截断到 0 和 255：** `Brighten(300)` 把每个像素截断成 `255`，`Brighten(-300)` 截断成 `0`。

**逐步扩展。**
1. 【追问再讲】并发：触发"现在要对上万张图提速"。纯 Python 的像素循环占着 GIL，线程并行不了，所以用进程池；任务单位是"一张图 x 全部流水线"，图只在进程间传一次；流水线通过 `initializer` 每个进程只收一次，不用每个任务都带；单张失败只记一条错误，不拖垮整批。`Image` 和步骤都是冻结的数据类，所以能直接 pickle，错误转成字符串再传回。

```python
import os
from concurrent.futures import ProcessPoolExecutor

_PIPELINES: dict[str, Pipeline] = {}


def _init_worker(pipelines: dict[str, Pipeline]) -> None:
    global _PIPELINES
    _PIPELINES = pipelines                        # 流水线每个进程只收一次，任务里只带图


def run_image(task: tuple[str, Image]) -> tuple[str, dict[str, Image | str]]:
    """一个任务 = 一张图 x 全部流水线。失败只记一条错误，不拖垮整批。"""
    name, image = task
    results: dict[str, Image | str] = {}
    for pname, pipeline in _PIPELINES.items():
        try:
            results[pname] = pipeline.apply(image)
        except StepError as err:
            results[pname] = str(err)             # 错误转成字符串再跨进程
    return name, results


def run_batch(images: dict[str, Image], pipelines: dict[str, Pipeline], workers: int | None = None):
    # 纯 Python 的像素循环占着 GIL，线程并行不了，所以用进程；Image 和步骤都是冻结的数据类，可以 pickle
    with ProcessPoolExecutor(workers or os.cpu_count(), initializer=_init_worker, initargs=(pipelines,)) as pool:
        return dict(pool.map(run_image, images.items(), chunksize=4))
```

2. 【追问再讲】形状推演与更多变换：触发"200 个变换文件里有几个裁剪会越界，能不能干活之前就知道"。每个步骤多一个 `output_size`，只算形状不碰像素，`Pipeline.output_size` 把整条流水线推演一遍；大图、小图两个子目录就是两种形状，200 个文件 x 2 种形状 = 400 次推演，几乎免费，非法的流水线在碰第一张图之前就整条拒绝。同时加入 `Invert` 和最近邻缩放 `Resize`，以及组合用的 `then`、`+`、`len`（返回新对象，原对象不变）。

```python
class Step(Protocol):
    def apply(self, image: Image) -> Image: ...
    def output_size(self, height: int, width: int) -> tuple[int, int]: ...      # 新：只推演形状，不碰像素


class Flip:  # 只列出新增或替换的方法
    def output_size(self, height: int, width: int) -> tuple[int, int]:
        return height, width


class Rotate:  # 只列出新增或替换的方法
    def output_size(self, height: int, width: int) -> tuple[int, int]:
        return (width, height) if self.quarter_turns % 2 else (height, width)


class Brighten:  # 只列出新增或替换的方法
    def output_size(self, height: int, width: int) -> tuple[int, int]:
        return height, width


class Crop:  # 只列出新增或替换的方法
    def output_size(self, height: int, width: int) -> tuple[int, int]:
        if self.top + self.height > height or self.left + self.width > width:
            raise ValueError(f"crop reaches outside the {height}x{width} image")
        return self.height, self.width

    def apply(self, image: Image) -> Image:                     # 校验与形状推演共用同一个函数
        self.output_size(image.height, image.width)
        return Image(tuple(r[self.left:self.left + self.width] for r in image.pixels[self.top:self.top + self.height]))


@dataclass(frozen=True, slots=True)
class Invert:
    def apply(self, image: Image) -> Image:
        return Image(tuple(tuple(255 - v for v in r) for r in image.pixels))

    def output_size(self, height: int, width: int) -> tuple[int, int]:
        return height, width


@dataclass(frozen=True, slots=True)
class Resize:
    """最近邻缩放：目标 (r, c) 取原图 (r*H//新高, c*W//新宽)。放大是复制，缩小是抽样。"""
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


REGISTRY.update({"invert": Invert, "resize": Resize})


class Pipeline:  # 只列出新增或替换的方法
    def output_size(self, height: int, width: int) -> tuple[int, int]:
        """只推演形状：非法的步骤在这里就以 StepError 报出，和 apply 报同一个 index。"""
        for i, step in enumerate(self.steps):
            try:
                height, width = step.output_size(height, width)
            except ValueError as err:
                raise StepError(i, step, str(err)) from err
        return height, width

    def then(self, step: Step) -> "Pipeline":                   # 组合返回新对象，原对象不变
        return Pipeline(self.steps + (step,))

    def __add__(self, other: "Pipeline") -> "Pipeline":
        return Pipeline(self.steps + other.steps)

    def __len__(self) -> int:
        return len(self.steps)
```

3. 【追问再讲】前缀缓存：触发"200 个变换文件前几步很可能相同，别重复算"。缓存的键是 `(输入图像, 步骤前缀)`，每执行一步存一项，从最长的已缓存前缀接着算，LRU 淘汰。先用 `output_size` 校验：非法流水线不执行任何一步，缓存也不脏。

```python
from collections import OrderedDict


class CachedRunner:
    """按 (输入图像, 步骤前缀) 缓存每一步的结果，LRU 淘汰，最多 max_entries 项。"""
    def __init__(self, max_entries: int) -> None:
        if max_entries < 1:
            raise ValueError("max_entries must be at least 1")
        self._max = max_entries
        self._cache: OrderedDict[tuple[Image, tuple[Step, ...]], Image] = OrderedDict()
        self.steps_executed = 0

    def cache_size(self) -> int:
        return len(self._cache)

    def run(self, pipeline: Pipeline, image: Image) -> Image:
        pipeline.output_size(image.height, image.width)          # 先整体校验：非法流水线不执行任何一步、不污染缓存
        steps = pipeline.steps
        start, current = 0, image
        for k in range(len(steps), 0, -1):                       # 从最长的前缀往短找
            hit = self._cache.get((image, steps[:k]))
            if hit is not None:
                self._cache.move_to_end((image, steps[:k]))      # 命中刷新最近使用
                start, current = k, hit
                break
        for k in range(start, len(steps)):
            current = steps[k].apply(current)
            self.steps_executed += 1
            self._cache[(image, steps[:k + 1])] = current        # 每个前缀单独存一项
            if len(self._cache) > self._max:
                self._cache.popitem(last=False)                  # 淘汰最久未用
        return current
```

4. 【加分】化简：触发"相邻的变换能不能合并"。只做保证等价的改写：同方向的两次镜像抵消，两次反相抵消，相邻旋转合并，同号亮度合并。一正一负的亮度不能合并：先加 200 再减 100，在像素 100 上得 155，不是 200。

```python
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


class Pipeline:  # 只列出新增或替换的方法
    def simplified(self) -> "Pipeline":
        """返回对任何输入都等价、步骤更少（或相同）的流水线：栈里新步骤与栈顶尝试合并，成功就继续往下试。"""
        out: list[Step] = []
        for step in self.steps:
            cur: Step | None = step
            while out and cur is not None and (m := _merge(out[-1], cur)) is not _NO_MERGE:
                out.pop()
                cur = m
            if cur is not None and not _is_identity(cur):
                out.append(cur)
        return Pipeline(tuple(out))
```

5. 【加分】分布式：触发"百万张图，图片和输出在不同的地方，有很多工作进程"。任务是"一批图 x 全部变换"；输出位置由 `(图, 变换内容)` 的哈希决定，同一个任务被重复投递会写到同一个位置，覆盖自己。

```python
import hashlib
import json
from itertools import batched


def output_key(image_id: str, spec: list[dict]) -> str:
    """输出位置由 (图, 变换内容) 决定：同一个任务被重复投递，写到同一个位置，覆盖自己即可。"""
    canonical = json.dumps(spec, sort_keys=True, separators=(",", ":"))
    return f"{image_id}/{hashlib.sha256(canonical.encode()).hexdigest()[:16]}.png"


def make_jobs(manifest: list[str], spec_ids: list[str], per_job: int = 50) -> list[dict]:
    """清单切成每批 per_job 张图的任务：一条队列消息 = 一批图 x 全部变换。"""
    return [{"job": i, "images": list(chunk), "specs": spec_ids} for i, chunk in enumerate(batched(manifest, per_job))]
```

**运行（逐步扩展）。**
- 并发：一次本机实测，48 张 400 x 400 的图、4 条正常流水线加 1 条故意越界的：串行 3.33 秒，8 个线程 3.36 秒（没有提速），8 个进程 0.93 秒；三种方式的结果逐项相等，越界那条在结果里是错误字符串 `step 0 (Crop(...)): crop reaches outside the 400x400 image`；
- 形状：`rotate` 后 `crop [0,0,4,1]` 作用在 2 x 4 上，`output_size` 得 `(4, 1)`；顺序换成先裁剪抛 `StepError`，`index` 是 0；
- 前缀缓存：先跑 `[镜像, 反相, 亮度+10]` 执行 3 步，再跑 `[镜像, 反相, 旋转]` 只多执行 1 步（累计 4 步），缓存里共 4 项；
- 化简：`[Rotate(1), Rotate(3), Flip(True), Flip(True), Brighten(5), Brighten(7)]` 化简成 `(Brighten(delta=12),)`；`[Brighten(200), Brighten(-100)]` 不变；
- 分布式：变换内容的键顺序不同（`{"arg":[1],"transform":"rotate"}` 与 `{"transform":"rotate","arg":[1]}`）得到同一个输出路径；120 张图按每批 50 张切成 3 个任务，大小是 `[50, 50, 20]`；
- 三层整合（核心加逐步扩展 2、3、4）：对同一套组合代码跑完整的单元测试，共 27 项全部通过。

**深入。**
1. 【必讲】值对象加统一接口：
   - 图像和步骤都用 `@dataclass(frozen=True, slots=True)`：自动得到按值比较、哈希和不可变，`slots` 去掉每个实例的字典。普通类要手写 `__eq__` 和 `__hash__`，漏了哈希就不能做缓存键，也不方便跨进程传（不可变值对象）；
   - `Image.__post_init__` 里用 `object.__setattr__` 在冻结对象上做一次规范化（拷贝成元组并校验）：普通赋值会被冻结拦下；不规范化，就要把"拷贝并校验"放在每个调用点；
   - 步骤接口用 `typing.Protocol`：结构化类型，步骤不必继承任何基类，类型检查器也能检查 `Pipeline` 里放的东西（鸭子类型加静态检查）；
   - 参数合法性在构造时，形状合法性在应用时，统一包装成带 `index` 的 `StepError`。
2. 【必讲】并发为什么是进程：
   - 工作是 CPU 密集的纯计算，线程要抢 GIL，实测 8 个线程 3.36 秒，和串行的 3.33 秒一样；进程 0.93 秒。若像素运算在 C 里完成并释放 GIL（Pillow、numpy 大多如此），线程也能并行；读取文件是 I/O 等待，线程适合做预取；
   - 任务粒度：一张图 x 全部流水线。粒度太细（图 x 单个变换）每个任务都要把图传一遍；粒度太粗（所有图一个任务）没法负载均衡。`pool.map` 的 `chunksize` 减少调度开销；
   - 流水线用 `initializer` 每个进程只送一次；失败隔离：单张图出错只返回错误字符串。
3. 【必讲】规模放大后的分布式切分：
   - 切分单位：图片清单切成每批 50 张的任务；一个任务 = 50 x 200 = 10,000 个输出，按每个输出 20 ms 约 200 秒，够长以摊薄队列开销，又够短以便失败后重做。百万张图共 1,000,000 ÷ 50 = 20,000 个任务；
   - 队列语义：至少一次投递加可见性超时。工作进程处理完才确认；崩溃后任务重新出现，所以必须幂等：输出位置由 `(图, 变换内容)` 的哈希决定，重复执行就是覆盖同一个文件；
   - 毒丸：某张图总是失败，重试几次后进死信队列，不阻塞整批；
   - 数据在哪里：图片在不同的地方时，清单里放完整地址，工作进程就近读取、写到对应的输出位置；工作进程无状态，按队列深度自动扩缩；
   - 队列选择：不需要顺序保证，选普通的工作队列（竞争消费）；若用 Kafka，并行度受分区数限制，要先把分区数开够。
4. 【追问再讲】提前校验：`output_size` 只算形状，输入一百万乘一百万也是瞬间；"先跑一遍看会不会出错"在大图上很贵，还会让半截结果污染缓存。
5. 【追问再讲】前缀缓存的键与代价：
   - 键用值（图像内容）不用 `id(image)`：内容相同的另一个对象仍命中，对象被回收后 `id` 还可能被复用造成错误命中；
   - `OrderedDict` 的 `move_to_end` 刷新、`popitem(last=False)` 淘汰，两个调用就是 LRU；
   - 每项是一张完整的中间图，缓存按项数限制容易撑爆内存：要按字节计量，或只缓存每隔几步的前缀。
6. 【追问再讲】化简里的 `match`：`_merge` 同时按两个步骤的类型和字段分派（`case Rotate(n), Rotate(m)`），守卫 `if d1 * d2 >= 0` 直接写在规则旁边；`isinstance` 链读起来要先拆字段再比较（代数数据类型上的模式匹配）。合并成功就弹出栈顶继续往下试，所以合并会级联。
7. 【加分】换成彩色图、numpy 或 GPU：像素从整数变成元组或数组，`Image` 的校验和逐像素的步骤变化；流水线、注册表、缓存、并发、队列都不变，这正是统一接口的好处。
8. 【加分】可观测与重试：每个输出的结果（成功或错误）按任务汇总；失败率、每任务耗时、队列深度是三个要看的指标。

**取舍与追问。** 按被问到的可能性排，通常口述就够：
- 一次性读入 10,000 张图会不会爆内存：不会一次全读，任务里一张一张读、算完就释放；大图和小图分目录，可以按形状分任务，便于估算内存。
- 进程数怎么定：CPU 核数附近；任务大图小图差异大时让 `chunksize` 小一些做负载均衡。
- 输出保存的格式与目录结构：按输入图加变换文件名的哈希组织路径，便于幂等和清理。
- 步骤能否并行：流水线内每步依赖上一步，不能并；同一步内可按行分块，但不如在图与图之间并行划算。
- **CPU 密集线程池无用：** 为什么不用 `ThreadPoolExecutor` 加 `asyncio`：对 CPU 密集没有帮助，只对读写文件的 I/O 等待有用。

**级别期望。**
- 中级：核心实现通过，变换和流水线正确，能说出为什么要并发，并给出可运行的进程池版本。
- 高级：不可变值对象、统一接口、注册表；进程池的任务粒度与失败隔离；提前校验形状；前缀缓存。
- 资深/专家：分布式的任务切分、幂等输出位置、至少一次投递、毒丸与死信；用数字推导规模；队列与分区的取舍；换成图像库、numpy 或 GPU 时哪些接口不变。

**先修概念。**
- [[hi-low-level-design-in-a-hurry-patterns|设计模式]]
- [[hi-low-level-design-in-a-hurry-oop-concepts|面向对象概念]]
- [[hi-low-level-design-concurrency-intro|并发入门]]
- [[hi-system-design-patterns-scaling-writes|扩展写]]
- [[hi-system-design-patterns-long-running-tasks|长时间运行的任务]]

**同类题。**
- [[solution-thread-pool|设计题解：线程池]]
- [[solution-amz-dag-runner|设计题解：DAG 任务执行器]]
- [[solution-task-scheduler|设计题解：任务调度]]
