---
id: msd-training-pipeline-versioning-cache
node: training.pipeline
type: qa
step: 2
---
## Q
训练流水线为什么要像代码一样版本化？怎样做到"某一步失败只重跑这一步"？用 DVC 举例。

## A
**为什么版本化**：一个模型由三样东西共同决定——**代码、数据、配置**。三者任一变化，模型都会变。线上出问题时你要回答"这个模型是用哪份数据、哪版代码、哪组参数训练的"，答不出来就无法复现，也无法安全回滚。

**缓存与增量重跑的原理**：把每一步看成一个纯函数，输出只由输入决定。
- 对每一步的输入（上游产物的内容哈希 + 这一步代码的哈希 + 参数）算一个键。
- 键没变，就直接复用上次的输出；键变了，才重跑这一步及其下游。
- 和 Make、Bazel 这类构建工具的思路一样。

**DVC 的写法**：在 `dvc.yaml` 里声明每个阶段的命令、依赖和输出。
```yaml
stages:
  features:
    cmd: python features.py
    deps: [features.py, data/raw]
    params: [features.window_days]
    outs: [data/features]
  train:
    cmd: python train.py
    deps: [train.py, data/features]
    params: [train.lr, train.epochs]
    outs: [models/model.pt]
    metrics: [metrics.json]
```
- `dvc repro`：只重跑依赖变化了的阶段。
- `dvc.lock` 记下每个依赖和输出的哈希，提交进 git，代码版本就绑定了数据版本。
- 大文件本体存在远端（S3 等），git 里只有指针。

**收益的量级**：特征转换 3 小时、训练 6 小时。只改了训练学习率，重跑只需 6 小时而不是 9 小时；训练在第 5 小时失败，从检查点继续只损失几十分钟。

**常见坑**：步骤里读了"当前时间"或"最新分区"，输出不再只由声明的输入决定，缓存就会给出错误结果。时间窗口必须作为显式参数传入。
