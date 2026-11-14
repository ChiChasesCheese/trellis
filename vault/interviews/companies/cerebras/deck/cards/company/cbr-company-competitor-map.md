---
id: cbr-company-competitor-map
node: company.competitors
type: qa
step: 1
---
## Q
Cerebras 的主要竞争对手有哪些？哪些既是对手又是伙伴？

## A
| 对手 | 是什么 | 关系 |
|---|---|---|
| **Nvidia** | GPU 霸主；2025 年底约 200 亿美元非独家授权 Groq 的芯片设计，推出"GPU 做预填充、SRAM 芯片分担解码"的机柜 | 最大对手，开始卖同一思路 |
| **AMD** | GPU 第二名 | 对手，也是伙伴（Helios 做预填充）和投资人 |
| **Groq** | 另一家 SRAM 推理芯片公司，仍运营 GroqCloud | 直接对手 |
| **SambaNova** | 推理芯片 SN50 | 直接对手 |
| **Google TPU** | 谷歌自研 AI 芯片 | 对手 |
| **AWS Trainium** | 亚马逊自研芯片 | 分离式推理里的伙伴 |
| **云与新云** | AWS、Azure、GCP、Oracle、CoreWeave | 卖推理服务的对手 |

- **CUDA**：Nvidia 的 GPU 编程平台，大多数 AI 软件建在它上面。Cerebras 不用 CUDA，模型要经过自家编译器，所以每个新模型都要做大量集成验证。
