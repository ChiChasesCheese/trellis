---
id: tlc-patterns-string-parsing-6-small-parsers
node: patterns.string-parsing
type: qa
step: 6
---
## Q
**字符串处理与表达式解析｜小型解析器：比较版本号（LC 165）与简化路径（LC 71）**

版本号为什么不能当字符串比较？路径简化为什么用栈？

## A
**LC 165**：按 `.` 拆成修订号，逐段转成整数比较；缺失的修订号当作 `0`；`int()` 自动去掉前导零。

```python
from itertools import zip_longest
def compare_version(version1: str, version2: str) -> int:
    for x, y in zip_longest(version1.split("."), version2.split("."), fillvalue="0"):
        if int(x) != int(y):
            return -1 if int(x) < int(y) else 1
    return 0
print(compare_version("1.2", "1.10"), compare_version("1.01", "1.001"), compare_version("1.0", "1.0.0.0"), compare_version("1.0.1", "1"))   # -1 0 0 1
```

- 不能字符串比较：`"1.2" < "1.10"` 在 Python 里是 `False`（第 3 个字符 `'2' > '1'`），而版本 `1.2 < 1.10`。
- `zip_longest(..., fillvalue="0")` 把短的补 `0`，`"1.0"` 与 `"1.0.0.0"` 相等。
- 时间 `O(n + m)`；`split` 之后用迭代，不额外建完整数字列表也可以。

**LC 71 简化 Unix 路径**：按 `/` 拆开；空段和 `.` 忽略；`..` 弹出上一级（根目录再向上还是根）；其他名字（包括 `...`）入栈。

```python
def simplify_path(path: str) -> str:
    stack: list[str] = []
    for part in path.split("/"):
        if part in ("", "."):
            continue                       # 空段（连续斜杠）和 "." 都忽略
        if part == "..":
            if stack:
                stack.pop()
        else:
            stack.append(part)             # 包括 "..." 这类合法名字
    return "/" + "/".join(stack)
print(simplify_path("/home//foo/"), simplify_path("/home/user/Documents/../Pictures"), simplify_path("/../"), simplify_path("/.../a/../b/c/../d/./"))   # /home/foo /home/user/Pictures / /.../b/d
```
