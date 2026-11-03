---
id: craft-bisect-sorted-lists-1-floor-ceiling
node: craft.idioms.bisect-sorted-lists
type: qa
step: 1
---
## Q
**bisect 与有序列表 · `bisect_left` 和 `bisect_right` 到底差在哪，生效版本该用哪个**｜写法

价格表按生效时间排好序，查询某一时刻的价格要找「最后一个不晚于该时刻的版本」。恰好等于生效时间的请求应该属于新版本还是旧版本？`bisect_left` 和 `bisect_right` 选哪个，`-1` 加在哪里？

## A
**要点。** 在有序列表 `a` 里二分查找 `x` 的**插入点**：`bisect_left(a, x)` 是插入到相等元素的**左边**，即第一个 `>= x` 的下标（ceiling）；`bisect_right(a, x)` 是插到相等元素的**右边**，即第一个 `> x` 的下标。所以「最后一个 `<= x`」（floor）是 `bisect_right(a, x) - 1`；「最后一个 `< x`」是 `bisect_left(a, x) - 1`。恰好等于生效时间属于新版本，就是 floor：用 `bisect_right`。

```python
starts = [10, 20, 20, 30]      # 有序；注意 20 出现两次

def floor_idx(a, x):   return bisect_right(a, x) - 1     # 最后一个 <= x 的下标
def lower_idx(a, x):   return bisect_left(a, x) - 1      # 最后一个 <  x 的下标
def ceiling_idx(a, x): return bisect_left(a, x)          # 第一个 >= x 的下标
def higher_idx(a, x):  return bisect_right(a, x)         # 第一个 >  x 的下标

for x in (5, 20, 25, 99):
    f, c = floor_idx(starts, x), ceiling_idx(starts, x)
    print(f"x={x:>2}  floor 下标 {f:>2}  ceiling 下标 {c}")

# 生效版本: 价格从 effective_from 开始生效; 恰好等于生效时间的请求属于新版本
effective = [100, 200, 300]
prices = ["v1", "v2", "v3"]
def version_at(t):
    i = bisect_right(effective, t) - 1       # 最后一个 effective <= t
    return prices[i] if i >= 0 else None
print([ (t, version_at(t)) for t in (99, 100, 199, 200, 350) ])
# 若用 bisect_left - 1: 恰好 200 的请求会落到旧版本 v1(错)
print("bisect_left 写法在 t=200:", prices[bisect_left(effective, 200) - 1])
```

实际输出：

```
x= 5  floor 下标 -1  ceiling 下标 0
x=20  floor 下标  2  ceiling 下标 1
x=25  floor 下标  2  ceiling 下标 3
x=99  floor 下标  3  ceiling 下标 4
[(99, None), (100, 'v1'), (199, 'v1'), (200, 'v2'), (350, 'v3')]
bisect_left 写法在 t=200: v1
```

**为什么。** 把 `bisect` 想成「插入点」比想成「查找」更不容易记错：新元素放在相等元素的左边还是右边。floor 要把相等的元素也算进去，所以插入点放在它们的右边，再退一位。

**易错。** 结果为 `-1` 表示没有这样的元素（请求早于最早的版本），必须单独处理，否则 `a[-1]` 会静默取到最后一个版本，答案完全错。
