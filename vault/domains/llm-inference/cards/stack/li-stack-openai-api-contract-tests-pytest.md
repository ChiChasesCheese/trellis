---
id: li-stack-openai-api-contract-tests-pytest
node: stack.openai-api
type: qa
step: 4
---
## Q
用 pytest 和 OpenAI Python 客户端，为一个 OpenAI 兼容推理接口写一组契约测试（contract test），应该覆盖哪些用例？给出代码骨架。

## A
**契约测试：** 不关心内部实现，只验证"接口按约定的格式和语义工作"。OpenAI 官方客户端可以直接指向任何兼容服务（`base_url` 参数），用它测试还能顺便保证真实客户端能用。

```python
import pytest
from openai import OpenAI, BadRequestError
client = OpenAI(base_url="http://localhost:8000/v1", api_key="test")
M = "meta-llama/Llama-3.1-8B-Instruct"

def chat(**kw):
    return client.chat.completions.create(model=M, messages=[{"role": "user", "content": "从 1 数到 50"}], temperature=0, **kw)

@pytest.mark.parametrize("n", [1, 5, 17])
def test_length_finish(n):
    r = chat(max_completion_tokens=n)
    assert r.choices[0].finish_reason == "length" and r.usage.completion_tokens == n

def test_stream_equals_nonstream():
    full = chat(max_completion_tokens=64).choices[0].message.content
    parts = [c.choices[0].delta.content or "" for c in chat(max_completion_tokens=64, stream=True) if c.choices]
    assert "".join(parts) == full

def test_stop_not_returned():
    r = chat(stop=["10"])
    assert "10" not in r.choices[0].message.content and r.choices[0].finish_reason == "stop"

def test_bad_temperature():
    with pytest.raises(BadRequestError):
        chat(temperature=5)
```

**应覆盖的用例清单：**
- **每种结束原因：** `stop`（自然结束、停止串）、`length`、`tool_calls`。
- **流式与非流式等价：** 内容、`finish_reason`、`usage`（开启 `include_usage`）。
- **参数边界：** `max_completion_tokens` 为 1；`temperature` 为 0 和 2；`top_p` 为 1 和极小值；`stop` 为 4 个串、跨 token 的串；`logprobs` 加 `top_logprobs` 为 0 和 20。
- **非法输入：** 越界参数、空消息、未知模型、超长上下文，逐一断言状态码和 `error.code`。
- **计数正确：** `prompt_tokens` 等于用同一分词器对模板化后的消息独立计算的长度。
- **结构化输出：** 指定 JSON Schema 时，输出能被 `json.loads` 解析且通过校验。
- **多语言与特殊字符：** 中文、emoji、代码块的流式拼接无乱码。

**运行方式：** `pytest -n auto`（pytest-xdist 并行）缩短时间；失败后 `pytest --lf` 只重跑上次失败的用例。
