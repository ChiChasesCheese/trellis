"""退货风险评分引擎（ReturnGuard）参考解：三个分项相加、按分数段做决定、批量逐项隔离。

设计五句话：
1. 评分规则是数据，不是 if 链：每个分项一张"下界（含）→ 分数"的分段表（`Tiers`），查表用二分，边界只有一种写法。
2. 整套规则装进不可变的 `Policy`（带版本号）；`RiskEngine` 只持有它，不持有任何会变的状态，所以天然无状态、线程安全。
3. 校验在任何计算之前：类型必须恰好是 `int`（`bool` 是 `int` 的子类，要单独挡住），再看范围；不合格抛 `ServiceError(400, "invalid_input")`。
4. 引擎内部用不可变的 `Assessment` 记录一次判定（含输入与策略版本），对外才变成合同规定的字典，每次新建，调用之间不共享任何对象。
5. `evaluate_many` 只在"处理一条记录"这一步 try；遍历输入迭代器本身不在 try 里，迭代器的异常原样抛出，输入只被遍历一次。
"""

from __future__ import annotations

from bisect import bisect_right
from collections.abc import Iterable
from dataclasses import dataclass
from typing import Generic, TypeGuard, TypeVar

T = TypeVar("T")
INVALID_INPUT = "invalid_input"
RECORD_KEYS = frozenset({"rating", "value_cents", "account_age_days"})


class ServiceError(Exception):
    """对外的服务错误：status 是 HTTP 状态码，code 是稳定的错误码字符串。"""

    def __init__(self, status: int, code: str) -> None:
        self.status, self.code = status, code
        super().__init__(code)


@dataclass(frozen=True)
class Tiers(Generic[T]):
    """分段表：`bounds` 是严格升序的下界（含），x 落在 [bounds[i], bounds[i+1]) 就取 `values[i]`。

    不变量：第一段从 0 开始（所以任何非负整数都有归属），最后一段没有上界，相邻两段之间没有缝也不重叠。
    """

    bounds: tuple[int, ...]
    values: tuple[T, ...]

    def __post_init__(self) -> None:
        increasing = all(a < b for a, b in zip(self.bounds, self.bounds[1:]))
        if not (self.bounds[:1] == (0,) and increasing and len(self.bounds) == len(self.values)):
            raise ValueError("分段表必须从 0 起、下界严格升序、每段一个值")

    @classmethod
    def of(cls, *steps: tuple[int, T]) -> Tiers[T]:
        """按 (下界, 值) 逐段书写，读起来和策略文档一一对应。"""
        return cls(tuple(bound for bound, _ in steps), tuple(value for _, value in steps))

    def index(self, x: int) -> int:
        """x 所在的段号。恰好等于下界的 x 属于这一段（左闭右开），这是全表唯一的边界规则。"""
        if x < self.bounds[0]:
            raise ValueError(f"{x} 小于第一段的下界")
        return bisect_right(self.bounds, x) - 1

    def at(self, x: int) -> T:
        return self.values[self.index(x)]


@dataclass(frozen=True)
class Policy:
    """一版完整的评分策略，创建后不可变；改规则就发新版本，不原地改。"""

    version: str
    rating_points: tuple[int, ...]  # 下标 0 对应评分 1
    value: Tiers[int]  # 下界单位：分
    age: Tiers[int]  # 下界单位：天
    decision: Tiers[str]  # 下界单位：总分

    @property
    def max_rating(self) -> int:
        return len(self.rating_points)


POLICY_V1 = Policy(
    version="v1",
    rating_points=(40, 30, 20, 10, 0),
    value=Tiers.of((0, 0), (10_000, 15), (50_000, 30)),
    age=Tiers.of((0, 25), (30, 10), (180, 0)),
    decision=Tiers.of((0, "approve"), (30, "manual_review"), (60, "reject")),
)


