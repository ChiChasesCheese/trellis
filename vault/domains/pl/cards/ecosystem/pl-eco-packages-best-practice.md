---
id: pl-eco-packages-best-practice
node: ecosystem.package-managers
type: qa
step: 10
---
## Q
资深工程师怎样管理依赖？通用规则是什么，Go、Java、Rust、Python 各自怎么做，何时破例？

## A
**通用规则**：
1. **应用提交锁文件，库只写宽松约束**。
2. **依赖越少越好**：每个依赖都是一份供应链风险与升级成本；标准库能做的不引依赖。
3. **升级是有节奏的例行工作**，不是出事才做；自动化工具开 PR，CI 跑完测试再合。
4. **安全扫描进 CI**：已知漏洞（CVE）检查、许可证检查。
5. **构建可复现**：固定工具链版本，固定依赖，内容哈希校验。

按语言：
- **Go**：`go.mod` 和 `go.sum` 都提交；`go mod tidy` 保持整洁；用 `go list -m -u all` 查可升级项，`govulncheck ./...` 查漏洞；大公司用 `GOPROXY` 搭内部代理。
- **Java**：Maven 用 `dependencyManagement` 或 BOM（物料清单，统一版本表）集中管理版本；pom 里写明确版本，不用范围；用 `mvn dependency:tree` 和 enforcer 的收敛规则抓冲突；Gradle 开 dependency locking。
- **Rust**：应用提交 `Cargo.lock`；用 `cargo audit`/`cargo deny` 检查漏洞和许可证；审慎打开 features，`cargo tree -d` 找重复版本；二进制发布前 `cargo build --locked`。
- **Python**：用 `uv` 或 `poetry` 生成锁文件，`uv sync --frozen` 在 CI 里安装；不要往全局 Python `pip install`，每个项目一个虚拟环境；`pip-audit` 检查漏洞；库的约束写成下限加主版本上限，不要写死 `==`。

**何时破例**：库的开发者要在 CI 里同时测试依赖的最低版本和最新版本，来检验约束写得对不对（Go 的 MVS 天然测最低版，其他语言需要刻意做）。
