---
id: hl-c16-practice-kit-commands
node: cpp-lessons.c16-coderpad-survival
type: qa
step: 21
---
## Q
在 kit 根目录里，怎么开始一道 C++ 题、跑某个标签的测试、对参考实现跑测试、让 stdin→stdout 的题跑起来？

## A
```bash
python3 tools/cpptest.py start loop/rounds/01_video/hc03_recursive_sum              # starter.hpp → work.hpp
python3 tools/cpptest.py run   loop/rounds/01_video/hc03_recursive_sum --tag part1   # 默认 --impl work
python3 tools/cpptest.py run   loop/rounds/01_video/hc03_recursive_sum --impl reference --exclude-tag perf -q
python3 tools/cpptest.py main  loop/rounds/00_oa/oa01_job_chain --impl reference < input.txt
```
- `start`：把起点复制成你的工作副本；`run`：跑测试，默认测你的 `work`，`--impl reference` 测参考实现；`main`：只对 stdin→stdout 的题，用输入文件喂给程序。
