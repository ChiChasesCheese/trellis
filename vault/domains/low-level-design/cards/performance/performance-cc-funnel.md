---
id: performance-cc-funnel
node: performance.complexity-constants
type: qa
step: 4
---
## Q
要在几万个文件里找出内容完全相同的重复文件。直接对每个文件算完整哈希，为什么太贵？“漏斗”式的分层比较怎么排顺序，每一层要满足什么条件才不会漏掉真重复？

## A
**由便宜到贵逐层过滤，每层只放行“可能相同”的**

- **第一层：文件大小**，一次 `stat` 就有，不读内容；大小不同的文件不可能相同，大小唯一的文件直接出局；
- **第二层：前 4 KiB 的哈希**，只读一小块；抽样摘要不同就不同，相同才进下一层；
- **第三层：完整哈希**，读全文件，只对前面都撞上的少数文件做；
- **每层都只能排除、不能误排**：相同的文件必然大小相同、前缀相同，所以这两个条件是“必要条件”，不会漏掉真重复；
- **进入下一层的条件是组里 ≥ 2 个**：只有一个文件的组没有同伴，不用再算。

实测（3.11，本机，200 个约 1 MB 的文件，文件缓存已热）：全部 `stat` 0.20 ms；各读前 4 KiB 做 SHA-256 共 1.9 ms；整个读完做 SHA-256 共 68 ms。冷磁盘上读整个文件会更慢，层与层的差距只会更大。

```python
import hashlib, os
from collections import defaultdict

def group(paths, key):
    g = defaultdict(list)
    for p in paths: g[key(p)].append(p)
    return [v for v in g.values() if len(v) > 1]     # 只留有同伴的组

def head(p):
    with open(p, "rb") as f: return hashlib.sha256(f.read(4096)).digest()

def duplicates(paths, full):       # full：完整哈希函数
    return [d for s in group(paths, os.path.getsize)
              for h in group(s, head) for d in group(h, full)]
```

<details class="pt"><summary>延伸</summary>

哈希相同不等于内容相同（极小概率碰撞）。如果误判的代价是删掉用户文件，最后一层要逐块比较内容，并在第一处不同就停。

</details>

**知识点：**复杂度与常数（Complexity vs Constants）
