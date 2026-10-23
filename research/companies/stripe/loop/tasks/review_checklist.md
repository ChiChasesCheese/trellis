# Review 清单（每题逐条打勾；F = 必须修，S = 建议）

## problem.md
- F 规则无歧义：每个 Part 的输入/输出/排序 tie-break/错误格式都定死；worked examples 与 solution 实际输出一致（跑一遍）
- F Part 递进真实：后一 part 建立在前一 part 上，不是换题
- S 题面像面试官会给的（Context 先讲业务，再讲格式）；Sources 有 URL+日期；"面试官会怎么追问" ≥ 5 条

## solution.py（最佳实践）
- F 公共 API 与 starter_template 签名一致；`main(stdin, stdout)` 只做 I/O 与分发
- F 钱用整数分或 Decimal；无 float 累加；舍入规则有注释
- F 输出顺序确定：排序 key 完整（含 tie-break）
- F 解析健壮：strip、空行、尾换行；坏输入按题面定义处理，不吞异常
- F 无全局可变状态；无死代码；无未用 import/变量（flake8 F* = 0）
- S 函数 ≤ 40 行；一个函数一件事；规则用常量/表而不是散落的 if；命名说人话；类型标注；docstring 一句话说清"做什么"
- S 复杂度符合 perf 预算且不过度工程（先直接后优化）；后 part 复用前 part 的函数
- S 面试可读性：一个陌生人 60 秒内能从 main 追到每个 part 的核心循环

## test_*.py
- F 每 part ≥ 3；markers 正确（每测恰一个 partN + 可选 edge/fmt/io/perf）；worked examples 逐字进测试
- F 非空洞：`IMPL=starter` 必须失败；断言的是精确值/精确字符串而不是 `len>0`
- F 无 flaky：线程测试有 join/超时；perf 用 `random.Random(0)`；不依赖真实时间/网络（int 题用本地 mockserver 随机端口）
- S 测试名说明意图；边界测试对应 problem.md 的 Edge cases 列表；io 测试用 `run_script` 断言 exact stdout

## 其他
- F `starter.py` 与 `starter_template.py` 内容一致；starter 的 `main()` 可运行（只是 partN 未实现）
- F `loop/lint.sh <dir>` 通过（black 110 + flake8 F 类 0）
- F REPORT.md 含 CONVENTIONS 规定的节 + "电面话术/边写边说"
- S bs 题：`mock.py start/ref` 跑通；patch ≤ 15 行；失败用例只命中注入的 bug
- S int 题：fixture 起/停 mockserver 干净；网络错误路径有测试
