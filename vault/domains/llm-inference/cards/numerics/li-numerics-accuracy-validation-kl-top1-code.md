---
id: li-numerics-accuracy-validation-kl-top1-code
node: numerics.accuracy-validation
type: qa
step: 2
---
## Q
怎样计算被测推理系统和参考实现之间的 KL 散度和 top-1 一致率？写出代码，并说明阈值大致怎么定。

## A
**输入：** 同一批 token 序列（token 是文字切成的小片段，这里直接给编号，绕过分词差异），两边各算出每个位置对词表的分数（logits），形状 `[位置数, 词表大小]`。

**指标：**
- **KL 散度（Kullback-Leibler divergence）：** `KL(P‖Q) = Σ P(x) × log(P(x) / Q(x))`，P 是参考分布，Q 是被测分布。衡量"用 Q 代替 P 损失了多少信息"，0 表示完全相同，越大差异越大。逐位置计算，再看平均值和高分位数。
- **top-1 一致率：** 每个位置两边分数最高的 token 是否相同，统计相同的比例。

```python
import torch
import torch.nn.functional as F

def compare(ref_logits, test_logits):
    p_log = F.log_softmax(ref_logits.float(), dim=-1)    # 参考的对数概率
    q_log = F.log_softmax(test_logits.float(), dim=-1)   # 被测的对数概率
    kl = (p_log.exp() * (p_log - q_log)).sum(-1)         # 每个位置一个 KL 值
    top1 = (ref_logits.argmax(-1) == test_logits.argmax(-1)).float().mean()
    return kl.mean().item(), kl.quantile(0.99).item(), top1.item()
```

**手算直觉：** 参考分布 (0.6, 0.4)，被测 (0.55, 0.45)：KL = 0.6 × ln(0.6/0.55) + 0.4 × ln(0.4/0.45) ≈ 0.0522 − 0.0471 = **0.0051**。最大的 token 仍是第一个，top-1 一致。

**阈值怎么定（不要拍脑袋）：**
1. **先测"无害差异"：** 用参考实现自己和自己比，只改变无关紧要的东西：FP32 对 BF16、批大小 1 对 32、单卡对多卡。得到的 KL 和 top-1 就是"正确实现之间也会有的差异"。
2. **在这个基础上留余量：** 例如参考自比的平均 KL 是 0.002、P99 是 0.03、top-1 一致率 99.2%，被测系统的门限可以设为平均 KL < 0.005、P99 < 0.08、top-1 > 98.5%。
3. **量化版本单独设：** 8 位量化的 KL 会明显大于 BF16 实现之间的差异，要基于"已验证质量可接受的量化版本"再校准一次。

**注意：**
- 比较要在同一组输入、同一位置上逐个进行，不能比较两边各自生成的文本（一旦生成分叉，后面的位置就不可比）。
- 只取高概率候选的 logprobs（比如 API 只返回前 20 个）时，KL 只能近似计算，阈值要相应放宽。
