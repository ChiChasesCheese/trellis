---
id: collision-probing-rejects-cache-locality
node: model.dict-set-internals
type: qa
source: cpython-internals
---
## Q
CPython 开发者曾经实验过让哈希冲突探测（probe）优先访问相邻内存以利用 CPU 缓存局部性（cache locality），结果为什么没有被采纳？

## A
实验发现，为了利用缓存局部性而让探测序列按规律访问相邻槽位，这种规律性反而会系统性地制造更多哈希冲突，抵消甚至超过缓存命中带来的收益；这个问题在小字典（整张表本就已经装在一两条缓存行里，没有额外未命中可省）和热点访问不均匀的大字典（高频键和它们的冲突链本来就常驻缓存）中都成立。因此 CPython 保留了原有的伪随机扰动探测（perturbation probing），没有改成基于相邻内存局部性的探测方式。
