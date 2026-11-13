---
id: tr-test-infra-sharding-xdist
node: test-infra.sharding
type: qa
step: 2
---
## Q
用 `pytest-xdist` 在一台机器上并行跑测试，`-n auto` 和几种 `--dist` 模式分别是什么意思？并行之后最常见的新问题是什么，怎么解决？

## A
**基本用法**：
- `-n auto`：每个物理 CPU 核起一个工作进程（worker，名字是 `gw0`、`gw1`…）；`-n 8` 指定个数；`-n logical` 按逻辑核数。
- `--dist load`（默认）：哪个工作进程空了就给它下一条测试。
- `--dist loadscope`：同一模块（或同一个类）的测试交给同一个进程，让模块级的昂贵 fixture 只建一次。
- `--dist loadfile`：同一文件的测试在同一进程。
- `--dist loadgroup`：带相同 `@pytest.mark.xdist_group("名字")` 的测试在同一进程，用来把必须串行的测试绑在一起。
- `--dist worksteal`：先平均分，空闲进程从别的进程的队列里"偷"任务，适合耗时差异很大的套件。

**并行后的新问题：测试间共享资源冲突**。串行时没事的测试，并行时撞在一起：
- **同一个端口**：两个进程都起服务监听 8000 端口。→ 用端口 0 让系统分配，或按 `worker_id` 计算端口。
- **同一个文件或目录**：都写 `/tmp/out.json`。→ 用 `tmp_path` fixture，每条测试一个独立临时目录。
- **同一个数据库或设备**：→ 每个进程一个独立的库名（例如 `test_db_gw3`），或用 `xdist_group` 把它们串行。
- **session 级 fixture 被执行 N 次**：每个工作进程各执行一次。要全局只做一次（例如下载一个大文件），用 `tmp_path_factory.getbasetemp().parent` 下的文件加文件锁协调。

```python
@pytest.fixture(scope="session")
def port(worker_id):          # 串行时 worker_id 是 "master"
    n = 0 if worker_id == "master" else int(worker_id[2:])
    return 9000 + n
```

**先验证再并行**：并行前装 `pytest-randomly` 打乱顺序多跑几次，确认测试之间没有顺序依赖。
