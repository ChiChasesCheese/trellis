---
id: parsing-io-streams-chunked-hash
node: parsing-io.streams
type: qa
step: 2
---
## Q
给大文件算 SHA-256，为什么不能 `hashlib.sha256(f.read())`？按块读时块的大小怎么选，哈希结果会不会因为分块不同而不同？

## A
**哈希对象可以逐块 `update`，结果与分块无关**

- **`f.read()`**：整个文件进内存；几个 GB 的文件直接 `MemoryError` 或把系统拖进交换；
- **逐块 `update`**：`h.update(chunk)` 可以调用任意多次，最终摘要等于对全部字节一次性计算的结果；
- **块大小**：64 KB 到几 MB 都可以；太小系统调用多，太大占内存；内存占用是块大小，与文件大小无关；
- **读到结尾**：`f.read(n)` 在文件末尾返回空字节串 `b""`，用 `iter(callable, sentinel)` 当终止条件最简洁；
- **文本模式不行**：哈希要以二进制（`"rb"`）读，文本模式会做换行和编码转换。

```python
import hashlib, io

def sha256_stream(f, block: int = 1 << 20) -> str:
    h = hashlib.sha256()
    for chunk in iter(lambda: f.read(block), b""):    # 读到 b"" 为止
        h.update(chunk)
    return h.hexdigest()

data = b"x" * 10_000
print(sha256_stream(io.BytesIO(data), 64) == hashlib.sha256(data).hexdigest())   # True：分块不影响结果
```

**知识点：**流式处理大文件（Streaming Large Files）
