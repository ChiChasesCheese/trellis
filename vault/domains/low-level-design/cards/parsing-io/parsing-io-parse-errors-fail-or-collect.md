---
id: parsing-io-parse-errors-fail-or-collect
node: parsing-io.parse-errors
type: qa
step: 6
---
## Q
批量导入一个 CSV，其中几行有错；解析一份配置文件，中间有一处语法错。各自应该「遇错立刻失败」，还是「记下错误继续往下」？

## A
**行相互独立就收集，一份文档内部就停下**

- **独立的记录**：每行是一个请求，第 3 行坏不影响第 4 行；收集所有错误并带上行号，一次报给使用者，改完不必再跑十遍；
- **同一份文档**：一个引号没闭合，后面所有内容的含义都变了；继续解析只会连锁地冒出一串假错误，遇第一个错误就停；
- **折中：同步点**：编译器遇错后跳到下一个分号或换行，再继续找下一处错误，前提是语法里有可靠的同步点；
- **整体要不要成功**：「全部有效才提交」就收集错误后整批拒绝；「尽量导入」就把好行入库，坏行单独输出；这是业务决定，要写进合同；
- **不要静默丢行**：被丢掉的行必须计数、报告，不然 100 行进、97 行出没人知道。

```python
def load(lines: list[str]):
    ok, errors = [], []
    for n, line in enumerate(lines, start=1):
        try:
            ok.append(int(line))
        except ValueError:
            errors.append((n, f"not an integer: {line!r}"))      # 带行号收集
    return ok, errors

print(load(["1", "x", "3", ""]))     # ([1, 3], [(2, "not an integer: 'x'"), (4, "not an integer: ''")])
```

**知识点：**解析错误（Parse Errors）
