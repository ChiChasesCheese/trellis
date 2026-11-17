---
id: data-defensive-copy-shallow
node: data.defensive-copy
type: qa
step: 2
---
## Q
构造函数里写了 `self._ratings = dict(ratings)`，其中 `ratings` 是 `{用户: {电影: 分数}}`。调用方之后改了某个用户的内层字典，服务里的数据为什么也变了？该复制到哪一层？

## A
**这些拷贝只复制最外一层，内层共享**

- **浅拷贝（shallow copy）**：新建外层容器，里面装的还是同一批对象的引用；内层可变对象依然共享；
- **要复制到哪一层**：复制到“不可变的值”为止；`{用户: {电影: 分数}}` 要两层都复制；
- **`copy.deepcopy`** 能递归复制，但慢，而且会复制不该复制的东西（锁、连接、回调）；形状已知时手写逐层复制更准；
- **更好的办法**：存的时候就转成不可变的结构（`frozenset`、元组、冻结的 dataclass），之后根本不需要复制；
- **测试**：构造之后改输入的内层，断言服务的结果没变；只测外层会漏掉这个洞。

```python
ratings = {"ann": {"m1": 5}}
shallow = dict(ratings)
deep = {u: dict(r) for u, r in ratings.items()}    # 形状已知：逐层复制

ratings["ann"]["m1"] = 1                           # 改内层
print(shallow["ann"]["m1"], deep["ann"]["m1"])     # 1 5
print(shallow["ann"] is ratings["ann"])            # True：内层是同一个对象
```

**知识点：**防御性拷贝（Defensive Copying）
