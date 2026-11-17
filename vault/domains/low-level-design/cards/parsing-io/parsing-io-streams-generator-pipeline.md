---
id: parsing-io-streams-generator-pipeline
node: parsing-io.streams
type: qa
step: 1
---
## Q
一个 20 GB 的访问日志要统计出错行数。`len([l for l in f.readlines() if "ERROR" in l])` 为什么会把机器撑爆？怎样让内存与文件大小无关？

## A
**逐行迭代加生成器管道，内存只留一行**

- **`readlines()` / `read()`**：先把整个文件装进内存，再开始处理；文件有多大，内存就要多大；
- **文件对象本身是迭代器**：`for line in f` 每次读一行（底层按缓冲块读磁盘），处理完这一行就可以丢掉；
- **生成器管道（generator pipeline）**：每一级是一个生成器，从上一级拉一行、处理、交给下一级；整条管道同时只有一行在内存里；
- **聚合用累加器**：`sum(1 for ...)` 不建列表；要全量结果才用得上列表，那就要想想这步能不能换成累加；
- **`with open(...)` 包住**：生成器没跑完时文件仍然开着，靠上下文管理器保证关闭。

```python
import io

def lines(f):
    for line in f: yield line.rstrip("\n")           # 逐行，不建列表

def only(pred, it):
    return (x for x in it if pred(x))                # 过滤也是惰性的

f = io.StringIO("ok\nERROR a\nok\nERROR b\n")        # 换成 open(path) 即可
print(sum(1 for _ in only(lambda s: "ERROR" in s, lines(f))))    # 2
```

<details class="pt"><summary>延伸</summary>

二进制文件或没有换行的大块数据，用 `iter(lambda: f.read(1 << 20), b"")` 按固定块读，内存同样有界；下一张卡讲它。

</details>

**知识点：**流式处理大文件（Streaming Large Files）
