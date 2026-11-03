---
id: craft-default-forms-1-min-default
node: craft.idioms.default-forms
type: qa
step: 1
---
## Q
**省掉标志变量 · `min(..., default=None)` 为什么能同时表达「最小够用」和「编号小优先」**｜写法

餐厅候位要给一团客人选桌：能坐下的空闲桌里选容量最小的（大桌留给大团），容量相同选编号小的，没有就等。标志变量版本要维护「当前最佳桌」和「当前最佳容量」两个变量。一行 `min` 就解决了，靠的是什么？

## A
**要点。** 两个关键：（1）**元组键**。`min` 比较元组时先比第一项，相等再比第二项，所以键 `(容量, 桌号)` 一次表达两条规则，不需要手写 `if`。（2）**`default=`**。`min` 对空序列默认抛 `ValueError`，加上 `default=None` 后「没有够用的桌」就是返回 `None`，不用事先判断是否为空，也不用 `try / except`。

```python
# 规则: 能坐下的空闲桌里选最小的(大桌留给大团), 容量相同取编号小的
sizes = [2, 4, 4, 6, 2]
free = {0, 1, 2, 3, 4}

def best_fit_flags(size):
    best = None
    best_cap = None
    for t in sorted(free):                       # 标志变量版: 三个状态要同步更新
        if sizes[t] >= size:
            if best is None or sizes[t] < best_cap:
                best, best_cap = t, sizes[t]
    return best

def best_fit(size):
    # 键 (容量, 桌号) 一次表达两条规则: 先比容量, 容量相同再比桌号
    fit = min(((sizes[t], t) for t in free if sizes[t] >= size), default=None)
    return None if fit is None else fit[1]

for need in (2, 3, 6, 7):
    print(f"{need} 人:", best_fit_flags(need), best_fit(need))

print("空序列 min 抛错:", end=" ")
try:
    min([])
except ValueError as e:
    print(e)
print("多个位置参数时不能用 default:", end=" ")
try:
    min(1, 2, default=0)
except TypeError as e:
    print(e)
```

实际输出（Python 3.14；3.12 及更早，空序列的报错文字是 `min() arg is an empty sequence`）：

```
2 人: 0 0
3 人: 1 1
6 人: 3 3
7 人: None None
空序列 min 抛错: min() iterable argument is empty
多个位置参数时不能用 default: Cannot specify a default for min() with multiple positional arguments
```

**为什么。** 标志变量版本每多一条规则就多一个要同步更新的变量，漏更新一个就是只在特定输入下出现的 bug。元组键把规则写成**数据**，而不是控制流。

**易错。** `default=` 只对单个可迭代参数的形式生效，`min(a, b, default=0)` 是 `TypeError`。如果元素本身可能是 `None`，返回 `None` 就分不清是「没有」还是「就是 None」；上面的写法返回的是 `(容量, 桌号)` 元组，所以没有歧义。
