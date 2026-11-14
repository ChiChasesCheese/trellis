---
slug: final-prices-with-a-special-discount-in-a-shop
---
## Q
**LC 1475 商品折扣后的最终价格**｜Easy

每件商品 `prices[i]` 减去它右边第一个不超过它的价格，没有就原价，返回最终价格数组。

## A
**一句话。** 下一个更小或相等元素：单调栈存还没找到折扣的下标，新价格不超过栈顶价格时，就是栈顶的折扣。

```python
def final_prices(prices):
    ans = prices[:]
    st = []                     # 价格严格递增的下标
    for i, p in enumerate(prices):
        while st and prices[st[-1]] >= p:
            ans[st.pop()] -= p  # p 是它右边第一个 <= 它的
        st.append(i)
    return ans
```

**复杂度。** 时间 `O(n)`，空间 `O(n)`。

**易错点。**
- 弹栈条件写成 `>`：相等的价格也算折扣，`[10,1,1,6]` 第二个 `1` 要减成 `0`。
- 直接改 `prices` 再比较：后面比较用的是已打折的价格，结果错。

**追问。**
- 从右往左写？：栈里维护右侧候选，弹掉比当前大的，栈顶就是第一个 `<=` 的。
- 为什么 `O(n)`？：每个下标进栈、出栈各一次。

**同模式。** LC 739 每日温度、LC 496 下一个更大元素 I、LC 901 股票价格跨度
