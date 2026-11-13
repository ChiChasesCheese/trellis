---
id: subprocess-run-timeout-check
node: concurrency.multiprocessing
type: qa
---
## Q
测试框架要调用一个外部命令行工具（比如被测的二进制），拿到它的输出和退出码，并且不能让它卡住整个测试。`subprocess.run` 应该怎么写？`timeout` 到期时它到底杀了谁？

## A
**传参数列表、捕获输出、设超时、检查退出码；但 `run` 超时只杀它直接启动的那个子进程，子进程再派生的进程（孙进程）会活下来。**

```python
r = subprocess.run(
    ["./engine", "--model", path, "--max-tokens", "16"],
    capture_output=True, text=True,   # stdout/stderr 收成 str
    timeout=60,                       # 超时抛 subprocess.TimeoutExpired
    check=True,                       # 退出码非 0 抛 CalledProcessError
)
print(r.returncode, r.stdout[:200])
```

- **用列表，不用 `shell=True`：** 列表里每个元素就是一个参数，路径里有空格或特殊字符也不会被 shell 重新解释，也没有命令注入的风险。只有真的需要管道、通配符时才用 shell。
- **`check=True`：** 退出码非 0 时抛 `CalledProcessError`，异常对象带着 `returncode`、`stdout`、`stderr`，打印出来就能看到失败原因。不加它，失败的命令会被当成成功。
- **超时时发生什么：** `run` 对子进程发 `SIGKILL`，等它退出，再抛 `TimeoutExpired`。但只杀这一个 PID。实测：`run(["sh", "-c", "sleep 31 & sleep 31"], timeout=1)` 在 1.01 秒抛出超时，`sh` 被杀了，两个 `sleep 31` 都还活着。
- **孙进程为什么危险：** 它们成为孤儿进程继续占用 CPU、端口、GPU 内存或测试硬件，下一个测试就会撞上「端口已被占用」或「设备忙」，看起来像一个新的偶发失败。
- **怎么彻底清理：** 让子进程自成一个进程组（process group），超时时对整个组发信号：`Popen(..., start_new_session=True)` 再 `os.killpg(p.pid, signal.SIGTERM)`。
