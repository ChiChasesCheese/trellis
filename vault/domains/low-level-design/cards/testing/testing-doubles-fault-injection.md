---
id: testing-doubles-fault-injection
node: testing.doubles
type: qa
step: 3
---
## Q
服务把一批记录写进存储，要求「要么全写入，要么全不写」。真实的存储很难在第三次写入时恰好失败，测试怎样验证失败时的回滚？

## A
**替身在指定的第 n 次调用抛出指定的错误**

- **故障注入（fault injection）**：fake 存储带一个「在哪一项失败」的参数（这里用键），到点就抛出真实会抛的错（`OSError`、数据库的错误码）；
- **错误要像真的**：抛出的异常类型、错误码与真实存储一致，被测代码里的 `except` 才会走到；
- **逐点注入**：把失败位置从第一项试到最后一项，每个失败位置都要回滚干净；只测中间一处会漏掉第一次或最后一次；
- **断言最终状态**：失败之后存储里什么都没有，而不是断言「调用了几次 delete」；
- **同样的做法**：超时、部分写入、重复键冲突，一个替身一个故障。

```python
def failing_put(data, bad_key):
    def put(k, v):
        if k == bad_key: raise OSError("disk full")
        data[k] = v
    return put
def save_all(data, put, items):
    try:
        for k, v in items.items(): put(k, v)
    except OSError:
        for k in items: data.pop(k, None)            # 回滚
        raise
for bad in "abc":                                    # 每个位置各失败一次
    data = {}
    try: save_all(data, failing_put(data, bad), dict(a=1, b=2, c=3))
    except OSError: print(bad, data)                 # 总是 {}
```

**知识点：**测试替身（Test Doubles）
