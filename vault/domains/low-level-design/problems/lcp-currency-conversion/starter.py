"""汇率换算服务练习骨架。公开 API 与 `solution.py` 一致，可以原样放进真实工作区的 `service.py`
（真实工作区里 `ServiceError` 在 `models.py`，其余相同）。同一个实例上的调用按顺序执行，不需要锁。

产品规则（逐条都有测试）：
 1. `register_rates(stream)` 只接受非空字符串；`None`、数字、字节串、空串都是 `ServiceError(400, "invalid_input")`。
    记录用逗号分隔，每条记录恰好是 `FROM:TO:RATE` 三段；空记录、空字段、多余的冒号、首尾逗号都非法；任何字段都不去空白、不改大小写。
 2. 货币码是 3 到 5 个 ASCII 大写字母；`FROM == TO` 的自报价非法。
 3. 汇率字面量要整串匹配 `[+-]?(?:[0-9]+(?:\\.[0-9]*)?|\\.[0-9]+)(?:[eE][+-]?[0-9]+)?`：`1`、`1.`、`.5`、`+2.5e-1` 合法；
    空白、十六进制、下划线、Unicode 数字、`nan`、`inf` 非法。
 4. 字面量解析成最接近的 binary64，且必须有限、落在 `[1e-12, 1e12]`（含两端）；边界看的是解析后的值，
    不做货币舍入，也不用对数近似。
 5. 累计图里出现过的货币（边的起点和终点都算）至多 8 种；一批报价让它超过 8 种，这批非法。报价有方向，登记一个方向不会产生反方向。
 6. 同一有向对可以重复，后写的覆盖先写的，跨调用也一样；成功时返回 `(201, {"registered_count": n})`，`n` 是这次调用的记录数（含重复）。
 7. 整批原子：任何一条记录非法，或货币数超限，整个调用什么都不改变，包括同批里更早的覆盖和新货币。
 8. 查询先后检查：两个货币码的格式（不是字符串或格式不对 → 400 `invalid_input`，哪怕另一个码未知），
    再检查两个码是否出现过（没出现过 → 404 `currency_not_found`），最后才找路线（没有 → 404 `route_not_found`）。
    只作过报价终点的货币也算出现过。
 9. 两个码相同（且出现过）：直达 `rate` 为 1；单次中转 `rates` 为 `[1]`；最优 `best_rate` 为 1、`path` 为 `[码]`。
10. `get_direct_rate` 返回 `(200, {"from", "to", "rate"})`，不同码时就是登记的那条边，没有则 `route_not_found`。
11. `get_single_hop_rates` 返回 `(200, {"from", "to", "rates"})`：直达边，加上每个 `S→M→T`（S、M、T 互不相同）两段汇率的乘积；
    不同路径得到相同数值时都保留；升序排序；更长的路线不算。
12. `get_best_rate` 返回 `(200, {"from", "to", "best_rate", "path"})`。考虑所有简单有向路径（每种货币至多出现一次，走到 T 就停），
    乘积从 1 开始从左到右连乘。设最大乘积为 M，`M - 乘积 <= 1e-5`（只用绝对容差）的路径合格；
    合格者里选边数最少的，再选整条货币序列字典序最小的。合格性始终相对 M，不相对已选中的路径；返回被选中路径自己的乘积，可能略小于 M。
13. `list_pairs(from_currency=None)` 返回 `(200, [{"from_currency", "to_currency", "rate"}, ...])`，按起点再按终点排序；
    `None` 列出全部；给了过滤码就走同样的格式检查（400）和出现过检查（404）；只作终点的货币返回空列表；空服务返回空列表。
14. 返回值是独立快照（改它不影响服务，之后的登记也不影响已拿到的结果）；返回的数字是 float，不是 bool 也不是字符串，不带多余字段；
    不同服务实例互不共享状态。
"""

from __future__ import annotations


class ServiceError(Exception):
    """对外的错误：status 是 HTTP 状态码，code 是稳定的字符串。"""

    def __init__(self, status: int, code: str) -> None:
        self.status, self.code = status, code
        super().__init__(code)


class CurrencyExchangeService:
    def __init__(self) -> None:
        pass

    def register_rates(self, rates_stream: str) -> tuple[int, dict]:
        raise NotImplementedError("todo: validate the whole batch, then publish it in one step")

    def get_direct_rate(self, from_currency: str, to_currency: str) -> tuple[int, dict]:
        raise NotImplementedError("todo: return the registered edge")

    def get_single_hop_rates(self, from_currency: str, to_currency: str) -> tuple[int, dict]:
        raise NotImplementedError("todo: direct edge plus every one-intermediate route, sorted")

    def get_best_rate(self, from_currency: str, to_currency: str) -> tuple[int, dict]:
        raise NotImplementedError("todo: search simple paths, apply the tolerance rule")

    def list_pairs(self, from_currency: str | None = None) -> tuple[int, list[dict]]:
        raise NotImplementedError("todo: list edges ordered by source, then target")
