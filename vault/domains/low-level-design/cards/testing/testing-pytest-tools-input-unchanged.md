---
id: testing-pytest-tools-input-unchanged
node: testing.pytest-tools
type: qa
step: 4
---
## Q
要测「分配函数不修改传入的列表」。测试里写 `before = data`，调用之后断言 `data == before`，永远是绿的。为什么？该怎么写？

## A
**调用前取副本，不是取别名**

- **别名**：`before = data` 只是给同一个列表起了第二个名字；函数改了它，两个名字一起变，比较自己和自己，恒为真；
- **副本**：`copy.deepcopy(data)` 是调用前的独立快照；嵌套结构要深拷贝，浅拷贝挡不住内层被改；
- **返回值也要查**：函数是否返回了输入对象本身（`result is data`），调用方改结果会不会影响输入；
- **顺序不限的结果**：规格没规定顺序时，两边都 `sorted` 再比，不依赖行序；
- **同类**：存下旧快照，之后与新状态做深比较，才看得出「查询之后状态是否变了」。

```python
import copy

def allocate(items: list) -> list:
    items.sort()                     # 缺陷：原地排序，还返回同一个对象
    return items

def input_unchanged(fn) -> bool:
    data = [3, 1, 2]
    before = copy.deepcopy(data)     # 副本，不是 before = data
    fn(data)
    return data == before

print(input_unchanged(allocate))                    # False：抓到了
print(input_unchanged(lambda xs: sorted(xs)))       # True
```

**知识点：**pytest 的常用工具（pytest Toolkit）
