---
id: api-returns-exception-vs-sentinel
node: api.returns
type: qa
step: 4
---
## Q
`s.find(x)` 找不到返回 `-1`，`s.index(x)` 找不到抛 `ValueError`。为什么 `find` 的写法会让人写出悄悄出错的代码？设计自己的接口时，失败该用特殊返回值还是异常？

## A
**调用方不处理就会继续跑下去的失败，用异常**

- **特殊值能被当成真值用**：`-1` 是合法下标，`s[s.find("x")]` 不报错，取到的是最后一个字符；
- **异常不会被忘**：不处理就中断，错误停在出错的地方，而不是传到三层以后；
- **返回值适合“预期的分支”**：调用方一定会立刻判断的结果，如 `dict.get` 的 `None`、`re.match` 的 `None`、`cancel()` 返回是否成功；
- **别两头占**：同一个函数有时返回 `None`、有时抛异常，调用方两种都得防；一个接口选一种，写进合同；
- **选择的依据**：失败是否算调用方的错。取消一笔已经结算的付款失败是业务上的正常结果，返回 `False`；传了负的金额是调用方的 bug，抛异常。

```python
s = "abc"
print(s[s.find("x")])             # 'c'：-1 被当成下标，没有任何报错
try: s.index("x")
except ValueError as e: print("index raises:", e)

def cancel(pending: set[int], pid: int) -> bool:
    if pid not in pending:
        return False              # 预期的结果：已结算或不存在
    pending.remove(pid)
    return True
print(cancel({1}, 2))
```

**知识点：**返回值设计（Return Values）
