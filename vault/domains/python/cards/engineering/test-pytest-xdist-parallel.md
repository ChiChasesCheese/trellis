---
id: test-pytest-xdist-parallel
node: engineering.testing
type: qa
---
## Q
一个 40 分钟的测试套件，用 `pytest-xdist` 并行跑。`-n auto` 做了什么？`--dist` 有哪些分配方式？为什么 session 作用域的 fixture 在并行后被执行了好几次，怎么办？

## A
**xdist 启动 N 个 worker 进程，把收集到的测试分给它们执行。每个 worker 是独立的 Python 进程，所以 session fixture 在每个 worker 里各建一次。**

```bash
pytest -n auto                       # worker 数 ≈ CPU 核数
pytest -n 8 --dist loadfile          # 同一文件的测试进同一个 worker
pytest -n 8 --dist loadgroup         # 同一 xdist_group 标记的测试进同一个 worker
```

- **分配方式：** `load`（默认，谁空闲给谁）、`loadscope`（同一模块或类的测试放一起，模块级 fixture 只建一次）、`loadfile`（按文件）、`loadgroup`（按 `@pytest.mark.xdist_group("db")`）、`worksteal`（先平均分，快的 worker 从慢的那里偷任务，适合耗时差别大的套件）。
- **session fixture 跑多次：** 4 个 worker 就是 4 次。实测：一个打印 `worker_id` 的 session fixture 在 `-n 4` 下记录了 gw0、gw1、gw2、gw3 各一次。如果它启动的是全局唯一的东西（建数据库、下载 5 GB 模型文件），要用文件锁让第一个 worker 做、其余的等待并复用结果。
- **`worker_id` fixture：** 值是 `gw0`、`gw1`……，不并行时是 `master`。用它给每个 worker 分不同的端口、临时库名、输出目录，避免互相踩。
- **前提是测试互相独立：** 并行会打乱顺序。依赖前一个测试留下的状态、共用一个固定端口或文件名的测试，在串行时通过，并行后随机失败。先装 `pytest-randomly` 打乱顺序串行跑几次，暴露这些依赖。
- **收益上限：** 总时间至少是最慢那个测试的时长，再加每个 worker 的启动和收集开销；几秒钟的套件并行反而更慢。
