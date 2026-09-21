---
id: lessram-slots-mechanism
node: performance.less-ram
type: qa
source: python-docs
---
## Q
定义了 `__slots__ = ('x', 'y')` 的类，实例为什么比默认的类省内存？代价是什么？

## A
默认每个实例都带一个 `__dict__` 存属性，本身就要占一块哈希表的内存；声明 `__slots__` 后 Python 在类层面为每个名字生成描述符（descriptor），实例直接用固定槽位存值，不再创建 `__dict__`，省下这块哈希表开销。代价是实例不能再动态添加 `__slots__` 之外的属性（赋值会抛 `AttributeError`），也默认失去弱引用（weak reference）支持。
