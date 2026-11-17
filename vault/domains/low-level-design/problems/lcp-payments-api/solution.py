"""付款记录接口（Payments API）：SQLite 里的两张表，三个函数。
设计：账户只有 id，余额不存，每次从付款流水现算（余额 = 该账户全部付款金额之和，正负都算）；
存在性由 `accounts` 表回答，不由付款表回答，所以"没有付款的账户"（余额 0）和"不存在的账户"（None）分得开；
记付款是单条 `INSERT … SELECT … WHERE EXISTS`，账户不在时一行都不写，也就不会消耗付款 id；
两个 id 序列都靠 AUTOINCREMENT 落在 `sqlite_sequence` 表里，关库重开后接着走。
三个函数都不关调用方的连接，也不自己管事务：每个函数只发一条会改数据的语句，语句本身是原子的。
"""

from __future__ import annotations

import sqlite3
from dataclasses import dataclass

# ---- 值类型与建库（真实工作区里由 models.py 提供，函数部分单独放进 service.py）----


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
    """打开（或新建）一个数据库文件。自动提交模式：每条语句各自成为一个事务；外键约束打开。"""
    connection = sqlite3.connect(path, isolation_level=None)
    connection.executescript("PRAGMA foreign_keys = ON;" + SCHEMA)  # 外键是连接级开关，每次打开都要设
    return connection


# ---- 三个操作 ----

BALANCE_OF = """
SELECT a.id,
       (SELECT COALESCE(SUM(p.amount), 0) FROM payments AS p WHERE p.account_id = a.id)
FROM accounts AS a
WHERE a.id = ?
"""

# 账户在才会产生一行可插入的数据：存在性检查与写入是同一条语句里的两个部分，中间没有缝隙
PAY_IF_ACCOUNT_EXISTS = """
INSERT INTO payments (account_id, amount)
SELECT a.id, ? FROM accounts AS a WHERE a.id = ?
"""


def create_account(database: sqlite3.Connection) -> Account:
    """新账户：id 由 AUTOINCREMENT 分配，余额必然是 0（还没有任何付款）。"""
    cursor = database.execute("INSERT INTO accounts DEFAULT VALUES")
    return Account(cursor.lastrowid, 0)


def get_account(database: sqlite3.Connection, account_id: int) -> Account | None:
    """账户不存在返回 None；存在但没有付款，余额是 0（COALESCE 把空集的 NULL 换成 0）。"""
    row = database.execute(BALANCE_OF, (account_id,)).fetchone()
    return None if row is None else Account(row[0], row[1])


def create_payment(database: sqlite3.Connection, account_id: int, amount: int) -> Payment | None:
    """给已有账户记一笔付款；账户不存在返回 None，什么都不写（rowcount 为 0），付款 id 原地不动。
    金额可正可负可为零，不检查透支；两笔相同的付款就是两条记录。"""
    cursor = database.execute(PAY_IF_ACCOUNT_EXISTS, (amount, account_id))
    if cursor.rowcount == 0:
        return None
    return Payment(cursor.lastrowid, account_id, amount)


if __name__ == "__main__":
    db = open_database(":memory:")
    first = create_account(db)
    print(first, create_payment(db, first.id, 700), create_payment(db, first.id, -250))
    print(get_account(db, first.id), get_account(db, 99), create_payment(db, 99, 5))
