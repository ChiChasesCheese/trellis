---
nodes:
- types.basics
title: PEP 526：变量注解语法
corpus: peps
section: 15-pep-0526
url: https://peps.python.org/pep-0526/
tags:
- canonical
---

# PEP 526：变量注解语法

在函数注解（PEP 484）之后，把注解扩展到变量、类变量和实例变量：primes: List[int] = [] 这种写法取代了此前只能用注释表达的 # type: List[int]。Rationale 列出了类型注释（type comment）的六个实际痛点：编辑器不会高亮注释里的类型信息、无法在不赋初值的情况下标注未定义变量、条件分支里的类型注释难以对齐阅读、注释不是语言的一部分导致想解析它就得自己写解析器而不能复用 ast、普通注释和类型注释混在一起难以区分、运行时也拿不到这些信息。文档同时强调这不是要把 Python 变成静态类型语言，变量注解依旧不做运行时类型检查，只是提供更规整的元数据载体，也为后续 dataclass 读取字段类型铺了路。
