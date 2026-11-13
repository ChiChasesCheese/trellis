---
id: li-serving-speculative-drafter-variants
node: serving.speculative
type: qa
step: 3
---
## Q
投机解码的"起草者"（drafter）有哪几种？各自的优缺点是什么？在 vLLM 里怎么配置？

## A
**起草者：** 负责快速猜出接下来 k 个 token 的组件，猜得越准（接受率越高）、越便宜，加速越大。大模型随后一次检查这 k 个。

- **独立的小草稿模型（draft model）：** 同一家族的小模型，比如用 1B 给 70B 起草。必须和大模型使用同一个分词器（把文字切成 token 并编号的程序）。优点是通用；缺点是要额外占显存、额外维护一个模型，且小模型每个 token 也要一步步生成。
- **n-gram 查找（prompt lookup）：** 不用任何模型，在输入和已生成的文本里找"最近几个 token 曾经出现过的地方"，把它后面的内容当作草稿。几乎零成本，对复述、改写代码、基于文档的问答效果很好；开放式写作几乎没用。
- **EAGLE 系列：** 在大模型上接一个很小的额外网络（"头"），它读取大模型最后几层的内部向量来预测后续 token。因为直接利用了大模型的内部信息，接受率比独立小模型高，成本低。需要为每个大模型专门训练这个头。
- **MTP（multi-token prediction，多 token 预测）：** 模型训练时就带了预测后面第 2、3 个 token 的额外模块（如 DeepSeek-V3），推理时直接拿来起草。

**vLLM 配置（启动参数 `--speculative-config`，一段 JSON）：**

```bash
vllm serve <目标模型> --speculative-config '{"method": "ngram", "num_speculative_tokens": 4, "prompt_lookup_min": 2, "prompt_lookup_max": 5}'
vllm serve <目标模型> --speculative-config '{"method": "draft_model", "model": "<草稿模型>", "num_speculative_tokens": 5}'
vllm serve <目标模型> --speculative-config '{"method": "mtp", "num_speculative_tokens": 1}'
```

**怎么选：**
- 流量以检索问答、代码编辑为主：先试 n-gram，零成本。
- 模型官方提供 EAGLE 头或 MTP 模块：优先用它们。
- 高并发时：批已经很大、计算单元已经忙碌，检查多余位置不再"免费"，加速会缩小甚至变成减速。上线前要在目标并发下实测。
