---
id: fluency-collections-dict-order
node: fluency.collections
type: qa
step: 1
---
## Q
购物车要按“商品第一次加入的顺序”列出行，数量可以改。用 `dict[sku, qty]` 存，没有另外维护顺序的列表。给已有商品改数量、删掉再加回来、数量减到 0，行序各怎么变？

## A
**dict 的插入序就是行序**

- **保证**：`dict` 按键第一次插入的顺序迭代（3.7 起是语言规定，不是实现细节）；
- **改已有的键不动位置**：`lines["shirt"] = 5` 值变了，位置还在原处；
- **删了再放落到末尾**：先 `del` 再赋值，键被当成新键排在最后；需求写“改量位置不动”，就别用“先删后加”的实现；
- **数量减到 0 要删键**：`0` 不入库，“库里有这行”与“数量为正”才是同一件事；
- **不要一边遍历一边增删**：遍历 `dict` 时改变大小抛 `RuntimeError`；要改就遍历 `list(d)` 的快照；
- **何时才需要另外的结构**：要按“最近使用”重排才用 `OrderedDict.move_to_end`；只要插入序，普通 `dict` 足够。

```python
lines = {"shirt": 2, "hat": 1}
lines["shirt"] = 5                  # 改量：位置不动
print(list(lines))                  # ['shirt', 'hat']
del lines["shirt"]; lines["shirt"] = 5
print(list(lines))                  # ['hat', 'shirt']：落到末尾

def set_qty(lines: dict[str, int], sku: str, qty: int) -> None:
    if qty == 0:
        lines.pop(sku, None)        # 减到 0：删键，没有这个键也不报错
    else:
        lines[sku] = qty
```

**知识点：**容器的选择与惯用法（Collections Idioms）
