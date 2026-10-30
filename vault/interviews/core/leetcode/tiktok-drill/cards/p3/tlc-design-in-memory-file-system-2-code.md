---
id: tlc-design-in-memory-file-system-2-code
node: p3.design-in-memory-file-system
type: qa
step: 2
---
## Q
**LC 588 设计内存文件系统**｜写出 Python 实现

实现 `FileSystem`：`ls(path)`、`mkdir(path)`、`addContentToFile(filePath, content)`、`readContentFromFile(filePath)`。路径是绝对路径（根为 `/`），`1 <= path.length <= 100`，名字只含小写字母，参数都有效，`ls` 按字典序，`addContentToFile` 是追加，四个方法合计至多 `300` 次调用。

## A
**思路。** 用前缀树（trie）。每个节点有 `children` 字典和 `content`，`None` 表示目录。写一个 `_walk(path, create)` 沿路径下行，`create=True` 时缺失的节点现建；四个方法都建立在它上面。

```python
class _Entry:
    def __init__(self) -> None:
        self.children: dict[str, "_Entry"] = {}
        self.content: str | None = None    # None 表示目录，字符串表示文件


class FileSystem:
    def __init__(self) -> None:
        self.root = _Entry()

    def _walk(self, path: str, create: bool = False) -> _Entry:
        node = self.root
        for name in filter(None, path.split("/")):     # "/" 拆出来是 ["", ""]，filter 去掉空串
            if create:
                node = node.children.setdefault(name, _Entry())
            else:
                node = node.children[name]
        return node

    def ls(self, path: str) -> list[str]:
        node = self._walk(path)
        if node.content is not None:                   # 文件：只返回它自己的名字
            return [path.rsplit("/", 1)[-1]]
        return sorted(node.children)

    def mkdir(self, path: str) -> None:
        self._walk(path, create=True)

    def addContentToFile(self, filePath: str, content: str) -> None:
        node = self._walk(filePath, create=True)
        node.content = (node.content or "") + content  # 追加，不是覆盖

    def readContentFromFile(self, filePath: str) -> str:
        return self._walk(filePath).content or ""
```

运行：新建后 `ls("/")` → `[]`；`mkdir("/a/b/c")` 并写入 `/a/b/c/d` 为 `"hello"` 后，`ls("/")` → `['a']`，`readContentFromFile("/a/b/c/d")` → `'hello'`，`ls("/a/b/c/d")` → `['d']`，`ls("/a/b/c")` → `['d']`；再追加 `" world"` 读出 `'hello world'`。

**复杂度。** 每次操作 `O(L)`；`ls` 另加 `O(k log k)` 排序 `k` 个子项；空间是所有名字的总长。

**写法要点。** 每个节点在 `__init__` 里新建自己的 `children` 字典，不要写成类属性，否则所有节点共享同一个字典；`filter(None, path.split("/"))` 一步去掉空段，根目录 `"/"` 自然得到空序列；`setdefault(name, _Entry())` 一次完成“有就取，没有就建”（每次会白造一个对象，规模小可以接受）；`rsplit("/", 1)[-1]` 取最后一段文件名；`(node.content or "") + content` 同时处理新建和追加。
