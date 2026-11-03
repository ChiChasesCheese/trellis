---
id: craft-bisect-sorted-lists-2-key-param
node: craft.idioms.bisect-sorted-lists
type: qa
step: 2
---
## Q
**bisect 与有序列表 · `key=` 比另存一个平行列表好在哪**｜写法

账本的历史余额按序号有序存成对象列表，要按序号二分。3.10 之前的写法是另存一个只含序号的列表。`bisect_right(hist, seq, key=lambda line: line.seq)` 省掉了什么风险？`key` 在哪些参数上生效有什么易错点？

## A
**要点。** 平行列表（parallel lists）是两份必须保持同步的数据：每次往对象列表里加、删、改，都要同样改序号列表。漏了一次，二分找到的下标就指向错的对象，而且没有任何报错。`key=`（3.10+）让 `bisect` 直接在对象列表上二分，只维护一份数据。`insort` 同样支持 `key=`。

```python
@dataclass(frozen=True)
class Line:
    seq: int
    balance_after: int

hist = [Line(1, 100), Line(3, 80), Line(7, 130)]

# 老写法: 另存一份平行的 seq 列表，两份要同步维护
seqs = [l.seq for l in hist]
# 新写法 (3.10+): key= 让 bisect 直接在对象列表上二分
def balance_at(seq: int) -> int:
    i = bisect_right(hist, seq, key=lambda line: line.seq)    # seq 本身不经过 key
    return hist[i - 1].balance_after if i else 0

print([balance_at(s) for s in (0, 1, 2, 3, 6, 7, 99)])

# 平行列表漂移: 往 hist 里插入新行, 忘了同步 seqs
insort(hist, Line(5, 90), key=lambda line: line.seq)          # insort 的 key 会同时作用于新元素
print("平行列表按旧 seqs 找 seq=5:", bisect_right(seqs, 5), "-> 下标 ", bisect_right(seqs, 5) - 1,
      "对应", hist[bisect_right(seqs, 5) - 1])
print("key= 找 seq=5:", hist[bisect_right(hist, 5, key=lambda l: l.seq) - 1])
```

实际输出：

```
[0, 100, 100, 80, 80, 130, 130]
平行列表按旧 seqs 找 seq=5: 2 -> 下标  1 对应 Line(seq=3, balance_after=80)
key= 找 seq=5: Line(seq=5, balance_after=90)
```

**易错。** 对 `bisect_left / bisect_right`，`key` 只作用于列表里的元素，**不作用于要查找的值** `x`：所以传的是 `seq` 本身，而不是一个 `Line`。对 `insort`，`key` 同时作用于列表元素和新元素，传入的是要插入的对象。另外，列表必须按这个 `key` 有序，否则二分的结果没有意义，也不会报错。

**为什么。** 每次现建一个 `[v.effective_from for v in versions]` 再二分，每次查询的代价是 O(n)，二分就白做了；`key=` 在二分过程中只对被探测的 O(log n) 个元素调用 key 函数。
