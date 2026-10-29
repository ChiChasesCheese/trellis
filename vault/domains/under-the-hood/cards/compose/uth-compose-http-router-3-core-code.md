---
id: uth-compose-http-router-3-core-code
node: compose.http-router
type: qa
step: 3
---
## Q
**不到 30 行写出路由器**｜httprouter · v1.3.0（简化）

把「方法表 + 树」写成一个 Python 类：注册和查找各读写哪些结构？哪些不变量必须一直成立？

## A
**不变量。**

- 同一个节点下，静态段和占位符不能并存（httprouter 在注册时直接 panic），所以查找永远只有一条路，不用回溯
- 一条完整路径至多挂一个处理函数
- 查找只读：注册全做完之后，多个线程并发查找也不用加锁

**顺序。** 注册：取（或建）方法的树根，逐段下行、缺了就建，最后在终点挂处理函数。查找：取方法的树根，逐段下行，静态段优先，占位符把整段记成参数，终点有处理函数才算命中。

```python
from typing import Callable


class Node:
    def __init__(self) -> None:
        self.kids: dict[str, Node] = {}              # 下一段 -> 子节点；占位符段统一用键 ""
        self.pname = ""                              # 占位符的参数名
        self.handler: Callable | None = None


class Router:
    def __init__(self) -> None:
        self.trees: dict[str, Node] = {}             # 方法 -> 这个方法的树根

    def add(self, method: str, pattern: str, handler: Callable) -> None:
        node = self.trees.setdefault(method, Node())
        for seg in filter(None, pattern.split("/")):
            key = "" if seg[0] == ":" else seg       # 真实的段不会是空串，所以 "" 可以当占位符的键
            if node.kids and (key == "") != ("" in node.kids):
                raise ValueError(f"冲突: {pattern}")  # 同一层静态段和占位符不能并存
            if key == "":
                node.pname = seg[1:]
            node = node.kids.setdefault(key, Node())
        node.handler = handler

    def find(self, method: str, path: str) -> tuple[Callable | None, dict[str, str]]:
        node, params = self.trees.get(method, Node()), {}
        for seg in filter(None, path.split("/")):
            child = node.kids.get(seg)               # 静态段优先
            if child is None and "" in node.kids:
                params[node.pname], child = seg, node.kids[""]   # 占位符吃下这一整段
            if child is None:
                return None, {}
            node = child
        return node.handler, params
```

**坑。** 这里按 `/` 切段，httprouter 按字节压缩；这里忽略末尾 `/`，httprouter 会区分并给出重定向建议。

**例题：** LC 588 设计内存文件系统

设计 `FileSystem`：`ls(path)` 列出目录内容（按字典序，文件路径则返回文件名），`mkdir(path)` 逐级创建目录，`addContentToFile(filePath, content)` 创建文件或追加内容，`readContentFromFile(filePath)` 读内容。路径是以 `/` 开头的绝对路径，四个方法合计至多 300 次调用。例：`mkdir("/a/b/c")`、`addContentToFile("/a/b/c/d", "hello")` 后，`ls("/")` → `["a"]`，`readContentFromFile("/a/b/c/d")` → `"hello"`。按 `/` 切成段、每段进入下一层字典，和 `add` 里的循环是同一种走法。

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
