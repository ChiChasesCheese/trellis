---
id: msd-mlops-registry-cicd-llm-manifest
node: mlops.registry-cicd
type: qa
step: 3
---
## Q
一个大语言模型的"可部署版本"不只是权重文件。它的发布清单（manifest）应该锁定哪些东西？为什么少锁一样就会出事？

## A
**大语言模型的输出由一整套东西共同决定。** 只换权重、其他不变，或者权重不变、换了引擎版本，输出都可能变。所以注册表里的一个"版本"应该是一个**清单**，锁定下面每一项，并用内容哈希标识：

```yaml
model: support-bot
version: 2026-11-13.1
weights:  s3://models/llama-8b-ft/  sha256:9f2c...   # 权重文件
tokenizer: sha256:41ab...       # 分词器：把文字切成词元编号的规则
chat_template: sha256:7d10...   # 对话模板：把多轮对话拼成一串文字的格式
generation_config: {temperature: 0.7, max_tokens: 1024, stop: ["<|eot_id|>"]}
system_prompt: prompts/support/v12.txt
quantization: fp8-dynamic       # 每个参数用 8 位存的方案
engine: vllm==0.11.0            # 推理引擎版本
engine_args: {tensor_parallel_size: 2, max_model_len: 32768}
hardware: H100-80GB
eval_report: s3://evals/support-bot/2026-11-13.1.json
```

**少锁一样会怎样：**
- **分词器或对话模板不一致：** 权重是对的，但模型看到的输入格式和训练时不同。症状是回答突然啰嗦、不停止、或多出奇怪的标记。
- **停止词没锁：** 模型说完了却不停，一直生成到长度上限，费用和延迟翻倍。
- **引擎版本漂移：** 镜像里写的是 `vllm:latest`，某次重建拉到新版本，默认参数变了，延迟或输出悄悄变化，回滚权重也修不好。
- **系统提示没版本：** 有人在配置中心直接改了提示，质量下降却查不到是哪次改动。

**做法：**
- **不可变：** 清单一旦注册不可修改，任何一项变化都生成新版本。
- **一起发布、一起回滚：** 部署系统按清单整体部署；回滚是指回上一个清单，而不是只换权重。
- **启动时自检：** 服务启动时校验每个文件的哈希与清单一致，不一致就拒绝就绪。
- **评测绑定：** 评测报告记录的是"哪个清单"的结果，换了任何一项都要重跑相应的评测。
