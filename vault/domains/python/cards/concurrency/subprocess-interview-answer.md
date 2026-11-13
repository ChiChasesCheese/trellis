---
id: subprocess-interview-answer
node: concurrency.multiprocessing
type: qa
---
## Q
面试里被问「你的测试框架要启动被测服务和命令行工具，怎么保证它们不卡住、不残留、失败时信息完整？」，怎么答？

## A
按下面的顺序说：

1. **启动方式：** 参数用列表，不用 `shell=True`；`start_new_session=True` 让被测进程自成进程组，之后能一次性清理它派生的所有进程。
2. **读输出：** 用 `communicate()` 或 `run(capture_output=True)` 边读边等，避免管道写满死锁；长期运行的服务把输出重定向到文件，失败时附到报告中。
3. **超时分层：** 单个命令有 `timeout`，单个测试有 `pytest --timeout`，整个任务有 CI 上限。超时先 `os.killpg(..., SIGTERM)`，宽限几秒后 `SIGKILL`，最后回收，不留僵尸也不留孤儿。
4. **判读退出码：** 正数是程序自己报告的失败；负数（shell 里 128 + N）是被信号杀死：`-9` 先查 OOM，`-11`/`-6` 是原生代码崩溃，去拿 core dump。
5. **清理放在 fixture 里：** 服务进程用 `yield` fixture 启停，测试失败也一定执行清理；用 `worker_id` 或随机端口避免并行测试互相占用。
6. **兜底检查：** 每个测试或每个任务结束后检查有没有残留进程和被占用的设备，有就让构建失败，而不是让下一个测试莫名其妙地失败。
