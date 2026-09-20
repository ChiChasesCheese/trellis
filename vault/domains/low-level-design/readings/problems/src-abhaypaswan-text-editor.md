---
nodes: [problems.components.text-editor]
url: https://github.com/abhaypaswan/lld-python/tree/main/problems/text-editor
---
# lld-python — text-editor

值得读：自由来源里唯一原生 Python、带 pytest 套件的实现，三处判断和本题解一致，值得先看：
**新编辑必须清空重做栈**（它把"留着重做会把编辑重放到已经变了的文本上"讲得很具体）、
**连打合并的边界**（换行、长度上限、光标移动），以及**"相邻不等于意图"**——两次刻意的程序化插入
不该被折成一步。它的正文是一个 Python `str`（作者自己在追问里承认大文件要换 rope 或 piece
table），命令层是 `InsertCommand`/`DeleteCommand`/`ReplaceCommand`/`CompositeCommand` 四个类
加一个抽象基类。本题解把数据结构的选择正面做成了第 1 关（选 gap buffer 并给出代价表），
并把四个命令类坍缩成一个 `Edit` splice 数据类——因为插入、删除、替换本来就是同一种操作的三个特例。
