---
id: tr-test-infra-hermetic-checklist
node: test-infra.hermetic
type: qa
step: 1
---
## Q
什么是隔离、可复现的测试（hermetic test）？要让"同一个提交在任何机器上结果都相同"，具体要控制哪些东西？

## A
**定义**：测试的结果只取决于被测代码和测试自己声明的输入，不取决于跑在哪台机器、什么时间、前面跑过什么。

要控制的东西，按"输入从哪里漏进来"列：

- **依赖版本**：库用锁文件钉死（`uv.lock`、`requirements.txt` 带 `--require-hashes`、`go.sum`），安装时用 `uv sync --locked` 这类"锁文件不一致就报错"的命令；容器镜像用摘要（`image@sha256:...`）而不是 `latest` 标签。
- **外部数据**：测试要用的模型文件、数据集按固定版本下载，或放进制品库按哈希引用。例如从 Hugging Face 加载模型时传 `revision=<提交哈希>`，否则上游更新了文件，测试结果就跟着变。（模型文件就是一大组训练好的数字参数。）
- **网络**：单元和大部分集成测试不访问外网；用 `docker run --network none` 或 `pytest-socket` 的 `--disable-socket` 强制。
- **文件系统**：只写测试自己的临时目录（pytest 的 `tmp_path`，Bazel 的 `$TEST_TMPDIR`），不写 home 目录和共享路径。
- **时间、时区、语言环境**：注入时钟而不是直接读当前时间；固定 `TZ=UTC`、`LC_ALL=C.UTF-8`。
- **随机性**：随机种子固定或记录下来；Python 的字符串哈希顺序受 `PYTHONHASHSEED` 影响，需要时固定。
- **测试之间的状态**：每条测试自己准备、自己清理，不依赖执行顺序；可以装 `pytest-randomly` 插件让每次运行随机打乱顺序来验证。
- **硬件与数值**：同样的计算在不同型号的芯片上可能最后几位不同，测试要么固定硬件型号，要么用容差比较。

一句话：**把所有输入都写进声明里，没声明的输入一律切断**。
