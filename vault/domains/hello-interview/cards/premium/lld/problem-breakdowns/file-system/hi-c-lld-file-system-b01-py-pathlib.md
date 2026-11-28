---
id: hi-c-lld-file-system-b01-py-pathlib
node: lld.problem-breakdowns.file-system.beyond
type: qa
step: 2
---
## Q
**内存文件系统 · Python：路径解析用 `pathlib` 还是手写 `split`**｜拓展 · 加分

`PurePosixPath` 能帮路径解析吗？它会悄悄做哪些改写，哪些是面试需求不允许的？

## A
```python
from pathlib import PurePosixPath

assert PurePosixPath("/a//b/./c/").parts == ("/", "a", "b", "c")    # 连续斜杠、点、末尾斜杠都被抹平
assert PurePosixPath("/a/../b").parts == ("/", "a", "..", "b")      # 双点不会折叠（它不访问文件系统）
assert "/a/".split("/") == ["", "a", ""]                            # 手写 split 能看到空片段
```
- **"纯路径"的意思：** `PurePosix*` 只做字符串层面的解析，不碰磁盘，所以能放进内存文件系统；`Path` 会真的访问操作系统，不能用。
- **利与弊：** 它帮你处理了分隔符和 `.`，但把 `//`、末尾斜杠这类"应当报无效"的输入悄悄接受了；需求要求严格校验时，手写 `split` 再检查空片段更可控。
- **折中：** 先用 `split` 检查合法性，再交给 `PurePosixPath` 取 `parent`、`name` 等；或者只用它的 `.parts`。
- **一般规律：** 标准库的"宽容"是便利，也可能掩盖本应拒绝的输入；在边界处决定谁来校验。
- **何时不用：** 路径语义不是 POSIX 风格（比如盘符）或需要自定义转义时。
