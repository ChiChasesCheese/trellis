---
id: craft-copy-in-copy-out-2-shallow-or-deep
node: craft.idioms.copy-in-copy-out
type: qa
step: 2
---
## Q
**边界拷贝 · dict(row) 什么时候够用，什么时候必须 deepcopy**｜写法

行 dict 里的值有的是数字和字符串，有的是嵌套 dict 或 list。边界上只写 `dict(row)` 就够了吗？deepcopy 要多花多少，怎么判断该用哪个？

## A
**要点。** `dict(row)` 是浅拷贝（shallow copy）：新建外层 dict，但值还是同一批对象。值全是不可变的（数字、字符串、元组、冻结对象）时，共享它们没有任何危险，浅拷贝就够了。只要有一个值是可变的（list、dict、集合），改它就会透过拷贝影响到原件，这时才需要深拷贝（deep copy）。

```python
import copy, timeit

row = {"id": 1, "addr": {"city": "NYC"}, "tags": ["a"]}
shallow = dict(row)
shallow["addr"]["city"] = "LA"                       # 嵌套对象仍是共享的
print(row["addr"]["city"])
flat = {"id": 1, "name": "x", "score": 3.5}          # 值全是不可变的
f2 = dict(flat); f2["score"] = 0
print(flat["score"])                                 # 一层 dict() 就够了

big = {f"c{i}": [i] * 5 for i in range(20)}
t_shallow = timeit.timeit(lambda: dict(big), number=20000)
t_deep = timeit.timeit(lambda: copy.deepcopy(big), number=20000)
print(f"dict(): {t_shallow:.3f}s  deepcopy: {t_deep:.3f}s")
```

实际输出（耗时随机器而变，量级才是要点）：

```
LA
3.5
dict(): 0.001s  deepcopy: 0.134s
```

**为什么。** 第一行：浅拷贝之后改嵌套的 `city`，原件也变了。第二行：值全是不可变数时，改拷贝的键不影响原件。第三行是同一个 20 列的行拷两万次，深拷贝慢两个数量级，因为它要遍历每个嵌套对象并维护一张已拷贝对象的表。

**信号。** 能把行的值限制成不可变类型（`tuple` 代替 `list`、冻结数据类代替 dict），就能把深拷贝降为浅拷贝甚至不拷。不能限制，深拷贝就是正确的价格。
