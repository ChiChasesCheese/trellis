---
id: problems-text-editor-history-knows-no-document
node: problems.components.text-editor
type: qa
step: 9
tags: [grown]
---
## Q
文本编辑器的撤销栈（History）应该直接去改文档，还是只负责进出编辑记录、由别人去应用？

## A
只负责进出记录：`undo()` 弹出一个撤销单元，返回**应当按序执行的逆编辑**，由门面（Editor）交给文档去应用。这样 History 完全不认识 Document，可以被单独构造、单独断言（"两条首尾相接的键入并成了一个单元""弹出来的逆编辑是倒序的"），也能原样用在别的可撤销系统上（绘图、表格）。

反过来，撤销逻辑一旦和文档纠缠——比如 History 持有文档并直接调用它的方法——就再也没法单独测试了，而撤销恰恰是这类系统里最需要密集测试的部分。
