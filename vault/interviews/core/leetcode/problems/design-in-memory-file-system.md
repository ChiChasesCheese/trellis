---
slug: design-in-memory-file-system
---
## Q
**LC 588 设计内存文件系统**｜Hard

设计 `FileSystem`：`ls`（目录列子项并按字典序，文件只返回自己的名字）、`mkdir`（缺失的中间目录一并创建）、`addContentToFile`（追加内容）、`readContentFromFile`。

## A
**一句话。** 用 Trie 模拟目录树：节点有 `children` 和 `content`（`None` 是目录），每个操作先沿路径走到目标节点。

```python
class Entry:
    def __init__(self):
        self.children = {}
        self.content = None     # None 是目录，字符串是文件

class FileSystem:
    def __init__(self):
        self.root = Entry()

    def _walk(self, path, create=False):
        node = self.root
        for name in filter(None, path.split("/")):  # 去掉空串
            if create:
                node = node.children.setdefault(name,
                                                Entry())
            else:
                node = node.children[name]
        return node

    def ls(self, path):
        node = self._walk(path)
        if node.content is not None:    # 文件：返回自己的名字
            return [path.rsplit("/", 1)[-1]]
        return sorted(node.children)

    def mkdir(self, path):
        self._walk(path, create=True)

    def addContentToFile(self, filePath, content):
        node = self._walk(filePath, create=True)
        node.content = (node.content or "") + content   # 追加

    def readContentFromFile(self, filePath):
        return self._walk(filePath).content or ""
```

**复杂度。** 时间 每次 `O(L)`，`ls` 另加排序，空间 `O(名字总长)`。

**易错点。**
- 不过滤空串：`"/".split("/")` 是 `['','']`，`mkdir("/a")` 后 `ls("/")` 抛 `KeyError`。
- `ls` 文件路径只看 `children`：`ls("/a/b/c/d")` 得 `[]`，应为 `['d']`。
- 追加写成覆盖：第二次追加后旧内容丢了。

**追问。**
- 文件很大、频繁追加？：`content` 存片段列表，读取时再 `join`，追加摊还 `O(1)`。
- 怎么加 `rm` / `mv`？：删除是 `parent.children.pop(name)`，移动是摘下子树挂到新父节点。

**同模式。** LC 1166 设计文件系统、LC 208 实现前缀树、LC 642 设计搜索自动补全系统、LC 609 在系统中查找重复文件
