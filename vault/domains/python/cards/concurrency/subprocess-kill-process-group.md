---
id: subprocess-kill-process-group
node: concurrency.multiprocessing
type: qa
---
## Q
写一个函数：运行一个可能派生子进程的命令，超时后先礼貌地请整个进程树退出，宽限几秒还不退就强杀，并且不留下僵尸进程或孤儿进程。

## A
**让子进程开一个新会话（也就是新的进程组），超时后对整个组先发 `SIGTERM`，宽限期过了再发 `SIGKILL`，最后用 `communicate()` 收尸。**

```python
def run_tree(cmd, timeout, grace=5):
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                         text=True, start_new_session=True)  # 自成进程组
    try:
        out, err = p.communicate(timeout=timeout)
    except subprocess.TimeoutExpired:
        os.killpg(p.pid, signal.SIGTERM)       # 整个组，不只是 p
        try:
            out, err = p.communicate(timeout=grace)
        except subprocess.TimeoutExpired:
            os.killpg(p.pid, signal.SIGKILL)
            out, err = p.communicate()         # 回收 p，不留僵尸
        raise TimeoutError(f"{cmd} > {timeout}s, rc={p.returncode}")
    return p.returncode, out, err
```

- **进程组（process group）：** 一组可以被一个信号同时送达的进程。`start_new_session=True` 让子进程调用 `setsid()`，成为新会话和新进程组的组长，组 ID 等于它的 PID，它之后派生的进程默认都在这个组里。Python 3.11 起也可以用 `process_group=0` 只建新组。
- **实测：** 对 `sh -c "sleep 32 & sleep 32"` 设 1 秒超时，1.01 秒后抛出，`rc=-15`（被 SIGTERM 结束），`pgrep` 找不到任何残留的 `sleep 32`。
- **先 TERM 后 KILL：** `SIGTERM` 可以被程序捕获，用来刷盘、释放设备、删临时文件；`SIGKILL` 无法捕获，进程立刻消失，什么都来不及做。给 5–30 秒宽限期是常见做法。
- **为什么用 `communicate` 而不是 `wait`：** 它一边读 stdout/stderr 一边等待，避免输出塞满管道导致双方互等；它返回时子进程已被回收，不会变成僵尸。
- **局限：** 如果孙进程自己又调用了 `setsid()` 脱离了这个组（守护进程常这么做），`killpg` 管不到它。容器里可以用 cgroup 整组杀掉；Linux 上也可以用 `prctl(PR_SET_PDEATHSIG)` 让子进程在父进程死后收到信号。
