---
id: tlc-design-in-memory-file-system-0-whole
node: b.design-in-memory-file-system
type: qa
---
## Q
**LC 588 设计内存文件系统**｜Hard · TikTok 高频

设计内存文件系统类 `FileSystem`：`ls(path)`，`path` 是文件路径时只返回含该文件名的列表，是目录路径时返回目录里所有文件名和子目录名，结果按字典序；`mkdir(path)`，按路径创建目录，中间缺失的目录也要创建；`addContentToFile(filePath, content)`，文件不存在就创建，存在就把 `content` 追加到原内容末尾；`readContentFromFile(filePath)`，返回文件内容。路径都是绝对路径，除根目录 `/` 外都以 `/` 开头、不以 `/` 结尾；`1 <= path.length, filePath.length <= 100`；名字只含小写字母，同一目录下没有重名；操作参数都有效（不会读不存在的文件，`ls` 的路径存在），`addContentToFile` 的父目录一定存在；`1 <= content.length <= 50`；四个方法合计至多调用 `300` 次。例：`ls("/")` → `[]`；`mkdir("/a/b/c")`；`addContentToFile("/a/b/c/d", "hello")`；`ls("/")` → `["a"]`；`readContentFromFile("/a/b/c/d")` → `"hello"`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 用前缀树（trie）模拟目录树：每个节点有 `children` 字典和 `content`（`None` 表示目录，字符串表示文件）；四个操作都先沿路径逐级走到目标节点，再做各自的事。每次操作 `O(L)`，`ls` 额外对子项排序。

**识别。** 「路径、层级、目录」是树；按名字逐级往下查是前缀树（trie）；`ls` 要字典序，所以取 `children` 的键再 `sorted`；目录与文件的区别用一个字段表示，`content is None` 就是目录。这是设计题（class design），考点是数据结构的选择和边界，不是难算法。

**推导。** 暴力：一个扁平字典 `路径 → 内容`，`ls` 扫描所有路径找直接子项，300 次调用也够快。浪费：每次 `ls` 重扫全部路径，而目录结构本来就是一棵树。洞察：把路径按 `/` 拆开，每一段对应一层子字典；`mkdir` 与 `addContentToFile` 沿路径创建缺失节点，`ls` 与 `read` 沿路径查找，`ls` 只需要看当前节点的 `children`。

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

**复杂度。** 每次操作 `O(L)`（`L` 是路径长度，最多 `100`）；`ls` 另加 `O(k log k)` 排序 `k` 个子项；空间是所有名字的总长。

**易错点。**
- `"/".split("/")` 得到 `['', '']`，不过滤空串就会在根下多出一层名为 `""` 的节点：`mkdir("/a")` 后 `ls("/")` 抛出 `KeyError: ''`。用 `filter(None, ...)`。
- `ls` 作用在文件路径上要返回 `[文件名]`；只看 `children` 会得到 `[]`，`ls("/a/b/c/d")` 应是 `['d']`。
- 追加不是覆盖：写成 `node.content = content`，第二次追加后 `/a/b/c/d` 读出 `' world'`，旧内容丢了。

**追问。**
- 文件很大、频繁追加：`content` 存成片段列表，读取时 `"".join`，追加是摊还 `O(1)`，不会反复复制整个字符串。
- 加 `rm` / `mv`：删除是 `parent.children.pop(name)`，移动是摘下子树再挂到新父节点，整棵子树一次完成，这是树比扁平字典强的地方。
- 并发访问：每个目录节点一把锁，沿路径逐级加锁（hand-over-hand），或整体读写锁。

**同模式。** LC 1166 设计文件系统、LC 208 实现前缀树、LC 642 设计搜索自动补全系统、LC 609 在系统中查找重复文件。
