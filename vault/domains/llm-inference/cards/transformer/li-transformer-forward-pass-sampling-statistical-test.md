---
id: li-transformer-forward-pass-sampling-statistical-test
node: transformer.forward-pass
type: qa
step: 6
---
## Q
怎样测试推理服务的随机采样实现是正确的？给出一个可执行的统计检验方案。

## A
**难点：** 开启随机采样后，同一个请求每次输出不同，不能逐字断言。但"抽中每个 token 的频率"必须符合模型给出的概率分布（经温度、top-p 等处理之后）。所以用统计检验：大量抽样，比较观测频率和理论概率。

**方案：**
1. **构造一个下一个 token 分布清楚的提示：** 比如"随机说一个 1 到 4 之间的数字："，并且只生成 1 个 token（`max_tokens=1`）。
2. **拿到理论概率：** 用 `logprobs=true, top_logprobs=20` 请求一次，得到前 20 个候选的对数概率；或用参考实现直接算 logits（模型对每个 token 的原始分数），手动套用同样的温度和 top-p，得到理论分布。
3. **大量抽样：** 同一请求、不固定种子，发 N = 5,000 次，统计每个 token 出现的次数。
4. **卡方检验（chi-square test）：** 比较观测次数和"N × 理论概率"。

```python
from scipy.stats import chisquare
obs = [counts[t] for t in toks]                  # 观测次数
exp = [N * p for p in probs]                     # 期望次数（概率已归一化到这些 token）
stat, pvalue = chisquare(obs, exp)
assert pvalue > 1e-3, f"采样分布偏离理论值 p={pvalue}"
```

**要覆盖的场景：**
- `temperature` 取 0.5、1.0、1.5：分布应按预期变尖或变平。
- `top_p=0.5`：被截掉的 token 出现次数必须为 0，一次都不能有。
- 固定 `seed`：同一种子两次请求应得到相同输出（在同一部署上），不同种子应有差异。
- 批大小不同（单发和并发 64 个）：分布不应改变。

**注意：** 期望次数小于 5 的类别要合并，否则卡方检验不可靠；显著性阈值设得很严（如 1e-3），避免检验本身成为偶发失败的测试。
