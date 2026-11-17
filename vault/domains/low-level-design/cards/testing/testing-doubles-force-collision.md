---
id: testing-doubles-force-collision
node: testing.doubles
type: qa
step: 4
---
## Q
去重程序先按哈希分桶，再在桶内逐字节确认。真实数据里几乎碰不到哈希碰撞，「桶内逐字节确认」这段代码怎么测？

## A
**把哈希换成常量函数，人造碰撞**

- **难碰到的分支靠注入**：摘要函数做成可传入的参数；测试传一个对所有输入返回同一个值的函数，所有内容落进同一个桶；
- **断言结果仍按字节分组**：不同内容必须被分开，相同内容必须在一起；
- **证明确认步骤不是摆设**：如果去掉最后一步，这个测试会红；
- **替身越简单越好**：常量函数比写一个「找得到碰撞的哈希」可靠得多；
- **同类做法**：让时钟永远不前进、让随机源总是返回最大值，用极端的替身走到极端的分支。

```python
import hashlib

def group(blobs, digest=lambda b: hashlib.sha256(b).digest()):
    buckets = {}
    for i, b in enumerate(blobs): buckets.setdefault(digest(b), []).append(i)
    groups = []
    for idxs in buckets.values():
        by_bytes = {}
        for i in idxs: by_bytes.setdefault(blobs[i], []).append(i)   # 桶内按字节确认
        groups += by_bytes.values()
    return sorted(groups)

blobs = [b"aa", b"bb", b"aa"]
print(group(blobs))                              # [[0, 2], [1]]
print(group(blobs, digest=lambda b: b"same"))    # [[0, 2], [1]]：人造碰撞，结果不变
```

**知识点：**测试替身（Test Doubles）
