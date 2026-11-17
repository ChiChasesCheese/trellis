---
id: parsing-io-streams-bad-line
node: parsing-io.streams
type: qa
step: 3
---
## Q
命令行工具从标准输入一行读一个 JSON 请求，每行输出一个结果。第 3 行是坏的，另有一行是空行、一行含非法字节。怎样让这些行不影响其他行，而且输出的行数和输入对得上？

## A
**每行独立处理，每行必有一行输出**

- **按行解码**：从 `sys.stdin.buffer` 读字节，每行自己 `decode`；整个流设成 UTF-8 严格模式时，一个坏字节会让后面所有行都读不出来；
- **错误隔离**：`try` 放在每行的处理里，坏行转成 `{"error": ...}` 的一行；真实代码只捕获解析层自己的命名错误（示例为了简短用 `ValueError` 代替），`except Exception` 会把自己的 bug 也吞掉；
- **空行不能跳过**：空行也是一个请求，它是坏的，答案是一行错误；跳过会让第 n 行的输出对应到第 n+1 行的输入；
- **输出只写结果行**：诊断信息去标准错误，管道的下游才能按行解析；
- **驱动要薄**：解码、解析、评估、序列化四步，每步一个函数，驱动只负责循环。

```python
import io, json

def handle(raw: bytes) -> dict:
    try:
        return {"n": len(json.loads(raw.decode("ascii")))}      # 解码、解析、评估
    except ValueError:                                           # UnicodeDecodeError 和 JSONDecodeError 都是它的子类
        return {"error": "invalid_json"}

stdin = io.BytesIO(b'{"a":1}\n\n\xff\n{"b":')
for raw in stdin:
    print(json.dumps(handle(raw.rstrip(b"\n"))))
```

**知识点：**流式处理大文件（Streaming Large Files）
