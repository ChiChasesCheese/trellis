---
id: hi-lld-amazon-locker-7-pickup
node: lld.problem-breakdowns.amazon-locker
type: qa
step: 7
---
## Q
**取件方法与错误语义**｜低层设计 · 题目拆解

请写出快递柜 pickup 的逻辑，说明不同失败情形给用户什么错误，为什么“已用过”和“从未存在”用同一个报错，过期的码为什么不从表里删除。

## A
```python
def pickup(self, token_code: str) -> None:
    if not token_code:
        raise Exception("Invalid access token code")
    token = self.access_token_mapping.get(token_code)
    if token is None:   # 不存在或已被取走
        raise Exception("Invalid access token code")
    if token.is_expired():
        raise Exception("Access token has expired")
    token.get_compartment().open()
    self._clear_deposit(token)  # 释放格口并删码
```

**错误区分。** 取走时码被删除，之后再用它与随便输的码毫无区别，统一提示“无效”；要区分“已使用”得另记已用集合或标志，收益太小。过期的错误单独提示，因为用户能据此联系客服处理仍在柜里的包裹。

**为什么不删过期码。** 包裹还留在格口里，要等员工取走才算释放；码留在表里，才能提示过期，也才能让 `open_expired_compartments` 找到它们。

**易错。** `_clear_deposit` 要同时做两件事：格口标记空闲、码从表里移除。漏掉一步就会出现状态不一致。
