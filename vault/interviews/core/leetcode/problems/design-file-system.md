---
slug: design-file-system
---
## Q
**LC 1166 设计文件系统**｜Medium

设计文件系统：`createPath(path, value)` 创建新路径（如 `/a/b`）并关联值，仅当路径不存在且其父路径已存在时成功；`get(path)` 返回路径的值，不存在返回 `-1`。

## A
**一句话。** 用哈希表直接按完整路径存值；创建时取最后一个 `/` 之前的串当父路径，父路径必须已存在。

```python
class FileSystem:
    def __init__(self):
        self.d = {'': -1}                  # 根路径 '' 作为虚拟父节点

    def createPath(self, path, value):
        parent = path[:path.rindex('/')]   # 去掉最后一段
        if path in self.d or parent not in self.d:
            return False
        self.d[path] = value
        return True

    def get(self, path):
        return self.d.get(path, -1)
```

**复杂度。** 时间每次 `O(路径长度)`，空间 `O(路径总长度)`。

**易错点。**
- 根路径没处理：`/a` 的父路径是空串，哈希表里要预置 `''`。
- 不检查父路径：创建 `/a/b` 而 `/a` 不存在应失败。
- 忘了判重复创建：已存在的路径再创建也要返回 `False`。

**追问。**
- 为什么不用树？：题目只要求精确路径的读写，哈希表更简单；要列目录、删除子树时才需要 Trie 树。
- 同时支持 `ls`、`mkdir` 呢？：改成 Trie：每个节点有 `children` 字典和内容，逐段向下走。

**同模式。** LC 588 设计内存文件系统、LC 208 实现 Trie (前缀树)、LC 1472 设计浏览器历史记录
