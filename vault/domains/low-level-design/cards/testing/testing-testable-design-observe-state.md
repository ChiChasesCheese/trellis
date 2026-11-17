---
id: testing-testable-design-observe-state
node: testing.testable-design
type: qa
step: 6
---
## Q
删除用户时应当同时删掉他的收藏记录。公开的查询方法对已删除的用户总是返回空，所以哪怕删除代码漏掉了收藏行，通过接口的测试也发现不了。测试怎么看到这个泄漏？

## A
**把存储注入进来，测试直接数它的行**

- **接口看不到的状态**：孤儿行被查询方法按用户存在与否过滤掉了，从外面看一切正常；
- **注入存储**：构造函数接一个存储（这里是一个列表），测试自己持有它，删除之后断言它为空；
- **不要去碰私有属性**：`service._entries` 一改名测试就坏；注入进来的对象是测试和实现之间的正式接缝；
- **接缝要小**：只暴露「数据在哪」，不暴露内部算法；
- **对比**：如果这类检查经常需要，说明应当有一个公开的诊断方法（如 `count_rows()`），让运维也能看。

```python
class Lists:
    def __init__(self, entries: list):
        self.entries, self.users = entries, set()      # 存储由调用方持有
    def add(self, user: str, movie: str):
        self.users.add(user); self.entries.append((user, movie))
    def delete_user(self, user: str):
        self.users.discard(user)
        self.entries[:] = [e for e in self.entries if e[0] != user]
    def movies(self, user: str):
        return [m for u, m in self.entries if u == user and u in self.users]

rows: list = []
s = Lists(rows); s.add("ann", "m1"); s.delete_user("ann")
print(s.movies("ann"), rows)        # [] []：只有数 rows 才知道有没有孤儿
```

**知识点：**可测的设计（Design for Testability）
