"""付款记录接口（Payments API）：补全三个函数。

规则（每条都有测试盯着）：
1. `create_account`：插入一个账户，返回 `Account(id, 0)`；id 在新库里从 1 开始，每成功建一个加 1。
2. `get_account`：返回 `Account(id, 余额)`，余额是该账户全部付款金额之和（正负都算）；没有付款时余额是 0。
3. `get_account`：账户不存在返回 `None`——这是正常结果，不抛异常。
4. `create_payment`：账户存在时插入一条付款，返回 `Payment(id, account, amount)`。
5. `create_payment`：账户不存在返回 `None`，不写任何数据，也不消耗付款 id。
6. 账户 id 与付款 id 是两条独立的序列；金额为 0 的付款也是一条记录，也推进付款 id。
7. 金额可正可负可为零，不检查透支；两次相同的提交是两条不同的记录。
8. 关库重开后，账户、付款、余额和两条 id 序列都要还在；不同的数据库文件互不共享任何状态。
9. 不要关调用方传进来的连接；金额是整数分，余额与 id 都在 ±(2^53−1) 之内，返回的必须是 int。
"""

from __future__ import annotations

import sqlite3
from dataclasses import dataclass


@dataclass(frozen=True)
class Account:
    id: int
    balance: int


@dataclass(frozen=True)
class Payment:
    id: int
    account: int
    amount: int


SCHEMA = """
CREATE TABLE IF NOT EXISTS accounts (id INTEGER PRIMARY KEY AUTOINCREMENT);
CREATE TABLE IF NOT EXISTS payments (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    account_id INTEGER NOT NULL REFERENCES accounts(id),
    amount     INTEGER NOT NULL
);
"""


def open_database(path: str) -> sqlite3.Connection:
    connection = sqlite3.connect(path, isolation_level=None)
    connection.executescript("PRAGMA foreign_keys = ON;" + SCHEMA)  # 外键是连接级开关，每次打开都要设
    return connection


def create_account(database: sqlite3.Connection) -> Account:
    raise NotImplementedError


def get_account(database: sqlite3.Connection, account_id: int) -> Account | None:
    raise NotImplementedError


def create_payment(database: sqlite3.Connection, account_id: int, amount: int) -> Payment | None:
    raise NotImplementedError
