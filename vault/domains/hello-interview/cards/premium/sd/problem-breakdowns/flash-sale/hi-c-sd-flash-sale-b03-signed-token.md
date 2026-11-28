---
id: hi-c-sd-flash-sale-b03-signed-token
node: sd.problem-breakdowns.flash-sale.beyond
type: qa
step: 3
---
## Q
**限时抢购 · 拓展：用 HMAC 实现无状态的准入令牌**｜拓展 · 加分

准入令牌怎么签名、验证？为什么必须用恒定时间比较？

## A
**模式。** 签名令牌（signed token）：服务端用密钥给一段声明做 HMAC，验证时重新计算，不需要查库。

```python
import base64
import hashlib
import hmac
import json
import time

SECRET = b"rotate-me"        # 示例密钥；真实密钥来自密钥管理并支持轮换


def _b64(b: bytes) -> str:
    return base64.urlsafe_b64encode(b).decode()


def issue(user: str, product: str, ttl_s: int = 30, now: float | None = None) -> str:
    claims = {"u": user, "p": product, "exp": int((now or time.time()) + ttl_s)}
    body = _b64(json.dumps(claims, separators=(",", ":")).encode())
    sig = _b64(hmac.new(SECRET, body.encode(), hashlib.sha256).digest())
    return f"{body}.{sig}"


def verify(token: str, product: str, now: float | None = None) -> str | None:
    """通过则返回 userId，否则 None。"""
    try:
        body, sig = token.split(".")
        want = _b64(hmac.new(SECRET, body.encode(), hashlib.sha256).digest())
        # 恒定时间比较：普通 == 在第一个不同字节处提前返回，耗时泄露签名前缀
        if not hmac.compare_digest(sig, want):
            return None
        claims = json.loads(base64.urlsafe_b64decode(body))
    except ValueError:
        return None
    if claims["p"] != product or claims["exp"] < (now or time.time()):
        return None             # 绑定商品和有效期，其他商品的令牌不能拿来用
    return claims["u"]


t = issue("alice", "shoe-1", now=1000)
assert verify(t, "shoe-1", now=1010) == "alice"
assert verify(t, "shoe-2", now=1010) is None          # 换商品
assert verify(t, "shoe-1", now=1100) is None          # 过期
assert verify(t[:-2] + "xx", "shoe-1", now=1010) is None   # 被篡改
```
- **为什么：** 网关用对称密钥验签，不依赖数据库，在洪峰下几乎没有成本；令牌里写明 userId、productId、过期时间。
- **不防重放：** 同一令牌有效期内可重复使用，要靠一人一预留的唯一约束或一次性 ID 来补。
- **密钥管理：** 密钥泄露等于任何人都能自己发令牌；要支持轮换，令牌带密钥版本，验签同时接受新旧两个版本。
- **何时不用：** 需要立即撤销某个令牌时，纯无状态做不到，要额外维护黑名单。
