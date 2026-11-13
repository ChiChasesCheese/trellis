---
id: li-basics-what-is-a-model-model-checkpoint-contents
node: basics.what-is-a-model
type: qa
step: 4
---
## Q
从 Hugging Face 下载一个模型，目录里通常有哪些文件？各自起什么作用？哪个文件出错会导致什么问题？

## A
一个典型的模型目录（例如 7B 对话模型）包含四类文件：

- **`config.json`：结构说明书。** 写着层数（`num_hidden_layers: 32`）、每层宽度（`hidden_size: 4096`）、词表大小（`vocab_size: 32000`）、最长能处理多少文字等。代码根据它搭出空的计算结构。
- **`*.safetensors`：参数本体。** 几个到几十个分片文件，合起来约 14 GB（7B、每参数 2 字节）。`model.safetensors.index.json` 记录每个参数在哪个分片里。
- **分词器文件：`tokenizer.json`、`tokenizer_config.json`。** 模型只认数字编号，这些文件定义文字和编号怎么互转，以及对话格式模板（chat template）。
- **`generation_config.json`：生成时的默认设置。** 比如结束标记的编号、默认随机程度。

出错的后果各不相同：

- **配置和权重不匹配：** 加载时报"形状不对"，这是好情况，至少暴露了。
- **分词器换了版本：** 同一句话变成不同编号，模型照样输出，但答案质量下降或出现乱码，最难发现。
- **生成配置漏了结束标记：** 模型答完不停，一直输出到长度上限。

加载代码只需一行：`AutoModelForCausalLM.from_pretrained("<目录>", torch_dtype=torch.bfloat16)`。测试新模型上线时，这四类文件都要核对版本和哈希。
