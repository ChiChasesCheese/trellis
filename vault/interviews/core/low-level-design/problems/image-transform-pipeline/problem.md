# 图像变换流水线（Image Transform Pipeline）

一个小型图像处理库：灰度图是一块像素网格，翻转、旋转、裁剪、调亮度、缩放这些操作各是一个"步骤"，把步骤按顺序串起来就是一条流水线。你要设计图像和步骤的类型，让流水线可以组合、可以提前校验、重复运行时不重复劳动。不需要读写文件。

坐标是 `(行, 列)`，从 0 开始。所有类型都是不可变的值：`Image` 与每个步骤都能比较是否相等、能做字典的键。

**分关要求**（做完一关再看下一关）
- 第 1 关（约 25 分钟）：图像、步骤、流水线。
  - `Image(pixels)`：非空矩形，像素是 0 到 255 的整数（布尔值不算）；不合法抛 `ValueError`。传入的列表之后被调用方修改，不能影响图像。属性 `height`、`width`。
  - 步骤，每个都有 `apply(image) -> Image` 和 `output_size(height, width) -> tuple[int, int]`：
    `Flip(horizontal: bool)`（真为左右镜像，假为上下翻转）、`Rotate(quarter_turns: int)`（顺时针，任意整数按 4 取模）、`Crop(top, left, height, width)`（构造时要求 `top`、`left` 不小于 0，`height`、`width` 不小于 1，否则 `ValueError`）、`Brighten(delta: int)`（加 `delta` 后截断到 0 到 255）、`Invert()`（变成 `255 - v`）。
  - `Pipeline(steps)`：`apply(image)` 从左到右依次作用；某一步作用在不合适的图上（比如裁剪超出范围）时抛 `StepError`，带 `index`（第几步，从 0 起）、`step`、`reason`。空流水线原样返回。
  - 例：`Rotate(1)` 把 `[[1,2,3],[4,5,6]]` 变成 `[[4,1],[5,2],[6,3]]`；`Flip(True)` 再 `Rotate(1)` 得到 `[[6,3],[5,2],[4,1]]`。
- 第 2 关（约 20 分钟）：缩放、组合、尺寸推演。
  - `Resize(height, width)`：最近邻缩放，目标 `(r, c)` 取原图 `(r * 原高 // height, c * 原宽 // width)`，放大是复制、缩小是抽样；目标小于 1 抛 `ValueError`。例：`[[1,2,3,4]]` 缩到宽 2 得 `[[1,3]]`。
  - `Pipeline.then(step)`、`pipeline + other` 返回新流水线，原对象不变；`len(pipeline)`；流水线可比较、可哈希。
  - `Pipeline.output_size(height, width)`：只推演形状，不碰像素（输入一百万乘一百万也是瞬间）；不合法的步骤抛 `StepError`，和 `apply` 报同一个 `index`。
  - 步骤的顺序不可交换：先裁剪再缩放与先缩放再裁剪的结果不同。
- 第 3 关（约 15 分钟）：前缀缓存。
  - `CachedRunner(max_entries)`：`run(pipeline, image) -> Image`，结果和 `pipeline.apply(image)` 一样。缓存的键是 `(输入图像, 步骤前缀)`，按值比较；每执行一步就存一项，超出 `max_entries` 淘汰最久未使用的。`max_entries < 1` 抛 `ValueError`。
  - 运行时从最长的已缓存前缀接着算，命中的那项算作最近使用；属性 `steps_executed` 累计真正执行的步数，`cache_size()` 是当前项数。
  - 先用 `output_size` 整体校验：非法流水线抛 `StepError`，不执行任何一步，缓存也不变。
  - 例：容量 10，先跑 `[A,B,C]` 再跑 `[A,B,D]`，第二次只多执行 1 步。
- 第 4 关（选做）：化简。
  - `Pipeline.simplified()` 返回对任何输入都等价、步骤不更多的流水线：相同方向的两个 `Flip` 抵消、两个 `Invert` 抵消、相邻 `Rotate` 合并（转 0 次丢掉）、相邻同号的 `Brighten` 合并（`delta` 为 0 丢掉）；合并后继续与更前面的步骤尝试合并。一正一负的 `Brighten` 不能合并：先加 200 再减 100，在像素 100 上得 155，不是 100 + 100。

**评分点**
- 图像和步骤都是不可变值对象：能比较、能哈希、调用方改自己的列表不会伤到图像。
- 步骤用统一的 `apply` 与 `output_size` 接口，流水线不关心步骤种类，新增一种步骤不改流水线。
- 步骤自己的参数在构造时校验，依赖图像形状的校验在应用时，并统一包装成带 `index` 的 `StepError`。
- 尺寸推演和像素计算分开，所以能在干活之前拒绝非法流水线。
- 缓存键用值而不是对象身份；每个前缀单独存一项；校验在先，失败不污染缓存。
- 能讲清化简为什么只做"保证等价"的改写，以及截断为什么让亮度合并有符号条件。
- LRU 的"命中刷新、插入后淘汰最久"处理正确。
- 能说出换成彩色图、不规则裁剪或大图时，哪些接口会变、哪些不变。
