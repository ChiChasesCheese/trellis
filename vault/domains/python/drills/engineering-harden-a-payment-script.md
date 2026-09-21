---
nodes: [engineering.robustness, engineering.money-time, engineering.logging-config, engineering.testing]
tags: [drill, interview]
---
# Drill：把一段收款脚本改成生产可用的版本

```python
import requests
from datetime import datetime

def charge_customer(customer_id, amount):
    print(f"charging {customer_id} {amount}")
    try:
        total = amount * 1.0825  # 含税
        charged_at = datetime.utcnow()
        resp = requests.post(
            "https://psp.example/charge",
            json={"customer": customer_id, "amount": total, "at": charged_at.isoformat()},
        )
        return resp.json()
    except:
        print("charge failed")
        return None
```

这段代码能跑，但金额用 float 算、裸 `except:` 吞掉一切、用 `print` 记日志、没有一行测试。逐项改掉。

**限制与要求**
- 不许只改一处就说「够了」，四个问题（金额精度、异常处理、日志、测试）都要改。
- 改完的异常处理不能仍然吞掉调用方需要知道的失败。
- 时间戳必须是 aware datetime，不许继续用 `utcnow()`。
- 测试不许真的发网络请求，且不许依赖真实系统时钟。
- 20 分钟内完成全部四项。

**分关要求**
- 第 1 关（约 5 分钟）：把金额和时间戳改对。
- 第 2 关（约 5 分钟）：把异常处理和日志改对。
- 第 3 关（约 8 分钟）：给改完的函数写 pytest 测试，覆盖「成功」「PSP 抛异常」两条路径，不发真实请求。
- 第 4 关（约 2 分钟）：追问——如果 `charge_customer` 所在的模块以后要被别的团队当依赖库导入，日志配置上还要注意什么？

**评分点（强答案会命中）**
- `amount * 1.0825` 用 float 算税后金额：二进制浮点无法精确表示十进制小数，反复运算的误差会破坏金额的精确相等；应该用 `Decimal`，且要从字符串或整数分构造，不能直接把 float 传进 `Decimal()` [[money-decimal-exact-vs-float]] [[money-decimal-str-vs-float-ctor]]
- 四舍五入到分要显式传 `rounding` 参数（如 `ROUND_HALF_UP`）：`decimal` 模块默认上下文是 `ROUND_HALF_EVEN`（银行家舍入），不显式指定会得到和产品预期不一致的结果 [[money-quantize-rounding-explicit]]
- `datetime.utcnow()` 从 3.12 起弃用，因为它返回的是 `tzinfo=None` 的 naive 对象，容易在下游被误当本地时间处理；应改用 `datetime.now(timezone.utc)` 得到 aware 对象 [[money-utcnow-deprecated]]
- naive 和 aware 的 `datetime` 相减/比较会抛 `TypeError`；一旦把时间戳统一成 aware，后续所有跟这个时间戳做运算的代码也必须是 aware，不能混用 [[money-naive-aware-datetime-mix-typeerror]]
- 裸 `except:` 应该改成先捕获具体的异常类型（如 `requests.RequestException`），`except Exception` 放最后兜底且要记录后 `raise` 重新抛出，不能让调用方误以为调用成功 [[robust-except-exception-specific-first]]
- 只有明确知道会发生、且确认可以安全忽略的具体异常才适合吞掉（如用 `contextlib.suppress` 而不是宽泛的 `except: pass`）；给库/模块定义自己的根异常类，调用方捕获这一个根类型就能拦住所有该模块抛出的错误 [[robust-suppress-vs-bare-except-pass]] [[robust-oserror-hierarchy-catch-root]]
- `try` 块只放真正可能抛异常的那一两行，把「调用成功后的后续处理」放进 `else` 子句，避免后续代码里意外抛出的同类异常被误判成本次调用失败 [[robust-try-else-minimize-scope]]
- `print()` 只适合面向用户的常规输出；报告运行期间事件、用于监控和排查该用 `logging`，且要 `logger = logging.getLogger(__name__)` 让 logger 层级和模块结构对应，不同子模块可单独调级别 [[logging-vs-print-when-to-use]] [[logging-getlogger-name-convention]]
- 测试要注入时钟（把「取当前时间」做成可传入的参数或依赖）而不是依赖真实系统时间；`unittest.mock.patch` 打桩要打「使用/查找对象的地方」（这个模块里 `import requests` 后用到的 `requests.post`），不是打 `requests` 库定义处 [[test-mock-where-to-patch]]
- 测试 PSP 抛异常的路径要给 mock 设 `side_effect=requests.RequestException(...)`，而不是 `return_value`，才能真正驱动异常处理分支；用 `@pytest.mark.parametrize` 覆盖多组金额（含边界，如 0、负数、需要进位的小数）而不是每个边界单独写一个测试函数 [[test-mock-side-effect-vs-return-value]] [[test-pytest-parametrize-boundary]]

