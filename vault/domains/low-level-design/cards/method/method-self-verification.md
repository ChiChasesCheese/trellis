---
id: method-self-verification
node: method.evaluation
type: qa
step: 3
---
## Q
为什么要在面试官提问之前自己先跑一遍、验证一遍代码——没有测试框架时怎么做到？

## A
评分表明确给自我验证加分：一个 bug 被你自己先发现是加分项，同一个 bug 被面试官发现是减分项。没有测试框架时最便宜的做法是写一段：

```python
if __name__ == "__main__":
    lot = ParkingLot(spots=2)
    print(lot.park(car))       # 期望：分配成功
    print(lot.park(car2))      # 期望：车位已满，被拒绝
```

在运行之前先说出预期输出，再运行去对照。"先预测、再运行"证明你是在推理代码，而不是碰运气地戳它。
