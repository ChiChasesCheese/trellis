---
id: craft-external-call-outside-the-lock-2-window-must-be-recoverable
node: craft.patterns.external-call-outside-the-lock
type: qa
step: 2
---
## Q
**外部调用不持锁 · 付款期间持有期过期了怎么办**｜模式

用户占了座位，持有期 5 分钟，付款耗时超过了持有期；这段时间座位已被另一位用户合法地占走。付款回来后，直接把座位写成「我的」，会怎样？应该怎么写这个提交？

## A
**要点。** 锁外窗口里世界会变，提交时必须重新核对「我手里的占位还是不是有效的」：用持有凭证（hold id）和过期时间，而不是只看座位当前的状态。失效就抛错，并把「款已付、需要退」明确告诉调用方，也绝不覆盖别人的座位。进入窗口前先把持有期延长到付款窗口，让这种情况尽量少发生。

```python
def commit_naive(user, hid):
    seat.holder = user                       # 直接覆盖

def commit_checked(user, hid):
    if seat.hold_id != hid or time.monotonic() >= seat.expires:
        raise RuntimeError(f"hold {hid} 已失效：付款成功但座位已被释放，需要退款")
    seat.holder = user
```

ann 付款很慢，持有期过了，bob 合法占了座位，之后 ann 提交：

```
commit_naive -> ann 落单
   座位现在属于 ann
commit_checked -> 抛错: hold 3 已失效：付款成功但座位已被释放，需要退款
   座位现在属于 bob
```

**为什么。** 锁外窗口里不变量由占位的凭证来守。凭证（hold id、版本号、代号）是为了让迟到的操作被识别出来。

**易错。** 第一个版本没有任何报错，两个用户都以为自己买到了。
