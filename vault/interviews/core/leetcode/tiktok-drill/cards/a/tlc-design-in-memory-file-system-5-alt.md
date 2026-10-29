---
id: tlc-design-in-memory-file-system-5-alt
node: a.design-in-memory-file-system
type: qa
step: 5
---
## Q
**LC 588 设计内存文件系统**｜另一种解法

不用前缀树，只用一个目录集合加一个“路径 → 内容”字典，能不能实现 `FileSystem`？怎么写，什么时候选它，什么时候选前缀树？

## A
**扁平解法。** 目录存在 `dirs` 集合里（根 `/` 一开始就在），文件存在 `files` 字典里。`ls` 目录时扫描全部路径，取以 `目录路径 + "/"` 为前缀的那些，截掉前缀后取第一段作为直接子项名。

```python
class FlatFileSystem:
    def __init__(self) -> None:
        self.dirs: set[str] = {"/"}
        self.files: dict[str, str] = {}

    def ls(self, path: str) -> list[str]:
        if path in self.files:
            return [path.rsplit("/", 1)[-1]]
        prefix = path.rstrip("/") + "/"             # 带斜杠，避免 /a 匹配 /ab
        names = {p[len(prefix):].split("/", 1)[0]
                 for p in (*self.dirs, *self.files) if p != path and p.startswith(prefix)}
        return sorted(names)

    def mkdir(self, path: str) -> None:
        parts = path.split("/")[1:]
        for i in range(1, len(parts) + 1):          # 每一级祖先目录都要登记
            self.dirs.add("/" + "/".join(parts[:i]))

    def addContentToFile(self, filePath: str, content: str) -> None:
        self.mkdir(filePath.rsplit("/", 1)[0] or "/")
        self.files[filePath] = self.files.get(filePath, "") + content

    def readContentFromFile(self, filePath: str) -> str:
        return self.files[filePath]
```

运行：`mkdir("/a/b/c")`、写入 `/a/b/c/d` 为 `"hello"` 之后，`ls("/")` → `['a']`，`ls("/a/b/c")` → `['d']`，`readContentFromFile("/a/b/c/d")` → `'hello'`。

**复杂度。** `mkdir` / `add` / `read` 是 `O(L)`；`ls` 是 `O(P · L)`，`P` 是已有路径数。这里 `P` 至多几百，够用。

**什么时候选哪个。** 调用只有 `300` 次，扁平解法写得快、不容易出结构性错误，适合先口述作为基线；前缀树在 `ls` 频繁、目录很大、要支持 `rm` / `mv`（整棵子树一次摘挂）时明显更好，且 `ls` 只与子项数有关，与全局路径数无关。扁平解法的坑：前缀不带 `/` 会让 `ls("/a")` 把 `/ab` 的 `b` 当成子项；空目录必须显式记在 `dirs` 里，否则 `ls` 不到。
