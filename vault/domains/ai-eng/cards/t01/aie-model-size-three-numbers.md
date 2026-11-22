---
id: aie-model-size-three-numbers
node: t01.model-size-parameters-scaling-law
type: qa
step: 1
tags: [先修]
---
## Q
**Model size · 看模型规模的三个数**｜先修 · 必会

模型名字里常带 `7B`、`70B`。这个数是什么？光看它能不能判断模型强弱和运行成本？

## A
**一句话：** `7B` 是 **parameter**（模型里训练出来的数字，也叫权重）的个数：7 billion = 70 亿。参数越多，模型能学的东西越多，也越占内存。

**衡量规模要看三个数：**

| 数 | 代表什么 |
|---|---|
| parameters 个数 | 学习容量 |
| 训练用的 token 数（**training tokens**） | 学了多少 |
| **FLOPs**（floating point operations，浮点运算次数） | 训练的算力开销 |

- 训练 token 数 ≠ 数据集 token 数：数据集 1 万亿 token 训练 2 个 **epoch**（把数据集完整过一遍叫一个 epoch），training tokens 就是 2 万亿。
- 数据集常按 token 数而不是篇数算，因为一篇长文和一句话差得太远。

**内存估算：** 7B 参数、每个参数存 2 字节，推理时 GPU 内存至少 7B × 2 = 14 GB。

**参数数会骗人：** **sparse model**（大量参数为 0 的模型）和 **MoE**（mixture-of-experts，参数分成若干组 expert，每个 token 只启用其中几组）。

| 例子 | 总参数 | 每个 token 启用 |
|---|---|---|
| Mixtral 8x7B | 46.7B（8 个 expert 有共享部分，不是 56B） | 每层 2 个 expert，共 12.9B |

所以它的成本和速度接近 12.9B 的模型，不是 46.7B。

**两个常见误解：**
- 大不一定强：13B 的模型只喂一句话，不如小模型喂大量数据。
- 新一代同尺寸更强：Llama 3-8B 在 MMLU 上超过 Llama 2-70B。

**出处：** Huyen《AI Engineering》ch2 §Model Size
