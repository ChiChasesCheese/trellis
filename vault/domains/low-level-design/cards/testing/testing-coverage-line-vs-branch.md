---
id: testing-coverage-line-vs-branch
node: testing.coverage-limits
type: qa
step: 1
---
## Q
行覆盖率（line coverage）和分支覆盖率（branch coverage）有什么区别？为什么一个测试就能让下面的函数达到 100% 行覆盖，却明显漏测了？Python 里怎么测分支覆盖率？

```python
def clamp_tokens(n, limit=4096):
    if n > limit:
        n = limit
    return n
```

## A
**行覆盖只问「每行执行过没有」；分支覆盖还问「每个判断的真、假两个方向都走过没有」。没有 `else` 的 `if` 是行覆盖最典型的盲区。**

- **这个例子：** 只有一个测试 `clamp_tokens(5000) == 4096`。它进入了 `if`，四行全部执行，行覆盖 100%。但 `n <= limit`（不进 `if`、直接返回）这条路从没走过。
- **实测：** 用 `pytest --cov=clamp --cov-report=term-missing` 显示 `100%`；加上 `--cov-branch` 后变成 `83%`，Missing 一栏写着 `2->4`，意思是「从第 2 行直接跳到第 4 行」这条路没走过。
- **怎么开启：**

```bash
pytest --cov=mypkg --cov-branch --cov-report=term-missing
# 或者不用 pytest-cov：
coverage run --branch -m pytest && coverage report -m
```

- **报告怎么读：** `Missing` 列里的单个数字是没执行的行，`a->b` 是没走过的分支跳转，`BrPart` 是只走了一半的判断数。
- **团队约定：** 默认就打开分支覆盖；给新代码设门槛时只看本次改动的行（`diff-cover` 之类的工具），比要求全仓库达到某个百分比更公平、更难被凑数。
- **分支覆盖仍然不够：** 它不检查组合条件里每个子条件是否单独被验证，更不检查断言写得对不对。
