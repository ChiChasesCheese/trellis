---
id: test-pytest-select-k-m-nodeid
node: engineering.testing
type: qa
---
## Q
一个有 5,000 个测试的套件，你只想跑「名字里含 decode、但不含 slow 的测试」，或者「打了 gpu 标记但没打 nightly 标记的测试」，或者只重跑上次失败的那几个。pytest 分别怎么选？

## A
**按名字用 `-k`，按标记用 `-m`，按精确位置用节点 ID（node id），按上次结果用 `--lf` / `--ff`。**

```bash
pytest -k "decode and not slow"            # 名字表达式，不区分大小写的子串匹配
pytest -m "gpu and not nightly"            # 标记表达式
pytest "tests/test_api.py::TestStream::test_stop[eos]"   # 精确到一个参数组合
pytest --lf                                # 只跑上次失败的
pytest --ff -x                             # 先跑上次失败的，遇到第一个失败就停
pytest --co -q -m smoke                    # 只收集不运行，看会选中哪些
```

- **`-k`：** 对测试名、类名、模块名（以及标记名等关键字）做子串匹配，支持 `and`、`or`、`not` 和括号。它依赖命名习惯，改名就可能选漏。
- **`-m`：** 对标记做布尔表达式。标记是你主动给测试分的类，比名字可靠，适合定义套件分层：`smoke`、`nightly`、`gpu`。
- **节点 ID：** `文件::类::函数[参数ID]`，失败报告中会原样打印，复制过来就能单独重跑那一个。
- **`--lf` / `--ff`：** 依赖 `.pytest_cache` 里上次的结果。CI 的全新环境里没有这个缓存，所以它是本地调试工具。
- **先确认再跑：** `--co`（`--collect-only`）只列出会被选中的测试，不执行，用来检查表达式写对没有；输出末尾会显示多少个被取消选择（deselected）。
- **配合使用：** `-x` 第一个失败就停，`--maxfail=3` 失败三个就停，适合在大套件里快速拿到第一个线索。
