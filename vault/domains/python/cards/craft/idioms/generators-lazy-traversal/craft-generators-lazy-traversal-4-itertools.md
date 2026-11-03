---
id: craft-generators-lazy-traversal-4-itertools
node: craft.idioms.generators-lazy-traversal
type: qa
step: 4
---
## Q
**生成器与惰性遍历 · `pairwise`、`islice`、`heapq.merge` 各自替掉了什么手写代码**｜写法

外卖结算要遍历相邻的切点，消息订阅要从日志中间取一批，最近门店要把两个方向各自有序的结果按距离归并。标准库有现成的惰性工具，用它们比手写循环好在哪，各有什么代价？

## A
**要点。** `itertools.pairwise`（3.10+）产出相邻两两配对，等价于 `zip(xs, xs[1:])`，但不复制切片，对任何可迭代对象都有效（包括生成器）。`itertools.islice` 从任意迭代器取一段，惰性且不复制。`heapq.merge` 把多个**已排序**的迭代器惰性地归并成一个有序序列，支持 `key=`，内存只和输入个数有关，所以能取「前 k 个」而不物化全部。

```python
# 1) pairwise (3.10+): 相邻两两配对, 不复制切片
cuts = [0, 9, 17, 24]
print("pairwise:", list(pairwise(cuts)))

# 2) islice 作用在 deque 上: deque 不支持切片, 只能从头数到 offset
log = deque(range(100))
print("islice(deque, 40, 43):", list(islice(log, 40, 43)), "(要先跳过前 40 个)")

# 3) 两个有序生成器按「离目标的距离」归并, 取最近的 k 个: heapq.merge 惰性归并
def down(vals, target):                    # 从目标向小的一侧, 逐个产出
    return (v for v in sorted((v for v in vals if v <= target), reverse=True))
def up(vals, target):
    return (v for v in sorted(v for v in vals if v > target))

vals, target, k = [3, 8, 15, 20, 21, 40], 17, 3
merged = heapq.merge(down(vals, target), up(vals, target), key=lambda v: abs(v - target))

print("最近的 3 个:", sorted(islice(merged, k)))
```

实际输出：

```
pairwise: [(0, 9), (9, 17), (17, 24)]
islice(deque, 40, 43): [40, 41, 42] (要先跳过前 40 个)
最近的 3 个: [15, 20, 21]
```

**代价。** `islice` 作用在 `deque` 上要从头数到 `offset`，是 O(offset)，不是 O(1)：`deque` 不支持切片，也没有随机访问中间的快捷路径。订阅者落后很多时，每次读取都先跳过一长段，会变慢。需要快速定位时，要给日志建位点索引，或者换成可随机访问的结构。

**易错。** 手写的双指针归并容易在边界上出错，`heapq.merge` 的前提是每个输入已经按同一个 `key` 有序；传入没排好序的输入不会报错，只会给出乱序的结果。
