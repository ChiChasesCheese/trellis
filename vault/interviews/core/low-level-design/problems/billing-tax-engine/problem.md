# 计费 / 计税引擎（Billing & Tax Engine）

支付平台按商户收手续费，再在手续费之上收税。每个商户的费用规则（例如"2.9% 加 0.30"）会改，新规则从某个时间点起生效；
历史交易必须按它发生那一刻生效的规则计算，之后重算也要得到一模一样的数字。
照机考的节奏分关来做，做完一关再看下一关。

**分关要求**

- 第 1 关（约 20 分钟）：`publish` 为商户发布一个带生效时间的规则版本，`quote` 按交易时间找到当时生效的版本，
  依次运行规则链，返回每一行（规则 ID、种类、版本、金额）。两条规则：`PercentPlusFixed`（费率加固定费）和
  `TaxOnFees`（税建在前面各费用行之上）。金额是整数最小货币单位，每一行只取整一次，用银行家舍入。
- 第 2 关（约 15 分钟）：阶梯费率 `Tiered`（累进，每档只对落在这一档里的部分收费），封顶与保底 `Bounded`
  （包住任意一条规则）。不用改引擎。
- 第 3 关（约 20 分钟）：规则之间可以有依赖（`needs`），发布时按依赖排好顺序，写错（环、依赖不存在、ID 重复）当场拒绝；
  固定费可以按币种配置，缺币种要报错；发布和报价可以并发，读到的一定是完整的某一版。
- 第 4 关（选做）：发现某个版本配错了费率。`reprice` 用更正后的规则重算一笔旧交易，只返回有差额的调整行，旧各行不动。

**接口**

```python
@dataclass(frozen=True, slots=True) class Txn: id: str; merchant: str; amount: int; currency: str; ts: int
@dataclass(frozen=True, slots=True) class Line: rule_id: str; kind: str; version: int; amount: int   # kind: "fee" | "tax" | "adjustment"

class BillingError(Exception)              # 以下全是它的子类
class NoActiveRules(LookupError)           # 交易发生时没有生效的版本（含未知商户）
class StaleVersion(ValueError)             # 生效时间不晚于该商户上一个版本
class InvalidRuleSet(ValueError)           # ID 重复 / 依赖不存在 / 依赖成环 / 阶梯定义不合法
class MissingCurrency(LookupError)         # 固定费没有为这个币种配置

# 规则：任何有 rule_id、kind、needs 和 apply(txn, prior) -> Decimal | None 的对象（结构化类型，不必继承）
PercentPlusFixed(rule_id: str, bps: int, fixed: int | Mapping[str, int] = 0, kind: str = "fee", needs: tuple[str, ...] = ())
TaxOnFees(rule_id: str, bps: int, kind: str = "tax", needs: tuple[str, ...] = ())
Tiered(rule_id: str, tiers: tuple[tuple[int | None, int], ...], fixed: int | Mapping[str, int] = 0, kind="fee", needs=())
Bounded(rule_id: str, inner: Rule, minimum: int = 0, maximum: int | None = None)

class FeeEngine:
    def publish(self, merchant: str, effective_from: int, rules: Sequence[Rule]) -> int   # 返回版本号，从 1 起
    def quote(self, txn: Txn) -> tuple[Line, ...]
    def reprice(self, txn: Txn, previous: Sequence[Line], rules: Sequence[Rule], version: int) -> tuple[Line, ...]
```

规则细节：

- `bps` 是万分之一：`290` 是 2.9%。`PercentPlusFixed` 在 `amount <= 0` 时不适用（不产生这一行）；`TaxOnFees` 只汇总前面 `kind == "fee"` 的已取整各行，没有费用行就不适用。
- 生效版本 = 最后一个 `effective_from <= txn.ts` 的版本：恰好等于生效时间属于新版本。没有这样的版本抛 `NoActiveRules`，不能返回 0 费用。
- `publish` 的生效时间必须严格晚于该商户上一个版本（`StaleVersion`）；任何失败的发布都不占用版本号。
- `Tiered` 的 `tiers` 是 `((档上限, bps), ...)`，最后一档的上限必须是 `None`，前面的上限严格递增，否则 `InvalidRuleSet`。各档金额先累加再取整一次。
- `Bounded` 对不适用（`None`）的规则保持不适用；`kind` 和 `needs` 沿用被包住的规则。
- `needs` 列出必须排在前面的规则 ID；没有约束的规则保持书写顺序。`quote` 返回的行就是执行顺序。
- `reprice`：调整行的 `kind` 是 `"adjustment"`，金额 = 新 - 旧（按 `rule_id` 汇总），差额为 0 的不返回，按 `rule_id` 排序；更正的规则集同样要通过 `InvalidRuleSet` 校验。

例子：

```python
e = FeeEngine()
e.publish("m1", 100, (PercentPlusFixed("fee", 290, 30), TaxOnFees("tax", 1000)))
e.publish("m1", 200, (PercentPlusFixed("fee", 250, 30), TaxOnFees("tax", 1000)))
e.quote(Txn("t1", "m1", 10000, "USD", ts=150))   # fee 320（版本 1）、tax 32
e.quote(Txn("t2", "m1", 500, "USD", ts=150))     # fee 44.5 -> 44（取偶数）、tax 4.4 -> 4
e.quote(Txn("t3", "m1", 10000, "USD", ts=200))   # 版本 2：fee 280、tax 28
e.quote(Txn("t4", "m1", 10000, "USD", ts=99))    # 抛 NoActiveRules
```

**评分点**

- 按生效时间二分，而不是"当前配置"；能说清退款、重算为什么必须用交易发生时的版本，并固定"恰好等于生效时间"这条约定。
- 规则是对象，统一接口；加阶梯、封顶、保底、新的税只新增对象，引擎不动；税建在费用之上不是特殊逻辑，只是链上靠后的一条规则。
- 取整只在边界发生一次，全系统一处实现；能解释银行家舍入与四舍五入的区别，以及多档先累加后取整的原因。
- 发布时就校验（环、缺依赖、重复 ID），失败不留痕迹；运行期不会遇到半个版本。
- 读路径不加锁：发布造出新的不可变快照再换引用；能说出为什么不是"边读边改列表"。
- 报价是纯函数：不读当前时间，不依赖隐藏状态，重算结果逐位相同；没有版本时宁可报错。
- 纠错只追加调整行，不改旧行；与账本的冲正是同一个原则。
- 能口述：规则依赖图、多实例发布一致性（生效时间设在未来几分钟）、币种小数位（日元 0 位、科威特第纳尔 3 位）、固定费分摊时的守恒。
