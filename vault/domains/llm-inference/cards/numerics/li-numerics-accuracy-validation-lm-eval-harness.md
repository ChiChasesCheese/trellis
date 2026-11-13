---
id: li-numerics-accuracy-validation-lm-eval-harness
node: numerics.accuracy-validation
type: qa
step: 3
---
## Q
怎样用 lm-evaluation-harness 评测一个部署好的推理服务？跑评测时有哪些设置会让分数不可比？

## A
**lm-evaluation-harness（命令 `lm_eval`）：** 开源的大模型评测框架，内置几百个标准任务（如 MMLU 知识选择题、GSM8K 数学应用题），负责构造提示、调用模型、解析答案、计算分数。

**评测一个 OpenAI 兼容的服务：**

```bash
lm_eval --model local-chat-completions \
  --model_args model=meta-llama/Llama-3.1-8B-Instruct,base_url=http://localhost:8000/v1/chat/completions,num_concurrent=32 \
  --tasks gsm8k --apply_chat_template --num_fewshot 5 \
  --output_path results/ --log_samples
```

**直接加载模型到 vLLM 评测（不经过 HTTP）：**

```bash
lm_eval --model vllm --model_args pretrained=meta-llama/Llama-3.1-8B-Instruct,tensor_parallel_size=1 \
  --tasks mmlu,gsm8k --batch_size auto
```

**两种打分方式：**
- **对数概率打分：** 选择题把每个选项接在问题后面，比较模型给每个选项的对数概率，选最大的。不需要生成，结果稳定。但很多聊天接口不返回输入部分的对数概率，这类任务无法通过聊天接口评测。
- **生成后解析：** 让模型生成答案，再用规则抽取（比如 GSM8K 取最后一个数字）。依赖生成参数和输出格式。

**让分数不可比的设置：**
- **few-shot 示例数（`--num_fewshot`）：** 0 个和 5 个示例的分数可以差很多。
- **是否套对话模板（`--apply_chat_template`）：** 对话模型不套模板，分数常常明显偏低。
- **生成参数：** 温度、最大长度。最大长度太短，数学题的推理过程被截断，答案丢失。
- **答案解析规则：** 同一任务常有"严格匹配"和"宽松匹配"两种分数，报告要写清用的是哪个。
- **框架和任务版本：** 任务定义会更新，要固定 `lm_eval` 版本并记录任务版本。

**用 `--log_samples` 保存每一题的输入、输出和得分：** 两个版本分数有差异时，逐题对比找出哪些题从对变错，比只看总分有用得多。
