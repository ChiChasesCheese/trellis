---
id: cbr-role-tiers
node: role.tools
type: qa
step: 1
---
## Q
Cerebras RIT 的 SDET 要用哪些工具？哪些必会、哪些应会、哪些知道就行？

## A
| 档次 | 工具 | 一句话 |
|---|---|---|
| 必会 | Python | 测试、编排、工具的主语言 |
| 必会 | pytest | Python 测试框架；基础设施团队要求会写 pytest 扩展 |
| 必会 | CI/CD | 每次提交自动构建、测试、发布 |
| 必会 | Linux 排查 | 日志、`gdb`、`strace`、`pdb` |
| 应会 | Kubernetes | 容器编排，推理平台跑在上面 |
| 应会 | Prometheus / Grafana | 指标采集和看板，常用作性能与健康门 |
| 应会 | asyncio、多进程 | 并发跑大量测试，处理超时、重试、取消 |
| 应会 | Go | 职位写"Python、Go 或类似语言" |
| 知道 | PyTorch | 写模型的框架，用来算参考结果 |
| 知道 | vLLM / SGLang | 开源 LLM 推理引擎，GPU 推理线在用 |
| 知道 | 模拟器、C++ | 没有硬件时跑晶圆程序；运行时和工具常用 C++ |
| 知道 | Jenkins、Bazel、Argo CD、Terraform、Helm | 构建、部署、基础设施 |

- **你的现状**：Python 有个人项目 66K 行；Kubernetes 在实习里用过；Go 没有，直说。
