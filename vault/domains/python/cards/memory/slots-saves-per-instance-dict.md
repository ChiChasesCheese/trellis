---
id: slots-saves-per-instance-dict
node: memory.object-size
type: qa
source: cpython-internals
---
## Q
百万级实例的场景下，给类声明 `__slots__` 为什么能明显省内存？

## A
不声明 `__slots__` 时每个实例默认都带一个 `__dict__` 来存实例属性，dict 这种哈希表结构本身有不小的固定开销（预留空位、哈希表元数据）；声明 `__slots__` 后 CPython 为这些属性名分配固定偏移量的槽位，不再为每个实例创建 `__dict__`，改用更紧凑的定长结构存属性值，实例数量越多，省下的总内存越明显。
