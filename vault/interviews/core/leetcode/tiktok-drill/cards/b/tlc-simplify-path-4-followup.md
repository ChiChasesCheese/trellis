---
id: tlc-simplify-path-4-followup
node: b.simplify-path
type: qa
step: 4
---
## Q
**LC 71 简化路径**｜追问

面试官接着问：（1）输入是相对路径（不以 `/` 开头）怎么办？（2）能不能直接用标准库？（3）路径里有符号链接呢？

## A
1. **相对路径**：`..` 在栈空或者栈顶本身就是 `..` 时不能弹，而要保留（无处可退）；结果为空时返回 `"."`，也不再加开头的 `'/'`：

```python
def simplify_relative(path: str) -> str:
    stack: list[str] = []
    for part in path.split('/'):
        if part in ('', '.'):
            continue
        if part == '..':
            if stack and stack[-1] != '..':
                stack.pop()
            else:
                stack.append('..')           # 相对路径：无处可退时保留 ..
        else:
            stack.append(part)
    return '/'.join(stack) or '.'
```

   `simplify_relative("a/../../b")` → `"../b"`，`simplify_relative("a/..")` → `"."`，与 `posixpath.normpath` 的结果一致。
2. **标准库**：`posixpath.normpath` 规则基本相同，`normpath("/../")` 得到 `"/"`、`normpath("///a")` 得到 `"/a"`；但开头恰好两个 `/` 时它按 POSIX 保留（`normpath("//a/b")` 得到 `"//a/b"`），与题目要求不同。面试一般要求手写，标准库只用来对照。
3. **符号链接**：词法化简只处理文本。`a/link/..` 在真实文件系统里可能指向 `link` 目标的父目录，而不是 `a`；要得到真实路径需要逐段查文件系统（`os.path.realpath`），并处理环形链接。

**Python 提醒**：`'/'.join(stack) or '.'` 利用空串为假；`"a//b".split('/')` 得到 `['a', '', 'b']`，而 `str.split()` 不带参数才会把连续空白合并，别混淆。
