---
id: quality-null-returns
node: quality.errors
type: qa
step: 4
---
## Q
```python
def get(self, key, default=None):
    return self._data.get(key, default)
```
如果字典里某个 key 对应的合法值本来就是 `None`，调用方用 `if store.get(key) is None` 判断"不存在"会出什么问题？

## A
`None` 同时被用来表示两件不同的事——"这个 key 不存在"和"这个 key 存在，值恰好是 `None`"——调用方没法区分,于是把一个合法值误判成了缺失。这不是异常处理问题，是把"缺失"这个信号叠加在了"合法值可能取到的范围"里，是 `None` 作哨兵值最常见的坑。

```python
_MISSING = object()

def get(self, key, default=_MISSING):
    value = self._data.get(key, _MISSING)
    if value is _MISSING:
        return default
    return value
```
修法是用一个只在这一处使用、和任何合法值都不可能相等的哨兵对象（`object()` 的一个实例）来表示"缺失"，而不是复用一个本身也是合法值的 `None`。如果调用方确实需要区分"不存在"和"存在但是 `None`"这两种情况,签名上也应该显式表达出来,而不是留给调用方自己猜。
