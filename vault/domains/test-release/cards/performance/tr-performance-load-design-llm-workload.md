---
id: tr-performance-load-design-llm-workload
node: performance.load-design
type: qa
step: 1
---
## Q
给一个大语言模型推理服务做负载测试，工作负载模型（workload model）要描述哪些维度？用 `vllm bench serve` 怎么表达？

## A
**先说清对象**：大语言模型（LLM）推理服务接收一段文字（prompt），逐个生成后续文字。文字被切成叫 token 的小单位（大约一个词或半个词）。一个请求的成本主要由**输入有多少 token**和**要生成多少 token**决定：输入在开头一次性处理，输出必须一个一个地生成，所以长输出的请求会占用服务很久。

**工作负载模型要描述的维度**：
- **输入长度分布**：聊天请求可能几百个 token，文档总结可能上万个；用固定长度测试会和真实情况差很远。
- **输出长度分布**：决定每个请求占用服务的时间。
- **到达过程**：请求是按平均速率随机到达（泊松过程），还是成簇突发。
- **开环还是闭环**：开环（open loop）按到达过程发送，不管前面的请求是否完成，模拟大量独立用户；闭环（closed loop）固定 N 个并发，一个完成才发下一个，模拟有并发上限的上游。
- **共享前缀**：很多请求以同样的系统指令开头，服务可能复用这部分的计算；测试数据要反映真实的共享比例，否则结果过于乐观或悲观。

**对应的 `vllm bench serve` 参数**：

```bash
vllm bench serve --base-url http://127.0.0.1:8000 \
  --dataset-name random --random-input-len 1024 \
  --random-output-len 256 --random-range-ratio 0.5 \
  --num-prompts 2000 --request-rate 8 --burstiness 1.0 \
  --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,99
```

- `--request-rate 8`：平均每秒 8 个请求，开环；默认 `inf` 表示所有请求在开头一次性发出；
- `--burstiness`：1.0 为泊松到达，小于 1 更突发，大于 1 更均匀；
- `--max-concurrency`：限制同时在途的请求数，用来模拟闭环或上游限流；
- `--random-range-ratio 0.5`：长度在设定值上下按比例随机，而不是全部相同；
- 指标：TTFT 是首个 token 的等待时间，TPOT 是之后平均每个 token 的时间，ITL 是相邻 token 的间隔，E2EL 是整个请求的端到端延迟。

最可信的做法是用生产请求日志的长度分布和到达时间重放。
