---
id: errors-values-pass-through
node: errors.exceptions-vs-values
type: qa
step: 5
---
## Q
一个批量解析函数把坏格式的行变成 `None`。如果它读的迭代器自己抛了 `OSError`（磁盘出错），这个异常要不要也变成 `None`？

## A
**只把“自己负责的那类失败”变成值，其余原样传出**

- **格式错是这一行的问题**：转成值，后面的行照常处理；
- **读取出错不是格式问题**：磁盘坏了、网络断了，继续处理下去只会得到一堆看似正常的残缺结果，调用方也无从知道；
- **所以 `try` 只包住解析那一句**：`for` 取下一行的动作放在 `try` 外面，迭代器的异常碰不到 `except ValueError`；
- **同理**：数据库层的异常、配置回调里的异常，不包成 400，原样上抛，让顶层决定；
- **转换要窄**：能转成值的是合同里写明的失败，不是“所有异常”。

```python
def parse_all(rows):
    out = []
    for raw in rows:                         # 迭代器自己抛的异常不经过下面的 except
        try: out.append(int(raw))
        except ValueError: out.append(None)  # 格式错：这一行是 None
    return out

def feed():
    yield "1"; yield "x"; raise OSError("disk")

print(parse_all(["1", "x"]))                 # [1, None]
try: parse_all(feed())
except OSError as e: print("原样传出：", e)
```

**知识点：**异常与错误值（Exceptions vs Values）
