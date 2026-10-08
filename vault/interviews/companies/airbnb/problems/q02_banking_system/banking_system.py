"""The locked interface, as CodeSignal ships it.

Level 1 is transcribed from the assessment photos. Levels 2-4 are (reconstructed) from GitHub versions of the same
problem, see ../../catalog/raw/codesignal_banking_system_photos.md. Names may differ in the real test; semantics transfer.
"""
from abc import ABC


class BankingSystem(ABC):
    """
    `BankingSystem` interface.
    """

    # ---- Level 1 (verbatim) -------------------------------------------------------------

    def create_account(self, timestamp: int, account_id: str) -> bool:
        """
        Should create a new account with the given `account_id` if
        it doesn't already exist.
        Returns `True` if the account was successfully created or
        `False` if an account with `account_id` already exists.
        """
        # default implementation
        return False

    def deposit(self, timestamp: int, account_id: str, amount: int) -> int | None:
        """
        Should deposit the given `amount` of money to the specified
        account `account_id`.
        Returns the total amount of money in the account (balance)
        after processing the query.
        If the specified account does not exist, should return
        `None`.
        """
        # default implementation
        return None

    def pay(self, timestamp: int, account_id: str, amount: int) -> int | None:
        """
        Should withdraw the given `amount` of money from the
        specified account.
        Returns the amount of money in the account (balance) after
        processing the query.
        If the specified account does not exist, or if the account
        has insufficient funds to perform the withdrawal, should
        return `None`.
        """
        # default implementation
        return None

    # ---- Level 2 (reconstructed) --------------------------------------------------------

    def top_activity(self, timestamp: int, n: int) -> list[str]:
        """
        Should return the identifiers of the top `n` accounts with
        the highest total value of transactions, sorted in
        descending order; ties are sorted alphabetically by
        `account_id` in ascending order.
        The total value of transactions is the sum of all successful
        deposits, payments and accepted transfers (both sides).
        The result is a list of strings "<account_id>(<total>)".
        If fewer than `n` accounts exist, return all of them.
        """
        # default implementation
        return []

    # ---- Level 3 (reconstructed) --------------------------------------------------------

    def transfer(self, timestamp: int, source_account_id: str, target_account_id: str,
                 amount: int) -> str | None:
        """
        Should initiate a transfer between accounts. The `amount` is
        withdrawn from the source account immediately and held until
        the target accepts the transfer or the transfer expires.
        Returns the transfer id "transfer<ordinal>" (counting
        successful transfers from 1).
        Returns `None` if the source and target are the same, if
        either account does not exist, or if the source has
        insufficient funds.
        A transfer expires 24 hours (86400000 ms) after it was
        initiated: from `timestamp + 86400000` on it can no longer be
        accepted and the held money returns to the source account.
        """
        # default implementation
        return None

    def accept_transfer(self, timestamp: int, account_id: str, transfer_id: str) -> bool:
        """
        Should accept the transfer `transfer_id` on behalf of
        `account_id`: the held money is added to the target.
        Returns `True` on success, `False` if the transfer does not
        exist, was already accepted, has expired, or `account_id` is
        not its target.
        """
        # default implementation
        return False

    # ---- Level 4 (reconstructed) --------------------------------------------------------

    def merge_accounts(self, timestamp: int, account_id_1: str, account_id_2: str) -> bool:
        """
        Should merge `account_id_2` into `account_id_1`.
        Returns `True` on success, `False` if the ids are equal or
        either account does not exist.
        Pending transfers from `account_id_2`, and between the two
        accounts, are cancelled and refunded; pending transfers to
        `account_id_2` are redirected to `account_id_1`. Balance and
        total transaction value of `account_id_2` are added to
        `account_id_1`. `account_id_2` stops existing (its id may be
        created again later).
        """
        # default implementation
        return False

    def get_balance(self, timestamp: int, account_id: str, time_at: int) -> int | None:
        """
        Should return the balance of `account_id` at time `time_at`
        (after every operation with timestamp <= `time_at`).
        Returns `None` if the account did not exist at `time_at`
        (not yet created, or already merged into another account).
        """
        # default implementation
        return None
