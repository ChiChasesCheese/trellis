---
id: hi-pt-figma-draw-api-4-op-command
node: qb.lld.figma-draw-api.points
type: qa
step: 4
---
## Q
**矢量图形编辑器绘图 API · 统一为 Op 与命令模式**｜出自：矢量图形编辑器绘图 API › 核心实体与接口

矢量编辑器的撤销、同步、持久化、协作要怎么共用一条管道？Document.apply 的返回值有什么用？

## A
**要点。** 所有功能都是对节点属性的赋值：Op(node_id, prop, value)，创建删除是特殊操作。
**关键方法。** 
```python
def apply(self, op):
    old = node.get(op.prop); node[op.prop] = op.value
    return Op(op.node_id, op.prop, old)  # 逆操作
```
**用途。** 返回旧值构成的逆操作，供撤销回放（命令模式）。
