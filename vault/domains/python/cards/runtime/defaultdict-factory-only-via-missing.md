---
id: defaultdict-factory-only-via-missing
node: runtime.stdlib-map
type: qa
source: python-docs
---
## Q
`defaultdict(list)` 用 `d[key]` 访问不存在的 key 会自动创建空列表；改用 `d.get(key)` 访问同一个不存在的 key，也会触发 `default_factory` 吗？

## A
不会。`default_factory` 是通过 `__missing__()` 这个钩子被调用的，只有直接用 `d[key]` 下标访问、且 key 不存在时才会走到 `__missing__()`；`dict` 原生的其它方法（比如 `.get()`）不调用 `__missing__()`，找不到 key 时仍按普通字典行为返回默认值，既不触发工厂函数，也不会往字典里插入新 key。
