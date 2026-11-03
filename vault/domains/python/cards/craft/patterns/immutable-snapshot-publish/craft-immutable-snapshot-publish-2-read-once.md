---
id: craft-immutable-snapshot-publish-2-read-once
node: craft.patterns.immutable-snapshot-publish
type: qa
step: 2
---
## Q
**不可变快照整体替换 · 为什么读者要「只读一次引用」**｜模式

快照已经是不可变的了，报价函数里先写 `len(self.sched.starts)`，后面再写 `self.sched.versions[-1]`，看起来每次读到的都是完整快照，有什么问题？

## A
**要点。** 每次 `self.sched` 都是一次独立的读取，两次读取之间可能发生了一次发布，你拿到的两个字段来自不同的版本。不可变保证的是「手里这一份不会变」，不保证「再去拿一次还是同一份」。读路径的关键纪律是：先把引用读到局部变量，之后只用这个局部变量。

```python
def quote_reading_twice(e, hook):
    n = len(e.sched.starts)              # 第一次读引用
    hook()                               # 此刻发生了一次发布
    return n, e.sched.versions[-1]       # 第二次读引用：另一个版本

def quote_reading_once(e, hook):
    s = e.sched                          # 只读一次
    hook()
    return len(s.starts), s.versions[-1] # 两个字段来自同一个快照
```

读到一半发布一次：

```
quote_reading_twice  -> (1, 'B') （版本数 n 应与最后版本配对：n=1 对应 A，n=2 对应 B）
quote_reading_once   -> (1, 'A') （版本数 n 应与最后版本配对：n=1 对应 A，n=2 对应 B）
```

**为什么。** 依赖的是 CPython 里单次属性赋值不会被撕成两半，所以读到的要么是旧引用要么是新引用；它不会让你的两次读取保持一致，一致性来自你只读一次。

**易错。** 这类 bug 不会报错，只是偶尔把新旧混着用（版本数是旧的，规则是新的），测试里几乎撞不上。
