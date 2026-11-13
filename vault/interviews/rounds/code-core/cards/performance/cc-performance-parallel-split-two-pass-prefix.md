---
id: cc-performance-parallel-split-two-pass-prefix
node: performance.parallel-split
type: qa
---
## Q
Parallelise the prefix sum `out[i] = a[0] + … + a[i]`. Every output seems to depend on the one before it — how can workers run at the same time?

## A
**Two passes over w chunks. Pass 1, in parallel: each worker sums its chunk. Then a serial prefix over just the w totals gives each chunk its offset. Pass 2, in parallel: each worker scans its chunk from its offset.**

```python
from concurrent.futures import ProcessPoolExecutor
from itertools import accumulate

def scan_chunk(args):
    chunk, offset = args
    return list(accumulate(chunk, initial=offset))[1:]

def parallel_prefix(a, workers=4):
    w = max(1, min(workers, len(a)))
    chunks = [a[len(a) * i // w: len(a) * (i + 1) // w] for i in range(w)]
    with ProcessPoolExecutor(max_workers=w) as ex:
        totals = list(ex.map(sum, chunks))            # pass 1: local sums
        offsets = list(accumulate(totals, initial=0))[:-1]  # serial, w items
        parts = ex.map(scan_chunk, zip(chunks, offsets))  # pass 2
        return [x for part in parts for x in part]
```

- **Walk-through.** `[3,1,4,1,5,9,2,6]`, w = 3: chunks `[3,1] [4,1,5] [9,2,6]`, totals 4, 10, 17, offsets 0, 4, 14. Chunk 2 from 4 → 8, 9, 14; chunk 3 from 14 → 23, 25, 31.
- **The price.** Each element is added twice: work 2n, time about 2n / w + w, so the best speedup is about w / 2.
- **Edges.** n = 0, n < w, w = 1 — check each against `itertools.accumulate`.
- **Complexity.** O(n) work, about O(n / w + w) time.

**Follow-ups.** 2D: prefix the rows in parallel, then the columns. Thousands of cores: a tree scan (Blelloch) in O(log n) steps, as on a GPU. Floats differ from serial in the last bits: compare with a tolerance.

## Q zh
把前缀和 `out[i] = a[0] + … + a[i]` 并行化。每个输出看起来都依赖前一个——worker 怎么同时跑？

## A zh
**分 w 块，扫两遍。第一遍并行：每个 worker 求自己那块的总和。然后只对这 w 个总和做一次串行前缀，得到每块的偏移量。第二遍并行：每个 worker 从自己的偏移量开始扫描自己那块。**

```python
from concurrent.futures import ProcessPoolExecutor
from itertools import accumulate

def scan_chunk(args):
    chunk, offset = args
    return list(accumulate(chunk, initial=offset))[1:]

def parallel_prefix(a, workers=4):
    w = max(1, min(workers, len(a)))
    chunks = [a[len(a) * i // w: len(a) * (i + 1) // w] for i in range(w)]
    with ProcessPoolExecutor(max_workers=w) as ex:
        totals = list(ex.map(sum, chunks))            # pass 1: local sums
        offsets = list(accumulate(totals, initial=0))[:-1]  # serial, w items
        parts = ex.map(scan_chunk, zip(chunks, offsets))  # pass 2
        return [x for part in parts for x in part]
```

- **走一遍。** `[3,1,4,1,5,9,2,6]`，w = 3：块 `[3,1] [4,1,5] [9,2,6]`，总和 4、10、17，偏移量 0、4、14。第 2 块从 4 起 → 8、9、14；第 3 块从 14 起 → 23、25、31。
- **代价。** 每个元素被加两次：工作量 2n，耗时约 2n / w + w，最好的加速比约 w / 2。
- **边界。** n = 0、n < w、w = 1——逐个和 `itertools.accumulate` 对比。
- **复杂度。** 工作量 O(n)，耗时约 O(n / w + w)。

**追问。** 二维：先并行处理各行，再并行处理各列。上千个核：树形扫描（Blelloch scan）只需 O(log n) 步，GPU 就这么做。浮点结果最后几位和串行不同：用容差比较。
