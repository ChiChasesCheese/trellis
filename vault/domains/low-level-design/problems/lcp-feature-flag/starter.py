"""功能开关与实验分组练习骨架。公开 API 与 `solution.py` 一致，可以原样放进真实工作区的 `feature_flags.py`。

产品规则（逐条都有测试）：
 1. 开关配置是 JSON 对象：`key`（匹配 `[A-Za-z0-9_-]{1,64}`，整串匹配，末尾换行不行）、`enabled`（布尔）、
    `variants`（非空、互不相同、非空字符串的列表）、`default_variant`（必须是某个变体）、`rules`（可省略，默认 `[]`）、
    `fallthrough.rollout`（必填，非空）。
 2. 规则 `{conditions, serve}`：`conditions` 可省略（默认 `[]`），条件之间是 AND，空列表命中所有用户；
    `serve` 必须是某个变体。条件 `{attribute, op, value}`：`attribute` 是非空字符串。
 3. 七个操作符与值的类型：`eq`/`neq` 要字符串、数字或布尔；`in`/`not_in` 要列表；`gt`/`lt` 要数字（布尔不算数字）；
    `contains` 要字符串。未知操作符、类型不符都抛 `ValidationError`。
 4. 放量表 `rollout`：键必须是已声明变体（没写的变体权重为 0），值是非负整数（浮点和布尔都不行），总和恰好 100。
 5. 规范化：丢掉开关、规则、条件、`fallthrough` 里的多余属性，存下来的配置形状固定；
    `create_flag`/`update_flag`/`get_flag`/`list_flags` 返回的都是调用方可随便修改的新对象，
    入参在创建之后再被修改也不影响已存的开关。
 6. 校验在碰存储之前完成：非法配置不创建、不替换，也不留痕。`create_flag` 重复 key 抛 `ConflictError`；
    `update_flag` 先校验（包括正文的 `key` 必须等于路径里的 key，否则 `ValidationError`），再查是否存在（`NotFoundError`）；
    整体替换，位置保持不变；`delete_flag` 返回是否存在过；`list_flags` 按创建顺序，删除后重建排到最后。
 7. 求值先校验入参：`user_id` 必须是非空字符串、`attributes` 给了就必须是对象（`None` 当作 `{}`），都抛 `ValidationError`；
    然后才查开关是否存在（`NotFoundError`）。
 8. 求值顺序：已停用 → `{"value": default_variant, "reason": "DISABLED"}`，规则与放量都不看；
    否则规则从上到下，第一条条件全部命中的赢 → `{"value", "reason": "RULE_MATCH", "rule_index"}`；
    都不命中 → `{"value", "reason": "FALLTHROUGH"}`。`rule_index` 只出现在 `RULE_MATCH` 里。
 9. 属性缺失，或类型与操作符不匹配，条件一律为 False，绝不抛异常；缺失时 `neq` 与 `not_in` 也是 False。
10. 相等是类型感知的：`True` 不等于 `1`；数字按精确值比较（`10**23` 不等于 `1e23`，`5` 等于 `5.0`）；字符串与数字不相等。
11. 分桶：`bucket = int(sha256(f"{flag_key}:{user_id}".encode("utf-8")).hexdigest(), 16) % 10000`，不能用随机数；
    变体按 `variants` 列表的顺序（不是放量表键的顺序）依次占累计区间，每个百分点 100 个桶单位，区间左闭右开。
12. 放量比例只决定区间边界，不进哈希：比例调整后，已经分到某变体、其区间没有被挤走的用户不变。
13. 并发：多线程同时创建同名开关恰好一个成功；更新是原子的，同时进行的求值只会看到完整的旧版或新版。
"""

from __future__ import annotations

import threading
from dataclasses import dataclass
from typing import Any

ALLOWED_OPS = frozenset({"eq", "neq", "in", "not_in", "gt", "lt", "contains"})
BUCKET_SPACE = 10000


class FeatureFlagError(Exception):
    """所有服务错误的基类。"""


class ValidationError(FeatureFlagError):
    """输入不合法（HTTP 400）。"""


class NotFoundError(FeatureFlagError):
    """开关不存在（HTTP 404）。"""


class ConflictError(FeatureFlagError):
    """同名开关已存在（HTTP 409）。"""


def bucket(flag_key: str, user_id: str) -> int:
    """用户在某个开关里的稳定桶号，范围 0..9999。"""
    raise NotImplementedError


@dataclass(frozen=True, slots=True)
class Condition:
    attribute: str
    op: str
    value: Any

    def matches(self, attributes: dict[str, Any]) -> bool:
        raise NotImplementedError

    def to_config(self) -> dict[str, Any]:
        raise NotImplementedError


@dataclass(frozen=True, slots=True)
class Rule:
    conditions: tuple[Condition, ...]
    serve: str

    def matches(self, attributes: dict[str, Any]) -> bool:
        raise NotImplementedError

    def to_config(self) -> dict[str, Any]:
        raise NotImplementedError


@dataclass(frozen=True, slots=True)
class Flag:
    key: str
    enabled: bool
    variants: tuple[str, ...]
    default_variant: str
    rules: tuple[Rule, ...]
    rollout: tuple[tuple[str, int], ...]

    def pick(self, bucket_number: int) -> str:
        raise NotImplementedError

    def evaluate(self, user_id: str, attributes: dict[str, Any]) -> dict[str, Any]:
        raise NotImplementedError

    def to_config(self) -> dict[str, Any]:
        raise NotImplementedError


def parse_flag(config: Any) -> Flag:
    """校验并规范化一份配置，任何不合法都抛 ValidationError。"""
    raise NotImplementedError


class FeatureFlagService:
    def __init__(self) -> None:
        self._flags: dict[str, Flag] = {}
        self._lock = threading.Lock()

    def create_flag(self, config: dict) -> dict:
        raise NotImplementedError

    def get_flag(self, key: str) -> dict | None:
        raise NotImplementedError

    def update_flag(self, key: str, config: dict) -> dict:
        raise NotImplementedError

    def delete_flag(self, key: str) -> bool:
        raise NotImplementedError

    def list_flags(self) -> list[dict]:
        raise NotImplementedError

    def evaluate(self, key: str, user_id: str, attributes: dict | None = None) -> dict:
        raise NotImplementedError
