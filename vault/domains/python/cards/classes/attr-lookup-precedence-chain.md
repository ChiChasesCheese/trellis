---
id: attr-lookup-precedence-chain
node: classes.attribute-lookup
type: cloze
source: python-docs
---
对实例 `a` 做 `a.x` 时，`object.__getattribute__()` 按优先级依次尝试：{{c1::数据描述符（在类的 MRO 上找到，同时定义 `__get__` 和 `__set__`/`__delete__`）}} → {{c2::实例 `__dict__`，找不到才继续 → 非数据描述符（只定义 `__get__`）或普通类变量}} → {{c3::`__getattr__()`（前面全部找不到、且类定义了它时才调用）}}，任何一步找到就不再往下走。
