"""运费计算服务练习骨架。公开 API 与 `solution.py` 一致，可以原样放进真实工作区的 `service.py`
（真实工作区里 `ServiceError` 在 `models.py`，其余相同）。同一个实例上的调用按顺序执行，不需要锁。

产品规则（逐条都有测试）：
 1. 国家码匹配 `[A-Z]{2,5}`，商品名匹配 `[A-Za-z0-9_-]{1,32}`；整串匹配，区分大小写，不去空白、不改大小写。
    所有十进制数字只含 ASCII 数字，允许前导零，每个数字不超过 1,000,000；金额一律是整数分。
 2. 一条费率是六段、用逗号分开的文本：`国家,商品,类型,最小数量,最大数量,费用`。类型是 `incremental`（进入本段的每一件
    各收一次费用）或 `fixed`（进入本段就一次性收费用）；最大数量写 `*` 表示无上界，别的写法都不是无上界；费用必须为正。
 3. `register_rules(rules)`：空批次、非列表、任何一行语法不对，都是 `ServiceError(400, "invalid_input")`。
    全部行的语法先检查完，再检查分段；所以语法错在批次的任何位置，都先于分段错。
 4. 同一个（国家，商品）的所有行归到一起，按最小数量排序，每段是整数闭区间：第一段从 1 开始，后一段的最小数量
    是前一段有限最大数量加 1，每段的有限最大数量不小于它的最小数量，且恰好最后一段无上界。
    缺口、重叠、起点重复、`*` 之后还有段、从 0 起、最后一段有限，都是 `ServiceError(422, "invalid_rules")`。
 5. 整批原子：任何一步失败，整个调用什么都不改变，包括同批里其他国家和商品。成功时，批里出现的每个（国家，商品）
    用新分段表整体替换旧的，没出现的保持原样；返回 `(201, {"registered_count": 输入行数})`。输入顺序不要求有序。
 6. `calculate_shipping(country, items)` 的错误按这个顺序：
    ① 国家语法不对，或 items 不是列表：400 `invalid_input`；② 这个国家一条费率都没登记（哪怕订单为空）：404 `country_not_found`；
    ③ 任何一行畸形、数量不是 1 到 1,000,000 的整数，或同一商品合并后超过 1,000,000：400；
    ④ 订单里有商品在该国没有费率：404 `product_not_found`；⑤ 某商品的费用或整单总额超过 2,147,483,647 分：400。
 7. 订单行是 `商品,数量`，恰好两段；数量为 0 不是一件商品，直接拒绝，不要造出"第 0 件"的分段。
    先把同一商品的数量相加，再算价；从第 1 件开始逐段填，把走到的每一段的费用都加起来，后面的段不会取代前面的段。
    `incremental` 段收 进入本段的件数 × 费用；`fixed` 段只要有件数进入就收一次费用；末段是 `fixed` 且无上界也合法。
 8. 金额用精确整数算，算完整笔再和 2,147,483,647 比，不能先转成浮点数或先截断。
 9. 报价返回 `(200, {"total_cost", "country", "breakdown"})`；`breakdown` 每行是 `{"product", "quantity"（合并后的）, "cost"}`，
    按商品名的 ASCII 升序；已知国家的空订单返回 `{"total_cost": 0, "country": 国家, "breakdown": []}`。
10. `list_rules(country=None)` 返回 `(200, 行列表)`；每行 `country, product, type, min_quantity, max_quantity（无上界是 None）, cost_cents`，
    按国家、商品、最小数量排序；给了过滤码就只要完全相等的国家；没有匹配（包括空串和畸形的码）就是空列表，也不会因此产生一个国家。
11. 不改调用方传进来的输入；返回的容器和行与内部状态无关，之后的登记不改变已经拿到的结果；不同实例互不共享状态。
"""

from __future__ import annotations


class ServiceError(Exception):
    """对外的错误：status 是 HTTP 状态码，code 是稳定的字符串。"""

    def __init__(self, status: int, code: str) -> None:
        self.status, self.code = status, code
        super().__init__(code)


class ShippingService:
    def __init__(self) -> None:
        pass

    def register_rules(self, rules: list[str]) -> tuple[int, dict]:
        raise NotImplementedError("todo: parse every line, build every schedule on a copy, then publish once")

    def calculate_shipping(self, country: str, items: list[str]) -> tuple[int, dict]:
        raise NotImplementedError("todo: merge repeated products, fill the tiers from unit 1, check the bound")

    def list_rules(self, country: str | None = None) -> tuple[int, list[dict]]:
        raise NotImplementedError("todo: rows sorted by country, product, minimum quantity")
