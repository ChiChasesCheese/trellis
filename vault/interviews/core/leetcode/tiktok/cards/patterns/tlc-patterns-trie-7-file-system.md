---
id: tlc-patterns-trie-7-file-system
node: patterns.trie
type: qa
step: 7
---
## Q
**字典树（Trie）｜路径树：设计内存文件系统（LC 588）**

文件系统的目录树和字典树是什么关系？`ls`、`mkdir`、读写文件各怎么做？

## A
路径按 `/` 分段，每一段就是树的一层——这和字典树"每个字符一层"完全同构，只是"字符"换成了"目录名 / 文件名"。

```python
class FileSystem:
    def __init__(self) -> None:
        self.root: dict = {}               # 目录：{名字: 子节点}；文件：用空字符串键存内容

    def _walk(self, path: str, create: bool) -> dict:
        node = self.root
        for name in filter(None, path.split("/")):   # filter(None, ...) 去掉根路径产生的空串
            node = node.setdefault(name, {}) if create else node[name]
        return node

    def ls(self, path: str) -> list[str]:
        node = self._walk(path, False)
        if "" in node:                     # 文件：只返回自己的名字
            return [path.rsplit("/", 1)[1]]
        return sorted(node)                # 目录：子项名字按字典序

    def mkdir(self, path: str) -> None:
        self._walk(path, True)             # 中间目录不存在时一并创建

    def addContentToFile(self, filePath: str, content: str) -> None:
        node = self._walk(filePath, True)
        node[""] = node.get("", "") + content

    def readContentFromFile(self, filePath: str) -> str:
        return self._walk(filePath, False)[""]

fs = FileSystem()
print(fs.ls("/"))                          # []
fs.mkdir("/a/b/c")
fs.addContentToFile("/a/b/c/d", "hello")
print(fs.ls("/"), fs.readContentFromFile("/a/b/c/d"), fs.ls("/a/b/c/d"))   # ['a'] hello ['d']
```

- 名字只含小写字母，不会出现空字符串名字，所以空字符串键可以安全地表示"这是文件，值是内容"。
- `ls` 对文件路径只返回文件名；对目录返回排序后的子项，不含内容键（目录节点里没有 `""` 键）。
- 路径长度 `<= 100`，每个操作 `O(路径深度 + 子项数 log)`。
- 要加 `rm`、`mv` 时，节点用类封装 `is_file`、`content`、`children` 更清楚。
