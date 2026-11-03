---
id: craft-make-unmake-undo-log-3-closure-log-and-nesting
node: craft.patterns.make-unmake-undo-log
type: qa
step: 3
---
## Q
**做/撤销与撤销日志 · 嵌套事务：每次写入记一个「变回去」的闭包**｜模式

内存键值库要支持嵌套事务：`begin` 可以套 `begin`，`rollback` 撤销最内层，`commit` 保留最内层的改动，但外层回滚仍能把它们一起撤销。怎么让几十种写操作（set、delete、改过期时间）都可撤销，又不为每种写写一套撤销代码？

## A
**要点。** 所有写操作最后都走同一个底层函数 `_apply(key, value)`（`None` 表示删除）。写之前取出旧值 `prior`，把一个「调用 `_apply(key, prior)`」的闭包追加到当前事务层的日志里。正向写入和撤销是**同一个操作**，只是目标状态不同。`rollback` 逆序执行日志；`commit` 把本层日志并进外层，数据已经生效，但外层仍然可以撤销它；不在任何事务里时不记日志（没人会 rollback）。

```python
class KV:
    def __init__(self):
        self.d = {}
        self.frames = []                                     # 每层事务一份撤销日志

    def _apply(self, k, v):                                  # 正向写入与撤销共用这一个函数
        if v is None: self.d.pop(k, None)
        else: self.d[k] = v

    def _write(self, k, v):
        prior = self.d.get(k)                                # 记下"变回去的目标状态"
        if self.frames:                                      # 不在事务里就不记：没人会 rollback
            self.frames[-1].append(lambda: self._apply(k, prior))
        self._apply(k, v)

    def set(self, k, v): self._write(k, v)
    def delete(self, k): self._write(k, None)
    def begin(self): self.frames.append([])
    def commit(self):
        done = self.frames.pop()
        if self.frames: self.frames[-1].extend(done)         # 并进外层：外层回滚仍能撤销它们
    def rollback(self):
        for undo in reversed(self.frames.pop()): undo()      # 逆序重放

s = KV(); s.set("name", "Ada")
s.begin(); s.set("name", "Bo"); s.set("age", "30")
s.begin(); s.delete("name"); s.set("age", "31")
s.rollback()                                                 # 只撤销内层
print("内层回滚后:", s.d)
s.commit()                                                   # 外层提交
print("外层提交后:", s.d)
s.begin(); s.set("x", "1"); s.begin(); s.set("y", "2"); s.commit(); s.rollback()
print("内层提交、外层回滚:", s.d, "<- x、y 都被撤销")
```

```
内层回滚后: {'age': '30', 'name': 'Bo'}
外层提交后: {'age': '30', 'name': 'Bo'}
内层提交、外层回滚: {'age': '30', 'name': 'Bo'} <- x、y 都被撤销
```

**为什么。** 必须**逆序**撤销：同一个键先后被写了两次，只有从最后一次往前撤，才能一步步回到最初的值。按顺序重放会得到第一次写之后的值，而不是写入前的值。把撤销写成「恢复到旧值」而不是「做反向运算」，也让它对重复的、相互覆盖的写都成立。

**易错。** 闭包里的 `prior` 要在定义时绑定（`lambda prior=prior: ...`，循环里尤其重要），否则所有闭包共享同一个变量，撤销时全部变成最后一个值。惰性过期（读到过期数据时顺手删掉）也走 `_write`，所以同样可撤销；撤销回去的是同一份 `(value, expires_at)`，过没过期仍由调用时的 `now` 重新判断，因此撤销一次惰性清理不会让过期数据复活。
