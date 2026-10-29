---
id: tlc-simplify-path-2-code
node: a.simplify-path
type: qa
step: 2
---
## Q
**LC 71 简化路径**｜写出 Python 实现

Unix 风格的绝对路径 `path`（长度 `1..3000`，由字母、数字、`'.'`、`'/'`、`'_'` 组成，以 `'/'` 开头）。写 `simplify_path(path)`，返回规范路径：`'.'` 忽略，`'..'` 回到上一级（根目录处忽略），连续斜杠合并，`'...'` 是普通名字，末尾无斜杠（根除外）。

## A
**思路。** `split('/')` 切段；`'..'` 弹栈（栈空时忽略），空串与 `'.'` 跳过，其他入栈；最后拼接。

```python
def simplify_path(path: str) -> str:
    stack: list[str] = []
    for part in path.split('/'):       # '//' 切出空串，'.' 与空串都只是噪声
        if part == '..':
            if stack:                  # 根目录没有上一级：栈空时忽略
                stack.pop()
        elif part and part != '.':     # '...' 之类是合法名字，照常入栈
            stack.append(part)
    return '/' + '/'.join(stack)
```

运行：`"/home/"` → `"/home"`，`"/home//foo/"` → `"/home/foo"`，`"/home/user/Documents/../Pictures"` → `"/home/user/Pictures"`，`"/../"` → `"/"`，`"/.../a/../b/c/../d/./"` → `"/.../b/d"`，`"/"` → `"/"`，`"/a/./b/../../c/"` → `"/c"`。

**复杂度。** 时间 `O(n)`：`split` 和遍历各 `O(n)`；空间 `O(n)`：切分结果和栈。

**写法要点。** `str.split('/')` 对连续斜杠产生空串，对开头和结尾的 `'/'` 也各产生一个空串，统一用 `part and ...` 过滤，不用单独处理。`elif part and part != '.'` 用真值判断空串，比 `len(part) > 0` 短。`'/' + '/'.join(stack)` 在栈空时自然得到 `"/"`，不需要分支。栈用 `list` 的 `append` / `pop()`（尾部 `O(1)`）。
