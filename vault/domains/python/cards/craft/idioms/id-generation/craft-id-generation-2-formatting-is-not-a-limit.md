---
id: craft-id-generation-2-formatting-is-not-a-limit
node: craft.idioms.id-generation
type: qa
step: 2
---
## Q
**ID 生成 · 订单号补零格式的两个坑**｜写法

订票系统把订单号格式化成 `PNR0001`，用 `f"PNR{n:04d}"`。流水号超过 9999 之后，这个格式会出什么问题？排序和分页依赖字符串顺序时尤其要小心。

## A
**要点。** `:04d` 中的 4 是最小宽度，不是上限：数字更长时直接变长，不会截断也不会报错。于是字符串长度不再固定，按字典序（字符串比较）排序时 `PNR10000` 排在 `PNR9999` 前面，「最新的订单」排错了。编号里要有可读的前缀可以，但顺序要靠数字本身或单独的序列字段。

```python
import itertools

n = itertools.count(9998)
ids = [f"PNR{next(n):04d}" for _ in range(4)]
print(ids)
print(sorted(ids) == ids)                                    # 按字符串排
print(sorted(ids, key=lambda s: int(s[3:])) == ids)          # 按数字部分排
print(len(f"{12345:04d}"))                                   # 宽度只是下限
```

实际输出：

```
['PNR9998', 'PNR9999', 'PNR10000', 'PNR10001']
False
True
5
```

**为什么。** 对用户展示的订单号和程序内部的排序键是两个用途。订单号为了好读可以带前缀和补零；需要顺序时，另存一个整数序号，或者宽度足够大、永远补到固定位数并在超限时报错。

**易错。** 凡是把数字拼进字符串当主键的地方，都要想「第 10 倍的量级会发生什么」：格式宽度、排序、范围查询（`BETWEEN 'PNR0001' AND 'PNR9999'` 会漏掉后面的订单）。
