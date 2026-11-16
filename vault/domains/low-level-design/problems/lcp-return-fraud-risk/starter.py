"""ReturnGuard 退货风险评分服务（待修复）。公开 API 与 `solution.py` 一致，可以原样放进真实工作区的 `service.py`。

这份代码能跑，但有几处和下面的规则不符：它就是要你修的东西。

产品规则（逐条都有测试）：
 1. `evaluate(rating, value_cents, account_age_days)` 只接受三个整数：评分 1..5，金额（分）≥ 0，账龄（天）≥ 0；
    布尔值、浮点数、字符串、`None`、范围外的值一律抛 `ServiceError(400, "invalid_input")`，且在任何计算之前；
    合法整数没有人为的上界（评分除外）。
 2. 评分分项：1→40、2→30、3→20、4→10、5→0。
 3. 金额分项：0..9999 分→0；10000..49999→15；≥ 50000→30（下界含）。
 4. 账龄分项：0..29 天→25；30..179→10；≥ 180→0（下界含）。
 5. 总分是三项之和，不归一、不取整、不截断；< 30 为 "approve"，30 ≤ 总分 < 60 为 "manual_review"，≥ 60 为 "reject"。
 6. 返回恰好 `{"score": int, "decision": str, "components": {"rating": int, "value": int, "age": int}}`。
 7. `evaluate_many(records)` 把有限可迭代对象只遍历一次，按输入顺序为每条记录返回一个结果：
    记录必须是字典且键恰好是 `rating`、`value_cents`、`account_age_days`；
    合法的记录是 `{"result": evaluate(...), "error": None}`，无效的记录是 `{"result": None, "error": "invalid_input"}`；
    坏记录不影响后面的记录；空输入返回 `[]`；输入迭代器自己抛出的异常不能被吞掉。
 8. 引擎无状态：调用之间、返回的嵌套字典之间互不影响，不修改输入；没有时钟、网络、汇率、学习模型的依赖。

Python 3.11，标准库。
"""

from __future__ import annotations


class ServiceError(Exception):
    """对外的服务错误：status 是 HTTP 状态码，code 是稳定的错误码字符串。"""

    def __init__(self, status: int, code: str) -> None:
        self.status, self.code = status, code
        super().__init__(code)


class RiskEngine:
    def evaluate(self, rating, value_cents, account_age_days):
        for x in (rating, value_cents, account_age_days):
            if x is None or isinstance(x, (str, float)):
                raise ServiceError(400, "invalid_input")
        if not 0 <= rating <= 5 or value_cents < 0 or account_age_days < 0:
            raise ServiceError(400, "invalid_input")
        rating_points = (5 - rating) * 5
        if value_cents > 50000:
            value_points = 30
        elif value_cents > 10000:
            value_points = 15
        else:
            value_points = 0
        if account_age_days < 30:
            age_points = 25
        elif account_age_days < 180:
            age_points = 10
        else:
            age_points = 0
        score = rating_points + value_points + age_points
        if score > 60:
            decision = "reject"
        elif score >= 30:
            decision = "manual_review"
        else:
            decision = "approve"
        return {"score": score, "decision": decision, "components": {"rating": rating_points, "value": value_points, "age": age_points}}

    def evaluate_many(self, records):
        results = []
        for record in records:
            try:
                if not isinstance(record, dict) or set(record) != {"rating", "value_cents", "account_age_days"}:
                    raise ServiceError(400, "invalid_input")
                results.append({"result": self.evaluate(**record), "error": None})
            except ServiceError:
                results.append({"result": None, "error": None})
        return results
