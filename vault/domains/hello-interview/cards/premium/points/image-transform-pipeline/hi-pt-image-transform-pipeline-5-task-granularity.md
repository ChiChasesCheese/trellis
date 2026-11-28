---
id: hi-pt-image-transform-pipeline-5-task-granularity
node: qb.lld.image-transform-pipeline.points
type: qa
step: 5
---
## Q
**图像变换流水线 · 任务粒度与 initializer**｜必会 · 出自：图像变换流水线 › 深入 2

进程池里一个任务该是什么？是"一张图 x 一个变换"，还是"一张图 x 全部变换"？流水线对象怎么送进工作进程？

## A
**粒度。** 一张图 x 全部流水线：图只在进程间传一次。太细（图 x 单个变换）每个任务都要传一遍图；太粗（所有图一个任务）没法负载均衡。

**流水线。** 用 `initializer` 加 `initargs`，每个进程只收一次，任务里只带图。

```python
ProcessPoolExecutor(workers or os.cpu_count(), initializer=_init_worker, initargs=(pipelines,))
```
**失败隔离。** 单张图出错只返回错误字符串，不拖垮整批。
