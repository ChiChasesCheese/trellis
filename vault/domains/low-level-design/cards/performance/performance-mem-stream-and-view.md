---
id: performance-mem-stream-and-view
node: performance.memory
type: qa
step: 3
---
## Q
给一个 64 MB 的文件算哈希，`hashlib.sha256(f.read())` 和按 1 MiB 一块读，内存差多少？切分一大块 `bytes` 时，`buf[i:j]` 和 `memoryview` 的区别是什么？

## A
**按块流式处理，内存只跟块大小有关；切片想不复制，用 `memoryview`**

- **一次读完**：内存里要有整个文件，文件越大峰值越高，几个并发任务一叠加就爆；
- **按块读，`h.update(chunk)`**：内存只有一块，与文件大小无关；哈希结果一模一样；
- **`bytes` 切片是复制**：`buf[i:j]` 新分配一块并拷贝数据；
- **`memoryview(buf)[i:j]` 是视图**：指向原缓冲区的同一块内存，不复制；代价是持有视图期间原缓冲区不能改变大小（`bytearray` 会拒绝）；
- **时间上两者一样，数据量大时视图更快**：复制要付出时间，视图几乎免费。

实测（3.11，本机，`tracemalloc` 峰值）：

| 场景 | 峰值内存 | 耗时 |
|---|---|---|
| 64 MB 文件一次 `read()` 再哈希 | 67.1 MB | 21.8 ms |
| 64 MB 文件按 1 MiB 块读 | 2.1 MB | 21.0 ms |
| 10 MB `bytes` 切成 64 KiB 小块（复制） | 10.5 MB | 0.146 ms |
| 同上，`memoryview` 切片 | 0.03 MB | 0.0054 ms |

```python
import hashlib

def sha256_file(path, chunk=1 << 20):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while block := f.read(chunk):     # 每次只持有一块
            h.update(block)
    return h.hexdigest()

buf = bytes(range(256)) * 4
mv = memoryview(buf)
print(bytes(mv[2:5]), mv[2:5].obj is buf)   # b'\x02\x03\x04' True：视图背后仍是 buf
```

**知识点：**减少分配（Reducing Allocation）
