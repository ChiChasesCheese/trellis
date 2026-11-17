---
id: debugging-origins-bisect-stages
node: debugging.failure-origins
type: qa
step: 3
---
## Q
一条处理流水线有八个阶段，最终输出的价格不对。每一阶段都插一堆 `print` 太乱，怎么用最少的检查找到第一个把数据弄坏的阶段？

## A
**对阶段输出二分：检查中间结果“还对不对”，每次砍掉一半**

- **先写一个“对不对”的判定**：它只看中间结果，比如价格非负、条目数不变、没有重复；
- **错误一旦出现就会一直传下去**：判定对前半段为真、对后半段为假；二分找到真变假的那个位置，就是出错的阶段；
- **八个阶段只要看三次**；一百个阶段只要看七次；
- **前提要成立**：后面的阶段不能把错值“修好”（比如最后一步截断负数，掩盖了前面的错）；有这种阶段，要分段查；
- **找到阶段后，再在阶段内部重复同样的做法**，直到定位到一行。

```python
def first_bad(stages, data, ok):
    outs, x = [], data
    for f in stages: x = f(x); outs.append(x)
    lo, hi = 0, len(outs) - 1            # 约定：最终输出 outs[hi] 是错的
    while lo < hi:
        mid = (lo + hi) // 2
        if ok(outs[mid]): lo = mid + 1   # 这里还对：问题在后半段
        else: hi = mid
    return lo

stages = [lambda xs: [x for x in xs if x],     # 0 去掉空值
          lambda xs: [x * 100 for x in xs],    # 1 换成分
          lambda xs: [x - 500 for x in xs],    # 2 缺陷：多减了一笔
          lambda xs: sorted(xs)]               # 3
print(first_bad(stages, [3, 0, 4, 9], ok=lambda xs: all(x >= 0 for x in xs)))   # 2
```

**知识点：**追踪失败源头（Tracking Failure Origins）
