---
id: li-metrics-benchmarking-tools-and-mlperf
node: metrics.benchmarking
type: qa
step: 3
---
## Q
常用的 LLM 推理基准工具有哪些（vllm bench、GenAI-Perf/AIPerf、MLPerf Inference）？各自适合什么用途？MLPerf 的场景和延迟约束是什么？

## A
**`vllm bench serve`（vLLM 自带）：** 对任意 OpenAI 兼容的服务发压，报告 TTFT、TPOT、ITL、端到端延迟的均值、中位数和分位数，以及吞吐和 goodput。

```bash
vllm bench serve --backend openai-chat --endpoint /v1/chat/completions \
  --model <模型> --dataset-name sharegpt --dataset-path ShareGPT.json \
  --num-prompts 2000 --request-rate 8 --save-result --seed 0
```

适合开发和回归测试：轻量、参数全、结果可存成 JSON 供对比。

**GenAI-Perf 与 AIPerf（NVIDIA）：** 针对推理服务的压测客户端，支持合成输入（指定输入 token 数的均值和标准差）、流式指标、多种接口类型。AIPerf 是 GenAI-Perf 的重写后继，采用多进程设计，避免高并发时客户端自己成为瓶颈。

```bash
aiperf profile -m <模型> --url localhost:8000 --endpoint-type chat --streaming \
  --synthetic-input-tokens-mean 512 --output-tokens-mean 256 --concurrency 16
```

适合跨引擎、跨硬件的对比：同一个客户端压不同的服务，口径一致。

**MLPerf Inference（MLCommons）：** 行业标准基准，厂商按严格规则提交、互相审查，结果公开。
- **场景：** Offline（所有样本一次给出，只比吞吐）；Server（请求按泊松过程到达，在延迟约束内比吞吐）；还有面向单流和边缘设备的场景。
- **LLM 的延迟约束：** Llama 2 70B 的 Server 场景要求 TTFT ≤ 2 秒、TPOT ≤ 200 毫秒；v5.0 增加的 Interactive 场景收紧到 TTFT ≤ 450 毫秒、TPOT ≤ 40 毫秒。
- **精度要求：** 提交的结果必须在参考模型的评测分数的规定比例之内（如 99% 或 99.9%），量化不能以过多精度为代价。
- **用途：** 看不同硬件在规范条件下的相对表现，但负载固定、调优深度极高，不能直接代表你的流量。

**选择原则：** 开发阶段用 `vllm bench` 做快速回归；对外比较或选型时用统一的外部客户端；MLPerf 用于理解行业水平和硬件能力边界。三者都要配合"你自己的真实流量回放"才能得出上线结论。