@dataclass(frozen=True)
class Assessment:
    """一次判定的完整记录：输入、策略版本、三个分项和决定。事后解释一个决定，靠的就是这些字段。"""

    policy_version: str
    rating: int
    value_cents: int
    account_age_days: int
    rating_points: int
    value_points: int
    age_points: int
    decision: str

    @property
    def score(self) -> int:
        return self.rating_points + self.value_points + self.age_points

    def as_dict(self) -> dict[str, object]:
        """合同规定的返回形状。每次调用都新建字典和嵌套字典，调用方改它不会影响任何别的结果。"""
        return {
            "score": self.score,
            "decision": self.decision,
            "components": {
                "rating": self.rating_points,
                "value": self.value_points,
                "age": self.age_points,
            },
        }

    def explain(self) -> str:
        """一行可读的解释：哪版策略、什么输入、各得几分、总分与决定。"""
        return (
            f"{self.policy_version}: rating={self.rating}→{self.rating_points}, "
            f"value={self.value_cents}→{self.value_points}, age={self.account_age_days}→{self.age_points}; "
            f"score={self.score} → {self.decision}"
        )


def _is_int(x: object) -> TypeGuard[int]:
    """恰好是 int：`bool` 是 `int` 的子类，`isinstance(True, int)` 为真，所以要比较类型本身。"""
    return type(x) is int


class RiskEngine:
    """无状态的评分引擎：同样的输入永远得到同样的输出，实例之间、调用之间互不影响。"""

    def __init__(self, policy: Policy = POLICY_V1) -> None:
        self._policy = policy

    def assess(self, rating: object, value_cents: object, account_age_days: object) -> Assessment:
        """校验、查表、定级，返回不可变的判定记录。"""
        policy = self._policy
        # `and` 短路：类型不对就不会去做大小比较，否则 "a" >= 0 会抛 TypeError 而不是 ServiceError
        if not (
            _is_int(rating)
            and 1 <= rating <= policy.max_rating
            and _is_int(value_cents)
            and value_cents >= 0
            and _is_int(account_age_days)
            and account_age_days >= 0
        ):
            raise ServiceError(400, INVALID_INPUT)
        rating_points = policy.rating_points[rating - 1]
        value_points = policy.value.at(value_cents)
        age_points = policy.age.at(account_age_days)
        return Assessment(
            policy_version=policy.version,
            rating=rating,
            value_cents=value_cents,
            account_age_days=account_age_days,
            rating_points=rating_points,
            value_points=value_points,
            age_points=age_points,
            decision=policy.decision.at(rating_points + value_points + age_points),
        )

    def evaluate(self, rating: object, value_cents: object, account_age_days: object) -> dict[str, object]:
        return self.assess(rating, value_cents, account_age_days).as_dict()

    def evaluate_many(self, records: Iterable[object]) -> list[dict[str, object]]:
        """逐条处理，每条一个 `{result, error}`；坏记录只影响它自己。"""
        outcomes: list[dict[str, object]] = []
        for record in records:  # 取下一条在 try 之外：迭代器自己的异常不属于"坏记录"，原样抛出
            try:
                outcomes.append({"result": self._evaluate_record(record), "error": None})
            except ServiceError as error:
                outcomes.append({"result": None, "error": error.code})
        return outcomes

    def _evaluate_record(self, record: object) -> dict[str, object]:
        # 必须是字典，且键恰好是三个：缺键、多键都算无效，不能悄悄忽略多余的键
        if not isinstance(record, dict) or record.keys() != RECORD_KEYS:
            raise ServiceError(400, INVALID_INPUT)
        return self.evaluate(record["rating"], record["value_cents"], record["account_age_days"])


if __name__ == "__main__":
    engine = RiskEngine()
    print(engine.evaluate(1, 50000, 10))
    print(engine.evaluate(5, 500, 365))
    print(engine.assess(3, 10_000, 0).explain())
    for outcome in engine.evaluate_many([{"rating": 3, "value_cents": 10_000, "account_age_days": 0}, {"rating": 0}]):
        print(outcome)
