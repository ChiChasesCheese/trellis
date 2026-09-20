---
nodes: [problems.components.text-editor]
url: https://github.com/prsnt558908/CodeZymSolutions/tree/main/1-100/q09_text_editor_lld
tags: [no-archive]
---
# CodeZymSolutions — q09 text editor（Python 教程 + 实现）

值得读：同一道题的另一种切法——完全不做撤销，改做"**字符 + 样式**"的文档模型：按行存
（`TextRow` 持有一串字符对象），用享元（Flyweight）加工厂把"同一个字符 + 同一套样式"的组合
共享成一个对象，避免一页文字造出成千上万个重复对象。拿来想"如果需求变成带格式的文档，设计会往
哪个方向长"很合适。它对大文档的插入删除没有任何优化（行内是一个列表），也没有光标、选区和历史；
本题解正文保持纯文本、把样式列进"扩展与追问"，并把重点放在缓冲区选型和撤销单元上。
它镜像的是 codezym.com 上的付费题库，因此只链接、不摘录。
