---
id: sparser-hashtable-hurts-iteration
node: model.dict-set-internals
type: qa
source: cpython-internals
---
## Q
把 dict 底层哈希表做得更稀疏（装载因子更低）能减少哈希冲突，但为什么会拖慢 `keys()`/`items()`/`__iter__()` 这类遍历操作？

## A
更稀疏的哈希表意味着同样数量的键分散在更大的底层数组里，而遍历类方法必须扫描每一个潜在槽位（entry）才能找出哪些被实际占用；把底层表大小翻倍，`keys()`、`items()`、`values()`、`__iter__()`、`update()` 这些方法要访问的、彼此不连续的内存位置数量也随之翻倍，缓存命中率也更低。所以放大哈希表在「减少冲突」和「拖慢遍历」之间是此消彼长的权衡（trade-off）。
