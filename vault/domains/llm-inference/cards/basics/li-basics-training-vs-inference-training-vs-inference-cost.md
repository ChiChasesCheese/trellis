---
id: li-basics-training-vs-inference-training-vs-inference-cost
node: basics.training-vs-inference
type: qa
step: 3
---
## Q
训练和推理的计算量、内存需求各差多少？以 7B 模型为例算一笔账。

## A
**计算量。**
- 推理：每个 token 一次前向计算，约 **2 × 参数个数** 次浮点运算。7B 模型约 14 GFLOP（140 亿次）每 token。
- 训练：前向 + 反向（反向约为前向的 2 倍），约 **6 × 参数个数** 次每 token。7B 模型约 42 GFLOP 每 token。
- 规模差距更大：训练一个 7B 模型要处理约 2 万亿 token（Llama 2 的数据量），总计算量约 6 × 7×10⁹ × 2×10¹² ≈ 8.4×10²² 次，要上千块 GPU 跑几周。推理一次 500 token 的回答只需 7 万亿次，一块 GPU 几秒钟。

**内存（每个参数要存什么）。**
- 推理：只存参数本身。FP16 每个 2 字节，7B 共 **14 GB**。另外加上每个请求的中间缓存。
- 训练（混合精度 + Adam 优化器的常见做法）：FP16 参数 2 字节 + FP16 梯度 2 字节 + FP32 主参数 4 字节 + Adam 的两个统计量各 4 字节，共 **16 字节每参数**，7B 约 112 GB，还不算中间结果。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 132" font-family="sans-serif" font-size="11">
<text x="4" y="14" fill="currentColor">每个参数占几字节（训练: FP16 参数和梯度, FP32 主参数, Adam 两个统计量）</text>
<text x="4" y="45" fill="currentColor">推理</text>
<rect x="40" y="30" width="36" height="24" fill="none" stroke="currentColor"/>
<text x="58" y="46" text-anchor="middle" fill="currentColor">参数2</text>
<text x="84" y="46" fill="currentColor">2 字节 → 7B 约 14 GB</text>
<text x="4" y="95" fill="currentColor">训练</text>
<rect x="40" y="80" width="36" height="24" fill="none" stroke="currentColor"/>
<text x="58" y="96" text-anchor="middle" fill="currentColor">参数2</text>
<rect x="76" y="80" width="36" height="24" fill="none" stroke="currentColor"/>
<text x="94" y="96" text-anchor="middle" fill="currentColor">梯度2</text>
<rect x="112" y="80" width="72" height="24" fill="none" stroke="currentColor"/>
<text x="148" y="96" text-anchor="middle" fill="currentColor">主参数4</text>
<rect x="184" y="80" width="72" height="24" fill="none" stroke="currentColor"/>
<text x="220" y="96" text-anchor="middle" fill="currentColor">Adam 4</text>
<rect x="256" y="80" width="72" height="24" fill="none" stroke="currentColor"/>
<text x="292" y="96" text-anchor="middle" fill="currentColor">Adam 4</text>
<text x="40" y="124" fill="currentColor">16 字节 → 7B 约 112 GB（不含中间结果）</text>
</svg>
```

**为什么推理成了独立的工程问题。** 训练是一次性的大成本；推理是每个用户每次提问都要付的成本，持续发生，而且有人在等结果。所以推理关心的是另一组指标：

- **延迟：** 第一个字多久出来，每个字间隔多久；
- **吞吐：** 一台机器每秒能输出多少 token；
- **成本：** 每百万 token 多少钱。

一个 7B 模型的权重只要 14 GB，一张 80 GB 的卡完全放得下，难点不在"能不能跑"，而在"同时服务很多人时又快又省"。
