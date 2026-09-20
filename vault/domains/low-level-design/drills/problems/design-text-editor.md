---
nodes: [problems.components.text-editor, patterns.command, patterns.behavioral]
tags: [problem]
---
# Drill：文本编辑器与撤销重做（Text Editor）

一个单光标、纯文本的编辑器，要能打开一个几 MB 的源文件：插入、删除、移动光标、选区、剪切粘贴，
以及撤销和重做。分数不在"两个栈"上，而在两处——**正文用什么数据结构存**（决定它是玩具还是能用），
以及**一次撤销到底撤掉什么**（决定它像不像一个真编辑器）。照真实机考的节奏分关做，做完一关再看
下一关。

**分关要求**（每关做完再看下一关，像真实的机器编码轮）
- 第 1 关（约 15 分钟）：插入、删除、光标移动、取任意区间。动手之前先在纸上写下**四个候选数据
  结构各自的每次操作代价**（一个 `str`、按行的 `list[str]`、gap buffer、piece table），选一个并写
  出理由。选完还要回答一个问题：删掉九成文本之后，你的结构会不会把内存还回去？把这条不变量做成
  一个可以断言的只读属性。
- 第 2 关（约 15 分钟）：撤销与重做。一次修改要携带足够把自己倒回去的全部信息——包括光标。
  新的编辑必须清空重做栈；撤销栈要有上限，超限丢**最旧**的。验收方式是跑一串**随机**的编辑与
  撤销，和一个"每步存一份全文"的朴素模型逐步对照（固定随机种子）。
- 第 3 关（约 10 分钟）：连续击键并成一个撤销单元，并在换行、长度上限、光标移动三处断开；
  有选区时输入即替换；剪切、复制、粘贴。想清楚"合并与否"的判据该由谁给出——相邻并不等于意图。
- 第 4 关（选做）：`find` / `find_all` / `replace_all`，其中"替换全部"必须是**一个**撤销单元。
  判分点只有一个：做完这一关，编辑记录类型和文档类是不是一行都没改——撤销栈那边最多只该多出
  一个「把一批编辑记成一个单元」的入口，而不是为查找替换新发明一种命令。

**怎么练**：把 `vault/domains/low-level-design/problems/text-editor/starter.py` 的方法体补全，
然后在仓库根目录运行
`IMPL=starter uv run --with pytest python -m pytest vault/domains/low-level-design/problems/text-editor -q`。

**评分点**
- 先给出四个数据结构的代价对比再选，而不是直接开写；说得出为什么"编辑是局部的"让 gap buffer 划算（[[problems-text-editor-buffer-choice]]）。
- 大量删除之后缓冲区把内存还回去，并把这条不变量暴露成可断言的属性（[[problems-text-editor-gap-shrink]]）。
- 把插入／删除／替换看成同一种 splice，用一个冻结 dataclass 代替四个命令子类，逆操作是字段对调（[[problems-text-editor-one-edit-record]]、[[patterns-command-callable-vs-class]]）。
- 主机制用增量而不是快照，但光标这种又小又难反推的状态随编辑一起快照（[[problems-text-editor-command-vs-memento]]、[[patterns-memento-vs-command-undo]]）。
- 新编辑第一件事就是清空重做栈；再加一道"要删的文本和现状对不上就抛错"的保险（[[problems-text-editor-redo-cleared-on-new-edit]]）。
- 合并连打由调用方的意图决定，程序化插入即使相邻也绝不合并（[[problems-text-editor-coalescing-intent]]）。
- 一批编辑作为一个撤销单元：执行从右往左，撤销逆序求逆（[[problems-text-editor-undo-unit-reverse-order]]）。
- 撤销栈不认识文档，只进出编辑记录，因此可以被单独测试（[[problems-text-editor-history-knows-no-document]]、[[patterns-command-cost]]）。
- 用长随机序列对照朴素模型来验收撤销，固定种子保证可复现（[[problems-text-editor-random-model-test]]）。
- 移动光标清掉选区；撤销恢复光标但不恢复剪贴板（[[problems-text-editor-cursor-clears-selection]]）。

**题解**：[[solution-text-editor]]——先做，再看。

**练习记录**
- [ ] 第 1 次（日期，用时，自评）：
