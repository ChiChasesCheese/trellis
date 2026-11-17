---
id: parsing-io-streams-external-sort
node: parsing-io.streams
type: qa
step: 5
---
## Q
一个文本文件有 100 GB，内存只有 8 GB，要按行排序。`sorted(f)` 做不到，怎么办？

## A
**外部排序：分块排好存盘，再多路归并**

- **第一步，生成有序的段（run）**：每次读一块能放进内存的行，在内存里排好，写成一个临时文件；
- **第二步，k 路归并**：同时打开所有段，每段只在内存里留一行，`heapq.merge` 每次取出最小的那一行；
- **内存**：约为一块的大小，加上 k 行；与总大小无关；
- **磁盘**：每行读写常数遍，总代价是 O(n log n) 的比较加两遍顺序读写；
- **段太多时**：同时打开的文件数有上限；先把段分批归并成更大的段，多做几轮。

```python
import heapq, itertools, tempfile

def runs(lines, size: int):
    it = iter(lines)
    while chunk := list(itertools.islice(it, size)):      # 每次最多 size 行
        f = tempfile.TemporaryFile("w+")
        f.writelines(sorted(chunk)); f.seek(0)
        yield f

def external_sort(lines, size: int = 3):
    return heapq.merge(*runs(lines, size))                # 每个文件一次只出一行

print([s.strip() for s in external_sort(f"{c}\n" for c in "dbfaecg")])   # ['a', 'b', ..., 'g']
```

<details class="pt"><summary>延伸</summary>

`heapq.merge` 要求每个输入本身有序，它是惰性的，所以输出可以直接写文件而不建列表。数据只要部分有序（日志按时间到达），选一个对应的归并策略比全排更便宜。

</details>

**知识点：**流式处理大文件（Streaming Large Files）