**参考答案**

```python
import logging
from datetime import datetime, timezone
from decimal import ROUND_HALF_UP, Decimal

import requests

logger = logging.getLogger(__name__)

class PaymentError(Exception):
    """本模块所有支付相关异常的根类。"""

TAX_RATE = Decimal("1.0825")

def charge_customer(customer_id, amount, *, now=lambda: datetime.now(timezone.utc)):
    total = (Decimal(str(amount)) * TAX_RATE).quantize(
        Decimal("0.01"), rounding=ROUND_HALF_UP
    )
    charged_at = now()
    try:
        resp = requests.post(
            "https://psp.example/charge",
            json={"customer": customer_id, "amount": str(total), "at": charged_at.isoformat()},
            timeout=5,
        )
    except requests.RequestException as err:
        logger.error("charge failed for %s: %s", customer_id, err)
        raise PaymentError(f"charge failed for {customer_id}") from err
    else:
        return resp.json()
```

`Decimal(str(amount))` 避免把 float 的二进制误差带进来；`quantize(..., rounding=ROUND_HALF_UP)` 把舍入规则写死；`now` 做成默认参数，测试时可以传入固定时钟；`requests.post` 只在 `try` 里，成功后的 `resp.json()` 放进 `else`；捕获具体的 `requests.RequestException` 后记录日志并包成模块自己的 `PaymentError` 重新抛出，不吞异常。

```python
import requests
import pytest
from datetime import datetime, timezone
from unittest.mock import patch
from payment import charge_customer, PaymentError

FIXED_NOW = datetime(2026, 9, 21, 12, 0, tzinfo=timezone.utc)

@pytest.mark.parametrize("amount", ["10.00", "0.01", "999.995"])
def test_charge_success(amount):
    with patch("payment.requests.post") as mock_post:
        mock_post.return_value.json.return_value = {"status": "ok"}
        result = charge_customer("cust_1", amount, now=lambda: FIXED_NOW)
        assert result == {"status": "ok"}

def test_charge_raises_payment_error_on_network_failure():
    with patch("payment.requests.post", side_effect=requests.RequestException("timeout")):
        with pytest.raises(PaymentError):
            charge_customer("cust_1", "10.00", now=lambda: FIXED_NOW)
```

`patch("payment.requests.post")` 打的是 `payment` 模块里查找 `requests.post` 用到的这个名字，不是 `requests` 库本身；`now=lambda: FIXED_NOW` 注入固定时钟，测试不依赖真实系统时间；`parametrize` 覆盖多组金额边界；失败路径用 `side_effect` 让 mock 真的抛出网络异常，断言函数把它包装成了 `PaymentError`。

第 4 关：这个模块被当依赖库导入时，`logger = logging.getLogger(__name__)` 本身没问题，但绝不能在库代码里往根 logger 写日志，也不能自己加 `StreamHandler`/`FileHandler` 这类真正输出的处理器——是否配置处理器、日志往哪里去，应该完全交给使用这个库的应用决定；如果担心库在应用完全没配置 logging 时把 WARNING 及以上消息默认打到 `sys.stderr`，可以给模块顶层 logger 加一个 `NullHandler`。

**尝试记录**
| 日期 | 用时 | 卡在哪 | 下次 |
|---|---|---|---|
