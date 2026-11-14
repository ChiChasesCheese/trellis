---
id: msd-serving-architecture-model-servers
node: serving.architecture
type: qa
step: 2
---
## Q
Triton、vLLM、Ray Serve、KServe 都被叫作"模型服务"工具，它们其实处在不同的层。各自负责什么？一个大模型服务一般怎么组合它们？

## A
**分三层看：**

| 层 | 管什么 | 代表 |
|---|---|---|
| **推理引擎 / 模型服务器** | 一个进程里把模型放进 GPU，收请求、凑批、跑计算 | NVIDIA Triton、vLLM、SGLang、TensorRT-LLM |
| **服务编排框架** | 多个模型或步骤怎么串起来、每步几个副本、按负载加减副本 | Ray Serve |
| **集群平台** | 在 Kubernetes 上部署、版本、流量切分、扩缩容 | KServe |

- **Triton：** 通用模型服务器。模型放在模型仓库里，目录形如 `models/<名字>/<版本号>/model.onnx` 加一个 `config.pbtxt`。它支持多种格式（ONNX、TensorRT、PyTorch、Python），在 `config.pbtxt` 里写 `dynamic_batching { max_queue_delay_microseconds: 100 }` 就会把短时间内到的请求凑成一批再算。对外接口是 KServe v2 推理协议，如 `POST /v2/models/<名字>/infer`，健康检查 `/v2/health/ready`。适合分类、排序、嵌入这类"一次输入、一次输出"的模型。
- **vLLM：** 专为大语言模型（一次一个词元地生成文字的模型）做的引擎。它管理每个请求生成过程中的中间状态（KV 缓存，存着已处理文字的计算结果，供后续每一步复用），并让请求在生成过程中随时加入或退出批次。对外是 OpenAI 兼容接口 `/v1/chat/completions`。
- **Ray Serve：** 用 Python 写"先嵌入、再检索、再调大模型"这类多步流程，每一步是一个 deployment，可以有自己的副本数和 GPU 配额，并按在途请求数自动扩缩。
- **KServe：** Kubernetes 上的自定义资源 `InferenceService`。写清楚模型在哪（`storageUri`）、用什么运行时，它负责拉起 Pod、加探针、做金丝雀分流（`canaryTrafficPercent`）和扩缩容。

**常见组合：** KServe（或自己写的 Kubernetes Deployment）管部署和流量 → 每个 Pod 里跑 vLLM 服务大模型 → 嵌入模型和重排模型放在 Triton 里 → 需要复杂编排时用 Ray Serve 把它们串起来。

**面试要点：** 别把"引擎"和"平台"混为一谈。引擎决定单卡快不快，平台决定上线、回滚和扩容稳不稳。
