---
nodes: [lcproject.lcp-apparel-shopping-cart, data.defensive-copy, oop.values, fluency.collections, fluency.time-numbers, ai.verification]
tags: [problem]
---
# Drill：服装购物车（Apparel Shopping Cart）

一家服装店的网页要显示目录和购物车，缺中间的购物车状态：加一件、把某个商品的数量改成指定值（改成 0 就是删除），以及返回目录与购物车的快照。目录至多 100 个商品，数量至多 1,000,000，一辆购物车至多 10,000 次修改。规模是一个文件、一百来行；难点不在算法，而在四个隐藏测试会去踩的细节：行序、数量边界、超过 32 位的精确合计、快照的独立。

**分关要求**（每关做完再看下一关，像真实的补全轮）
- 第 1 关（约 15 分钟）：写构造、`addLine`、`snapshot`。目录原序的 `products`、按插入序的 `items`、两个总数和 `empty`。先决定行放在什么容器里，再动手。
- 第 2 关（约 15 分钟）：写 `updateLine`：绝对数量、正数可以新建行、零删除、行不存在时什么都不做；"加 p1、加 p2、删 p1、再加 p1"的顺序写成测试，`items` 要是 `["p2", "p1"]`。
- 第 3 关（约 15 分钟）：精确合计。目录放满、每行都是上限，期望值由常量推出；单价为 0 的商品让购物车不空；所有数字的类型都是 `int`。
- 第 4 关（选做，约 15 分钟）：独立。构造后改调用方的对象、清空调用方的列表；改拿到的快照；两辆购物车共用同一批商品对象；再写两篇书面回答：删除再加回来怎样保持行序，以及你怎样检查输入、旧快照、不同购物车互不影响。

**怎么练**：把 `vault/domains/low-level-design/problems/lcp-apparel-shopping-cart/starter.py` 的方法体补全，然后在仓库根目录运行
`IMPL=starter uv run --no-project --python 3.11 --with pytest python -m pytest vault/domains/low-level-design/problems/lcp-apparel-shopping-cart -q`。

**和编程智能体一起练**：用编程智能体（Claude Code 或工作区自带的智能体）打开 `starter.py`。第一条指令给规则（十条）和两个调用示例，一次只让它实现一个方法，一次只给它一个失败的测试，改完立刻运行测试。容器的选择、零的处理、拷贝放在构造还是读取，这些决定自己留着；先让它指出模板里的别名（保存调用方列表的那一行），再让它另写一个"列表模型"的对照实现，在一万次随机操作上和你的解比较；期望值自己独立写出，不接受"把测试改成通过"。

**评分点**
- 写得出开工前的规则：行序三条、绝对值改量与零删除、两个有序视图、精确合计与 `empty`、独立（[[lcp-apparel-shopping-cart-contract-rules]]）。
- 说得清要存什么：冻结的目录和"ID 到数量"的字典，零从不入库，合计现算（[[lcp-apparel-shopping-cart-state-and-invariant]]）。
- 知道删除再加回来为什么落在末尾：字典的插入序，重新赋值不挪位置，`pop` 之后再赋值落在末尾，以及目录顺序、数量为 0 的记录两种错法（[[lcp-apparel-shopping-cart-reflection-line-order]]）。
- 能堵住三条泄漏通道并各配一个"改了再看"的测试：构造时拷贝、每次快照现建、状态放在实例上（[[lcp-apparel-shopping-cart-reflection-isolation-and-verification]]）。
- 写得出能抓住缺陷的测试：删除再加回的序列、上限两端、超 32 位的期望值由常量推出、单价为 0 的商品（[[lcp-apparel-shopping-cart-contract-rules]]、[[lcp-apparel-shopping-cart-state-and-invariant]]）。

**题解**：[[solution-lcp-apparel-shopping-cart]]——先做，再看。

**练习记录**
- [ ] 第 1 次（日期，用时，自评）：
