---
id: hl-loop-practice-commands
node: company.loop
type: qa
step: 15
---
## Q
用 Java 练一道电话面编码题的命令流程是什么？`start` 和 `run` 各做什么，`--impl reference` 是什么？

## A
```
python3 tools/jtest.py start loop/rounds/01_video/hc03_recursive_sum
python3 tools/jtest.py run   loop/rounds/01_video/hc03_recursive_sum --tag part1
```
- `start`：把空壳复制成你的工作副本（Java 是 `work/`，C++ 版是 `cpp/work.hpp`，工具换成 `cpptest.py`）。
- `run`：跑测试，`--tag part1` 只跑某一部分；加 `--impl reference` 改跑参考解。

Java 共 15 题，其中 12 题另有 C++ 版。
