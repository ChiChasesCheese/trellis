---
id: craft-validate-then-commit-1-write-vs-validate
node: craft.patterns.validate-then-commit
type: qa
step: 1
---
## Q
**先校验后提交 · 为什么失败的操作不能留下半截状态**｜写法

一次操作要改好几处状态（三个账户的余额）。如果每改一处就检查一次，第三处检查失败时前两处已经改了，调用方看到的是「报错了，但数据变了」。怎样组织代码，让「报错」等于「什么都没发生」？

## A
**要点。** 把所有可能失败的检查（validate）排在任何写入之前，最后留一段只做赋值、不会再失败的提交段（commit）。失败只会发生在提交段之前，状态天然没动。

```python
def transfer_naive(bal, moves):
    for acct, delta in moves:
        bal[acct] += delta            # 先写
        if bal[acct] < 0:             # 再查：前面几条已经落盘
            raise Insufficient(acct)

def transfer_safe(bal, moves):
    after = dict(bal)                 # 在副本上算出结果
    for acct, delta in moves:
        after[acct] += delta
    if any(v < 0 for v in after.values()):
        raise Insufficient            # 校验段：bal 一个字节没动
    bal.update(after)                 # 提交段：只剩赋值
```

三条操作 `a-50, b+50, c-30`（c 只有 10）实际输出：

```
transfer_naive 拒绝 c -> {'a': 50, 'b': 50, 'c': -20}
transfer_safe 拒绝 c -> {'a': 100, 'b': 0, 'c': 10}
```

**为什么。** 边写边查的版本失败后要手工回滚，而回滚路径本身几乎没人测，最容易出错。先校验把「撤销」整个取消掉。

**代价。** 要先在脑子里（或副本上）把结果算出来，多一次遍历；提交段必须真的不会失败（不做 I/O、不调用外部代码）。
