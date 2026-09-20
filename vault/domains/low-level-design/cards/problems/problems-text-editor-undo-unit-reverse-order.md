---
id: problems-text-editor-undo-unit-reverse-order
node: problems.components.text-editor
type: cloze
step: 8
tags: [grown]
---
文本编辑器里"替换全部匹配项"必须是{{c1::一个撤销单元}}，做法是把这一批编辑放进一个 `tuple[Edit, ...]` 整体压栈。执行时要{{c2::从右往左}}替换，这样每一处的起点都还是按原文算出来的，不必为长度差逐个修正下标；撤销这个单元时要{{c3::逆序}}逐条求逆，因为{{c4::后执行的编辑改变了先执行的编辑所依赖的下标}}。加上这个功能不需要改动 `Edit` 和历史栈一行代码——这正是{{c5::设计可扩展}}的证据。
