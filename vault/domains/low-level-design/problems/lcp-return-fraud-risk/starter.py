"""ReturnGuard 退货风险评分服务（待修复）。公开 API 与 `solution.py` 一致，可以原样放进真实工作区的 `service.py`。

这份代码能跑，但有几处和下面的规则不符：它就是要你修的东西。

规则（每一条都有测试）：
 1. `evaluate(rating, value_cents, account_age_days)` 的三个入参必须是整数：评分 1..5，金额（分）不小于 0，
    账龄（天）不小于 0。布尔、浮点、字符串、`None`、越界的值，都抛 `ServiceError(400, "invalid_input")`，
    而且要在算分之前抛；除评分外，整数没有上界。
 2. 评分分：1→40，2→30，3→20，4→10，5→0。
 3. 金额分：0..9999 分得 0；10000..49999 得 15；50000 及以上得 30。每一段的下界都算这一段。
 4. 账龄分：0..29 天得 25；30..179 得 10；180 及以上得 0。下界同样算这一段。
 5. 总分就是三项相加，不归一、不取整、不截断。低于 30 是 "approve"；30 到 59 是 "manual_review"；
    60 及以上是 "reject"。
 6. 返回值恰好是 `{"score": int, "decision": str, "components": {"rating": int, "value": int, "age": int}}`。
 7. `evaluate_many(records)` 只遍历一次输入（有限的可迭代对象），按输入顺序给每条记录一个结果。
    记录必须是字典，键恰好是 `rating`、`value_cents`、`account_age_days`。
    合法记录得 `{"result": evaluate(...), "error": None}`，非法记录得 `{"result": None, "error": "invalid_input"}`；
    坏记录不拖累后面的记录；空输入得 `[]`；输入迭代器自己抛的异常照常往外抛，不能吞。
 8. 引擎没有状态：调用之间、返回的嵌套字典之间互不影响，也不改输入；不依赖时钟、网络、汇率或学习模型。

Python 3.11，只用标准库。
"""

from __future__ import annotations


class ServiceError(Exception):
    """对外的服务错误：status 是 HTTP 状态码，code 是稳定的错误码字符串。"""

    def __init__(self, status: int, code: str) -> None:
        self.status, self.code = status, code
        super().__init__(code)


REQUIRED_FIELDS = ("rating", "value_cents", "account_age_days")


def _bad_input():
    return ServiceError(400, "invalid_input")


class RiskEngine:
    def evaluate(self, rating, value_cents, account_age_days):
        # 类型检查已经做对：比较类型本身，bool、float、str、None 都挡在外面
        for field in (rating, value_cents, account_age_days):
            if type(field) is not int:
                raise _bad_input()
        # 缺陷：评分下界写成 0
        if rating < 0 or rating > 5 or value_cents < 0 or account_age_days < 0:
            raise _bad_input()

        # 缺陷：评分表直接用公式算，1 分只得 20
        by_rating = (5 - rating) * 5

        by_value = 0
        if value_cents > 50000:  # 缺陷：这一行漏了"下界含"，恰好 50000 落进下一段
            by_value = 30
        elif value_cents >= 10000:
            by_value = 15

        by_age = 0
        if account_age_days < 30:
            by_age = 25
        elif account_age_days < 180:
            by_age = 10

        total = by_rating + by_value + by_age
        # 缺陷：60 分被当成 manual_review（30 的边界是对的）
        verdict = "approve"
        if total > 60:
            verdict = "reject"
        elif total >= 30:
            verdict = "manual_review"
        return {
            "score": total,
            "decision": verdict,
            "components": {"rating": by_rating, "value": by_value, "age": by_age},
        }

    def evaluate_many(self, records):
        out = []
        for item in records:
            try:
                if not isinstance(item, dict) or tuple(sorted(item)) != tuple(sorted(REQUIRED_FIELDS)):
                    raise _bad_input()
                out.append({"result": self.evaluate(**item), "error": None})
            except ServiceError:
                # 缺陷：错误码丢了，应该是 "invalid_input"
                out.append({"result": None, "error": None})
        return out
