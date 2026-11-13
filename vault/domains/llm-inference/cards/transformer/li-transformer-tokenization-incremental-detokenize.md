---
id: li-transformer-tokenization-incremental-detokenize
node: transformer.tokenization
type: qa
step: 1
---
## Q
流式输出时，推理服务怎样把一个个生成的 token 编号增量地转成文字（增量反分词，incremental detokenization）？为什么不能每个 token 单独解码再拼接？

## A
**token：** 文字被切成的小片段，每个片段有一个编号。生成时模型一次输出一个编号，服务要尽快把对应文字推给用户。

**为什么不能逐个单独解码再拼接：**
- **多字节字符被拆开：** 一个汉字或 emoji 在 UTF-8 里占 3–4 个字节，可能被拆成几个 token。单独解码第一个 token 得到的是不完整的字节，显示为 `�`。
- **空格和合并规则：** 有些分词器（如 SentencePiece）用特殊符号表示词首空格，单独解码一个 token 时开头的空格会被去掉或保留，取决于上下文，拼起来会多空格或少空格。
- **全部重新解码太慢：** 每步把整段输出从头解码一遍，输出越长越慢，长回答时成本是平方级。

**常用做法（vLLM、TGI 等引擎都采用类似算法）：** 维护两个偏移量 `prefix_offset` 和 `read_offset`，每步只解码最后一小段：

```python
def step(tok, ids, prefix_offset, read_offset):
    prefix_text = tok.decode(ids[prefix_offset:read_offset])
    new_text = tok.decode(ids[prefix_offset:])
    if len(new_text) > len(prefix_text) and not new_text.endswith("�"):
        delta = new_text[len(prefix_text):]       # 本步新确认的文字
        return delta, read_offset, len(ids)        # 向前推进两个偏移量
    return "", prefix_offset, read_offset          # 字符还不完整，先不输出
```

**要点：**
- 用前面几个 token 作为"上下文"一起解码，空格处理和整段解码一致。
- 结尾是 `�`（替换字符 `�`）说明字节不完整，先不输出，等下一个 token。
- 流结束时，把剩余未输出的文字一次性冲刷出去，否则最后一个字可能丢失。

**测试：** 用包含中文、emoji、连续空格、代码缩进的长回答，断言"流式各段拼接的结果 == 对全部编号一次性 `decode` 的结果"；再单独测试输出在一个多字节字符中间被 `max_tokens` 截断的情况。
