---
id: craft-generators-lazy-traversal-6-scales-cursor
node: craft.idioms.generators-lazy-traversal
type: qa
step: 6
---
## Q
**生成器与惰性遍历 · 从嵌套列表迭代器到游标分页**｜写法

LeetCode 的 Flatten Nested List Iterator 要求一次只展开一个；LLD 的文件搜索是惰性的前序遍历；一个 API 要返回几百万行时，同样的「别一次全拿」怎么落到服务上？

## A
**要点。** 三个尺度同一个思想：**消费者拉取，生产者暂停**。LeetCode 里是栈里放迭代器、遇到嵌套才压入；LLD 里是显式栈加 `yield`；服务里是**游标分页**：每次返回一页加「下一页从哪里开始」的游标，服务端不保存整个结果，每次请求都是一个小而独立的查询。

```python
# LeetCode 341 Flatten Nested List Iterator: 迭代器 + 显式栈, 只在被问到时才展开
class NestedIterator:
    def __init__(self, nested: list) -> None:
        self._stack = [iter(nested)]                  # 栈里放「迭代器」, 而不是展开后的列表

    def __iter__(self): return self

    def __next__(self) -> int:
        while self._stack:
            try:
                x = next(self._stack[-1])
            except StopIteration:
                self._stack.pop()                     # 这一层走完, 回到上一层
                continue
            if isinstance(x, list):
                self._stack.append(iter(x))           # 遇到嵌套: 压入, 先不展开
            else:
                return x
        raise StopIteration

# 系统里的同一件事: 游标分页。服务端不一次物化全部结果, 每次给一页 + 下一页的游标
ROWS = [(i, f"row{i}") for i in range(1, 11)]        # 按主键有序
IDS = [r[0] for r in ROWS]

def page(after_id: int, limit: int) -> tuple[list[tuple[int, str]], int | None]:
    start = bisect_right(IDS, after_id)               # 游标 = 上一页最后一行的主键
    rows = ROWS[start:start + limit]
    nxt = rows[-1][0] if len(rows) == limit else None
    return rows, nxt

def stream_all(limit: int) -> Iterator[tuple[int, str]]:
    cursor: int | None = 0
    while cursor is not None:
        rows, cursor = page(cursor, limit)            # 生成器把「分页」藏在后面
        yield from rows

print(list(NestedIterator([[1, [2, 3]], 4, [[5]]])))
print("第一页:", page(0, 4))
print("第二页:", page(4, 4)[1])
print("流式遍历的前 6 个主键:", [r[0] for _, r in zip(range(6), stream_all(4))])
```

实际输出：

```
[1, 2, 3, 4, 5]
第一页: ([(1, 'row1'), (2, 'row2'), (3, 'row3'), (4, 'row4')], 4)
第二页: 8
流式遍历的前 6 个主键: [1, 2, 3, 4, 5, 6]
```

**变化。** 进程内生成器的暂停点保存在内存里的栈帧；分布式里不能保存，状态必须**交给客户端**，也就是游标，它是上一页最后一行的主键，而不是页码。用游标比 `OFFSET n` 好：`OFFSET` 要跳过前 n 行，越翻越慢，期间有插入删除还会漏行或重复；游标定位在有序索引上，每页代价相同。

**代价。** 游标要求排序键稳定且唯一（主键，或主键加时间戳）；客户端拿到的是某一刻的视图，翻页期间的新增不保证出现。流式导出（逐行写到响应）是另一种方式，服务端要为每个连接保持住游标和资源，慢客户端会占住它们。

**信号。** 结果可能很大、调用方可能提前停、需要一页一页拉。
