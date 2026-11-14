---
id: msd-evaluation-llm-eval-benchmarks
node: evaluation.llm-eval
type: qa
step: 2
---
## Q
常用的公开基准有多大？用 lm-evaluation-harness 跑一次基准时，哪些设置会让同一个模型的分数差好几个点？

## A
**几个常见基准的规模：**
- **MMLU**：57 个学科的四选一选择题，测试集约 1.4 万题，测知识面。
- **GSM8K**：小学数学应用题，测试集 1,319 题，答案是一个数字，测多步推理。
- **HumanEval**：164 道 Python 编程题，每题带单元测试，用 pass@k（k 次尝试至少一次通过的概率）计分。

**用 lm-evaluation-harness 跑一次：**
```bash
lm_eval --model hf \
  --model_args pretrained=/models/llama-7b,dtype=bfloat16 \
  --tasks gsm8k --num_fewshot 5 --batch_size 8 \
  --output_path results/ --log_samples
```
评测正在运行的推理服务时，可以用 `--model local-completions` 或 `local-chat-completions` 指向它的兼容接口；`--log_samples` 把每道题的输入输出存下来，便于逐题对比。

**让分数差好几个点的设置：**
- **少样本数**（`--num_fewshot`）：提示里放几道带答案的示例题。0 个和 5 个可能差 10 个点以上。
- **对话模板**：对话模型要不要套用它的对话模板（`--apply_chat_template`，把题目包装成"用户说……助手答……"的格式）。套和不套的分数可能差很多。
- **答案提取规则**：从模型的长回答里用正则取出最终答案。规则太严，答对但格式略有不同的也被判错。
- **生成长度上限**：数学题的推理过程长，上限太小会被截断，答案没写出来。
- **评测框架和任务的版本**：同一任务在不同版本里的提示或提取规则可能改过。
- **采样设置**：温度大于 0 时每次结果不同，基准一般用贪心解码（每步选概率最高的词）。

**规则**：只有在**所有设置完全相同**时，两个分数才能比较。把框架版本、任务版本、完整命令和每题输出一起存档；网上看到的分数和自己跑的差几个点，先核对这些设置。
