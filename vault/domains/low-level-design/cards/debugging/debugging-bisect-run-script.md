---
id: debugging-bisect-run-script
node: debugging.bisect
type: qa
step: 2
---
## Q
手动二分十几轮既慢又容易答错。怎么用 `git bisect run` 全自动找出引入问题的提交？判断脚本的退出码有什么约定？写脚本时有哪些坑？

## A
**`git bisect run <脚本>`：git 在每个候选提交上运行脚本，用退出码代替你回答。0 表示好；1 到 127 之间（125 除外）表示坏；125 表示「这个提交没法测，跳过」；128 及以上让二分中止。**

```sh
#!/bin/sh
# 放在仓库外面，比如 /tmp/check.sh，免得被检出或清理掉
git clean -fdxq || exit 125                  # 清掉上一步留下的构建产物
make -j8 >/dev/null 2>&1 || exit 125         # 构建失败：跳过，不算坏
python3 -B -m pytest -q tests/test_limits.py::test_max_tokens || exit 1
```

```bash
git bisect start HEAD v2.3.0
git bisect run /tmp/check.sh
```

- **实测：** 在一个 100 个提交的仓库里，问题在第 63 个提交引入，`git bisect run` 运行脚本 7 次（log2(99) ≈ 6.6）就报告了第 63 个提交。
- **坑一：残留的构建产物。** 同一个实验里，最初的脚本每一步都判为好，最后找错了提交。原因是 Python 的 `.pyc` 缓存按源文件的修改时间和大小判断是否过期，`LIMIT = 4096` 改成 `LIMIT = 4095` 大小不变，检出又在同一秒内，旧的缓存被当成有效的。加上 `git clean -fdx` 和 `python3 -B` 后才找对。C/C++ 项目的增量构建同理。
- **坑二：构建失败当成坏。** 那样会把一个无关的编译错误认成罪魁，所以构建失败要 `exit 125`。
- **坑三：测试不稳定。** 在脚本里把测试重复跑几次（`pytest --count=5`，需要 `pytest-repeat`），任何一次失败才算坏。
- **坑四：测试本身也在变。** 新加的测试在旧提交上不存在。把判断用的测试文件复制到仓库外，每一步都用同一份去测。
- **性能回归：** 脚本里跑基准，耗时超过阈值就 `exit 1`；阈值要离两边的正常波动都有距离。
