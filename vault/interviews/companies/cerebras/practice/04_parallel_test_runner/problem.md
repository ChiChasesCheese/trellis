# 04 · 有界并行的测试执行器：超时、只对暂时性错误重试、汇总

限时 30 分钟，Python。

发布前要跑几百个测试命令，一个一个跑太慢，全部同时跑会把机器压垮，所以要"最多同时跑 N 个"。有的命令会卡死，要按时杀掉，而且要连它启动的子进程一起杀；有的失败是暂时的（设备忙、锁被占），值得再试一次，但真正的失败绝不能靠重试"刷"过去。这组练习让你用 `concurrent.futures` 和 `subprocess` 写这样一个执行器，最后打印带耗时的汇总。没有 AI 概念，考的是进程、并发和失败语义。

## 输入

一组 `(名字, shell 命令)`。命令行形式读一个文本文件，每行 `名字: 命令`，空行和 `#` 开头的行忽略（`make_commands.py` 会生成一个示例 `commands.txt`，里面有通过、真失败、暂时失败、卡死、大量输出各一种）。

## 任务

### Part 1：跑一个命令，带超时（约 10 分钟）

`run_once(cmd, timeout, tail=2000) -> Attempt(returncode, timed_out, seconds, output)`

- 用 shell 执行（`shell=True`），标准输出和标准错误合在一起收集，只保留最后 `tail` 个字符。
- 进程放进**新的会话**（`start_new_session=True`），它和它启动的所有子进程在同一个进程组里。
- 超时：先给整个进程组发 `SIGTERM`，等一小会儿，再发 `SIGKILL`；`returncode = None`，`timed_out = True`。
- 输出很多（几 MB）也不能卡住：用 `communicate()`，不要先 `wait()` 再读。

### Part 2：重试策略（约 7 分钟）

`run_with_retries(name, cmd, timeout, retries, transient) -> Result(name, cmd, status, returncode, attempts)`

- 退出码在 `transient`（暂时性错误码，比如 75 = "暂时失败，请重试"）里时才重试，最多再试 `retries` 次。
- 退出码 0、不在 `transient` 里的失败、超时：都不重试。
- `status` 是 `pass` / `fail` / `timeout`，看最后一次尝试；`seconds` 是所有尝试耗时之和。

### Part 3：有界并行（约 8 分钟）

`run_all(commands, jobs, timeout, retries=0, transient=frozenset()) -> [Result]`

- 同一时刻最多 `jobs` 个命令在跑。用 `ThreadPoolExecutor`：每个线程只是在等子进程，不占 CPU，GIL 不是瓶颈。
- 结果按**输入顺序**返回，不按完成顺序。
- 一个命令卡住不影响其他命令。
- `jobs < 1`、`timeout <= 0`、名字重复：`ValueError`。空列表返回空列表。

### Part 4：汇总（约 5 分钟）

`summarize(results, wall=None) -> str`：每个命令一行（状态、名字、退出码、尝试次数、耗时），再一行总计"N commands: a passed, b failed, c timed out, d retried; sum of durations …s, wall …s"，再列最慢的 3 个。`parse_commands(text)`、`main(argv)`：全部通过返回 0，否则返回 1。

## 例子

```text
$ python make_commands.py
$ python solution.py commands.txt --jobs 3 --timeout 2 --retries 2 --transient 75
PASS     fast_pass            rc=   0 attempts=1   0.27s
PASS     slow_pass            rc=   0 attempts=1   0.97s
FAIL     real_fail            rc=   1 attempts=1   0.01s
PASS     flaky_device         rc=   0 attempts=3   0.04s
TIMEOUT  hang                 rc=   - attempts=1   2.01s
PASS     noisy                rc=   0 attempts=1   0.05s
6 commands: 4 passed, 1 failed, 1 timed out, 1 retried; sum of durations 3.36s, wall 2.07s
slowest: hang 2.01s, slow_pass 0.97s, fast_pass 0.27s
```

总耗时 3.36 秒，墙钟只有 2.07 秒，因为最多 3 个同时跑。

## 边界情况

- 命令不存在：shell 返回 127，算失败，不是异常。
- 命令启动了孙进程后卡住：超时后孙进程也必须死（测试会读孙进程的 pid 去检查）。
- 输出 1 MB 以上。
- 暂时失败的次数比 `retries` 多：最后一次的退出码就是结果。
- 没有配置任何暂时性错误码：什么都不重试。

## 面试官会追问

| 追问 | 答题要点 |
|---|---|
| 为什么只杀 shell 不够？ | `shell=True` 时你拿到的是 shell 的 pid，真正干活的是它的子进程。只杀 shell，子进程变成孤儿继续跑，还握着输出管道，`communicate()` 会一直等。新会话 + `os.killpg` 一次杀整个组 |
| 进程自己又 `setsid` 跑出了进程组怎么办？ | 进程组管不住它。用 Linux 的 cgroup（容器里的资源组）把整个测试放进去，超时就杀整个 cgroup；或者每个测试跑在一次性容器里 |
| 为什么先 SIGTERM 再 SIGKILL？ | SIGTERM 让进程有机会清理临时文件、释放设备；不理会再 SIGKILL 强杀 |
| 重试为什么会掩盖缺陷？ | 一个真的竞态 bug 有 30% 概率失败，重试两次后 97% 能"通过"，bug 被藏起来。所以只对明确的暂时性错误码重试，并且把"重试后才通过"记下来，当作不稳定测试的信号上报 |
| 超时为什么不重试？ | 超时已经花掉了全部时间预算；卡死多半是真问题（死锁、等不到的资源），重试只会让整轮再慢一倍 |
| 为什么用线程，不用进程池？ | 线程只是阻塞在等子进程上，GIL 不影响；进程池多一层进程和序列化，没有好处。如果要在 Python 里做重计算，才换进程池 |
| 结果顺序为什么要确定？ | 两次运行同一份清单应该打印同样的报告，才能逐行比较；按完成顺序打印会因为调度不同而变 |
| 并发数怎么定？ | 看瓶颈资源：CPU 密集的测试取核数；独占设备的测试（每台测试机一块加速卡）按设备数；再用一次实测找吞吐不再上升的点 |
| 想要 asyncio 版本？ | `asyncio.create_subprocess_shell` + `asyncio.Semaphore(jobs)` 限流 + `asyncio.wait_for` 做超时；杀进程组的逻辑不变 |
| 怎么测这个执行器本身？ | 用极小的 Python 命令当测试：sleep 固定时间并把开始、结束时间写到文件，算最大重叠数验证并发上限；用计数文件模拟"前两次失败"；让命令启动孙进程并写出 pid，验证超时后孙进程不在了 |

## 评分看什么

- 超时后进程组被清理干净，没有孤儿进程，也没有因为大量输出而卡死。
- 重试条件写得窄：只对配置的暂时性错误码，超时和真失败都不重试，并能说出为什么。
- 并发上限真的生效，结果顺序确定。
- 汇总里有足够的信息定位问题：哪个慢、哪个重试过、哪个超时。
- 自己能说出这些行为各用什么测试来验证。

## 怎么跑

```bash
cd vault/interviews/companies/cerebras
uv run --project ../../../.. pytest practice/04_parallel_test_runner -q            # 约 8 秒
IMPL=starter uv run --project ../../../.. pytest practice/04_parallel_test_runner -q
cd practice/04_parallel_test_runner && uv run --project ../../../../../.. python make_commands.py \
  && uv run --project ../../../../../.. python solution.py commands.txt --jobs 3 --timeout 2 --retries 2 --transient 75
```
