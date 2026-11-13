---
id: li-transformer-forward-pass-compare-to-reference
node: transformer.forward-pass
type: qa
step: 3
---
## Q
怎样验证一个新推理实现（新引擎、新硬件或新内核）的前向计算是正确的？写出逐层对比的做法和容差设置。

## A
**原则：** 用同一份权重、同一组输入，让参考实现（通常是 Hugging Face transformers 的 PyTorch 代码，FP32 或 BF16）和被测实现各算一遍，比较中间结果和最终 logits（模型对词表每个 token 的原始分数）。

**步骤：**
1. **固定输入：** 准备几十条覆盖不同长度（1、17、512、4,096 个 token）和语言的输入，直接给 token 编号，绕过分词器，先排除分词差异。
2. **导出参考值：** `out = ref_model(ids, output_hidden_states=True)`，保存每层的隐藏状态（每个 token 在模型内部的 4,096 维向量）和 logits。
3. **导出被测值：** 被测系统能导出中间层最好；不能时，至少比较最终 logits 或返回的 logprobs（每个 token 的对数概率）。
4. **逐层比较：** 找到第一个差异明显跳升的层，问题就在那里。

```python
import torch
for i, (a, b) in enumerate(zip(ref_hidden, test_hidden)):
    cos = torch.nn.functional.cosine_similarity(a.float().flatten(), b.float().flatten(), dim=0)
    print(i, f"cos={cos:.6f}", f"maxabs={(a - b).abs().max():.4f}")
torch.testing.assert_close(test_logits.float(), ref_logits.float(), rtol=2e-2, atol=2e-2)
```

**容差怎么定：**
- `torch.testing.assert_close` 判定 `|a − b| ≤ atol + rtol × |b|`。对 BF16（16 位浮点，只有约 3 位有效十进制数字），它自己的默认容差是 `rtol=1.6e-2, atol=1e-5`；跨实现比较 32 层累积后的 logits，通常还要放宽到 1e-2 量级。
- 比"逐元素都在容差内"更稳健的指标：每层余弦相似度 > 0.999；最终 top-1 token（分数最高的那个）一致率 > 99%；两个概率分布的 KL 散度均值很小。
- 容差怎样定得有依据：先用参考实现自己和自己比（FP32 对 BF16、不同批大小），测出"无害差异"的范围，再把被测实现的门限设在它的若干倍。

**常见被抓到的问题：** 归一化的 ε 不对、位置编码基数不对、K、V 头的对应关系错位、某个融合内核在特定长度（如不是 16 的倍数）下越界。
