---
id: pl-sig-gotchas-best-practice
node: signatures.gotchas
type: qa
step: 8
---
## Q
怎样系统地防御语言的经典陷阱？资深工程师在 Go、Java、Rust、Python 里各启用哪些工具和约定？

## A
**通用方法**：陷阱不要靠记忆防御，要靠**自动化**：
1. **把陷阱编码成检查**：linter 规则、编译器选项、CI 步骤。
2. **在代码评审的清单里写下本语言的前五个陷阱**。
3. **为每个事故补一条规则或测试**，不要只写事后总结。
4. **测试用边界输入**：空集合、nil、最大值、重复元素、并发。
5. **从陷阱学习设计**：看到陷阱，就问一句“它背后的设计选择是什么”，下次设计 API 时避免制造同类陷阱。

按语言的工具与约定：
- **Go**：`go vet ./...` 与 `staticcheck`（含 nil 接口、循环变量、printf 格式、复制锁）；`go test -race`；返回 `error` 的函数无错误时直接 `return nil`；用切片后需要独立副本时 `slices.Clone`；初始化 map 后再写。
- **Java**：Error Prone 与 SpotBugs（抓 `Integer ==`、忽略返回值、字符串比较）；IDE 检查；对象比较一律 `equals`；金额用 `BigDecimal`；用 `Math.addExact` 做关键计算；集合操作留意 `remove` 的重载。
- **Rust**：`cargo clippy -- -D warnings`；发布构建在关键服务开启 `overflow-checks`；`unwrap` 只用于不可能失败处；反向引用用 `Weak`；遇到借用冲突先改数据布局，再考虑 `RefCell`。
- **Python**：`ruff`（B006 可变默认参数、B023 循环里的闭包、E722 裸 except）；`mypy`/`pyright`；默认值用 `None`；遍历时不要修改被遍历的集合；浮点比较用 `math.isclose`，金额用 `Decimal`。

**团队层面**：
- 新人入职材料里放一份“本团队语言的十大陷阱”，每条带最小复现代码。
- 线上事故若来自语言陷阱，回头补上对应的 lint 规则。

**何时破例**：个别规则对特定代码库误报多，可以局部关闭，但要写明理由（`# noqa: B006  # reason`、`//nolint:xxx // reason`）。

**判断标准**：同一类陷阱在你的代码库里不会出现第二次，说明防线是有效的。
