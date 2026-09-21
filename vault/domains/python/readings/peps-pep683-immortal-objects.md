---
nodes:
- memory.interning-immortal
title: PEP 683：用固定引用计数实现不朽对象（Immortal Objects）
corpus: peps
section: 03-pep-0683
url: https://peps.python.org/pep-0683/
tags:
- canonical
---

# PEP 683：用固定引用计数实现不朽对象（Immortal Objects）

解释 3.12 起 None、True、False、小整数、驻留字符串为什么会“免疫”引用计数——把 refcount 置为一个特殊哨兵值，Py_INCREF/DECREF 对其直接变成空操作。动机部分给出两条面试常问的理由：一是多核下每次 incref/decref 都会使 CPU 缓存行失效，高频访问的全局单例（如 None）在多线程下会互相“抢”缓存；二是为了给 per-interpreter GIL 铺路——若对象仍可变，跨解释器共享内建单例就会有数据竞争，只能给每个解释器复制一份，而不朽对象让“真正不可变”成立，从而免去复制。Rationale 部分列出了被否决的替代方案（用高位标记但不改 INCREF、加显式 flag、按类型跟踪、独立表跟踪），它们都没能解决缓存失效的性能问题。也提到唯一的行为破坏：读到的 refcount 会是一个异常大的常量，依赖具体数值的代码会出错。
