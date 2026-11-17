---
id: errors-narrow-where-to-catch
node: errors.narrow-catch
type: qa
step: 6
---
## Q
文件去重工具要比较两个文件的内容，其中一个读不了。异常该在读文件的底层函数里捕获，还是在比较函数里，还是在最外层 `main` 里？

## A
**在最低的、既有上下文又能做决定的那一层捕获**

- **太低（`read` 内部）**：它不知道调用方想跳过、记录还是中止，只能吞掉或原样抛；
- **太高（`main`）**：丢了“哪个文件、哪一步”的上下文，一个文件读不了，整批都跟着失败；
- **比较函数正好**：它知道两边各是谁，可以把问题记在读不了的那一边；
- **把失败变成该文件的记录**：路径加类型名，别的文件照常处理；
- **同组的代表读不了**：从组里去掉它，由下一个成员接任，这也是只有这一层才知道的决定。

```python
def first_unreadable(a: str, b: str, read):
    for path in (a, b):                        # 逐个读：才知道是哪一边出的问题
        try: read(path)
        except OSError as e:
            return path, type(e).__name__      # 问题记在这个文件头上
    return None

def read(p):
    if p == "b.txt": raise PermissionError(p)

print(first_unreadable("a.txt", "b.txt", read))    # ('b.txt', 'PermissionError')
print(first_unreadable("a.txt", "c.txt", read))    # None
```

**知识点：**捕获的范围（Narrow Catch）
