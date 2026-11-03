---
id: craft-read-only-views-and-snapshots-2-view-vs-snapshot
node: craft.idioms.read-only-views-and-snapshots
type: qa
step: 2
---
## Q
**只读视图与快照 · `MappingProxyType(self._counts)` 为什么不如 `MappingProxyType(dict(self._counts))`**｜写法

币箱要把各面额的数量交给外部查看。把内部字典包一层 `MappingProxyType` 之后调用方确实不能改了，币箱的实现却还多写了一层 `dict(...)`。这一层拷贝防的是什么？

## A
**要点。** `MappingProxyType` 是**视图**（view）：只读，但它背后仍然是同一个字典，底层变，视图跟着变。`dict(...)` 先拷贝再包装才是**快照**。视图防止「通过它写入」，快照还额外防止「被它读到不一致」：外部在遍历时，内部若同时变化，视图遍历会直接抛 `RuntimeError`，或者读到改了一半的内容。

```python
class CoinBank:
    def __init__(self) -> None:
        self._counts = {"5c": 2}

    def view(self):                            # 视图：包装内部字典本身
        return MappingProxyType(self._counts)

    def snapshot(self):                        # 快照：先拷贝，再包装成只读
        return MappingProxyType(dict(self._counts))

b = CoinBank()
v, s = b.view(), b.snapshot()
b._counts["5c"] = 99                           # 内部之后变了
print("视图跟着变:", dict(v), "| 快照不变:", dict(s))

# 视图被遍历的同时底层变化：遍历方会崩
try:
    for coin in b.view():
        b._counts["10c"] = 1                   # 例如另一个线程在同时找零
except RuntimeError as e:
    print("遍历视图时底层改了:", e)

for coin in b.snapshot():                      # 遍历快照：底层怎么变都不影响
    b._counts["25c"] = 1
print("遍历快照完成")
```

实际输出：

```
视图跟着变: {'5c': 99} | 快照不变: {'5c': 2}
遍历视图时底层改了: dictionary changed size during iteration
遍历快照完成
```

**为什么。** 判据是内部状态之后会不会变，以及有没有别的线程在改：构造后永不再变的（模块常量、冻结对象里的字段）给视图就够，省掉拷贝；运行期还会变的、尤其受锁保护的，必须给快照，并且在锁内拷贝。

**易错。** 视图并不是「线程安全的只读」：它没有锁，也没有拷贝。想靠它跨线程共享一个正在变化的字典，会在遍历处随机崩溃。
