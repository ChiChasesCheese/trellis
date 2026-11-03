---
id: craft-immutable-snapshot-publish-1-publish-whole
node: craft.patterns.immutable-snapshot-publish
type: qa
step: 1
---
## Q
**不可变快照整体替换 · 为什么读者看到半个更新**｜写法

税率引擎按商户保存「生效时间列表」和「对应的规则版本列表」两个平行列表，发布新版本时先给第一个列表追加，再给第二个追加。此刻一个报价请求进来，会读到什么？怎样让读路径一把锁都不用，又永远看不到半个更新？

## A
**要点。** 把两个字段放进同一个不可变对象（快照），发布时先在旁边造好完整的新快照，再用一次引用赋值换上去。读者拿到的要么是整个旧快照，要么是整个新快照，不存在中间状态。读路径不需要锁。

```python
@dataclass(frozen=True)
class Schedule:
    starts: tuple[int, ...] = ()
    versions: tuple[str, ...] = ()

def publish(self, start, version):          # 整体替换
    old = self.sched
    new = Schedule(old.starts + (start,), old.versions + (version,))
    self.sched = new                         # 一步换引用

def quote(self, ts):
    s = self.sched                           # 只读一次引用
    i = bisect.bisect_right(s.starts, ts)
    return s.versions[i - 1]
```

发布到一半时报价，平行列表与快照对比：

```
TwoLists  发布中途 quote(150) -> IndexError: list index out of range
TwoLists  发布完成 quote(150) -> v2
Snapshot  发布中途 quote(150) -> v1
Snapshot  发布完成 quote(150) -> v2
```

**为什么。** 两个字段要放进同一个对象：只有一次赋值才是原子的，两次赋值之间永远有缝。

**代价。** 每次发布都要拷贝整个结构，写是 O(n)（见第 3 张卡）。适合读多写少的配置、路由表。
