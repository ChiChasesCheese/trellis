---
id: li-basics-language-model-logits-softmax
node: basics.language-model
type: qa
step: 2
---
## Q
模型最后一层输出的 logits 是什么？softmax 怎样把它变成概率？用三个数手算一遍，并说明实现时的数值陷阱。

## A
**logits：** 模型最后一层给词表里每个 token 打的**原始分数**，可正可负，没有范围限制，也不加起来等于 1。分数越高，表示模型越认为它是下一个 token。词表 32,000 个 token，就有 32,000 个 logits。

**softmax：把分数变成概率。** 对每个分数取指数，再除以所有指数之和：

`p_i = e^(z_i) / Σ e^(z_j)`

**手算：** logits = `[2.0, 1.0, 0.0]`
- 取指数：e² ≈ 7.389，e¹ ≈ 2.718，e⁰ = 1，总和 ≈ 11.107
- 概率：7.389/11.107 ≈ **0.665**，2.718/11.107 ≈ **0.245**，1/11.107 ≈ **0.090**
- 三个概率加起来等于 1，而且保留了大小顺序。分数差 1，概率约差 e ≈ 2.7 倍。

**数值陷阱：**
- **溢出：** logits 可能是 80 这样的数，e⁸⁰ 超出 FP32 范围（约 3.4×10³⁸），变成无穷大。标准做法是先减去最大值：`softmax(z) = softmax(z - max(z))`，结果在数学上相同，但最大的指数变成 e⁰ = 1，不会溢出。
- **低精度：** 在 16 位浮点数里算 softmax，小概率会被舍成 0。推理引擎通常把 logits 转成 FP32 再算。

```python
import torch
z = torch.tensor([2.0, 1.0, 0.0])
print(torch.softmax(z, dim=-1))         # tensor([0.6652, 0.2447, 0.0900])
print(torch.log_softmax(z, dim=-1))     # 对数概率，API 里的 logprobs 就是它
```
