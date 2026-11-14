---
id: msd-training-experiments-what-to-log
node: training.experiments
type: qa
step: 1
---
## Q
一次训练实验要记录哪些信息，才能在三个月后复现它、或解释它为什么比另一次好？用 MLflow 写出记录代码。

## A
**原则**：模型 = 代码 × 数据 × 配置 × 环境 × 随机性。五样都记下来，才谈得上复现。

- **代码版本**：git 提交号，以及工作区有没有未提交的改动（有改动的实验不可复现，应拒绝或把 diff 一起存）。
- **数据版本**：训练集和测试集的路径、分区、行数和内容哈希；特征转换参数（均值、词表）的版本。
- **配置**：全部超参数（人设定、不由训练自动学出来的数，如学习率、批大小、训练轮数），包括默认值。
- **环境**：Python 包版本（`pip freeze` 或锁文件）、CUDA 和驱动版本、GPU 型号与卡数、容器镜像摘要。
- **随机种子**：所有随机数生成器的种子。
- **结果**：每步的训练损失和验证指标、最终测试指标、训练时长、产出的模型文件路径。

```python
import mlflow
with mlflow.start_run(run_name="rank-v13-lr3e-4"):
    mlflow.set_tags({"git_commit": commit, "data_version": "impr_2026_10_01_28d"})
    mlflow.log_params({"lr": 3e-4, "batch_size": 4096, "epochs": 3, "seed": 17})
    for step, loss in train():
        mlflow.log_metric("train_loss", loss, step=step)
    mlflow.log_metrics({"test_auc": 0.812, "test_logloss": 0.231})
    mlflow.log_artifact("requirements.lock")
    mlflow.log_artifact("model.pt")
```

**常用工具**：MLflow、Weights & Biases（`wandb.init(config=...)`）、TensorBoard（只管曲线）。工具不重要，重要的是**自动记录**：在训练脚本入口统一采集，不靠人手填。

**为什么值得**：线上模型出问题时，能从模型注册表的一条记录追到它的数据、代码和配置；两个实验结果不同时，能逐项比较差异在哪，而不是凭记忆猜。
