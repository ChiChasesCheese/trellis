---
id: problems-snake-and-ladder-die-is-a-callable
node: problems.games.snake-and-ladder
type: qa
step: 3
tags: [grown]
---
## Q
蛇梯棋（Snake and Ladder）要能换骰子：公平骰、灌铅骰、测试用的定死序列。流行写法是一个 `DiceRollStrategy` 抽象基类加几个子类，外面再包一个持有策略的 `Dice`。在 Python 里该怎么写，被拒绝的到底是什么？

## A
写成一个函数类型就够了：`Die = Callable[[], int]`，公平骰是一个闭包。

```python
def fair_die(sides: int = 6, rng: random.Random | None = None) -> Die:
    source = rng or random.Random()
    return lambda: source.randint(1, sides)
```

被拒绝的是两样东西，要分开说。**一是 `Dice` 这个壳**：它构造时收一个策略、`roll()` 原样转发，没有自己的职责——一个只转发一次调用的类，要么给它一个职责，要么删掉。**二是抽象基类**：一个只有一个方法、没有共享实现的接口，在 Python 里的载体就是函数类型。

**策略模式（Strategy）本身没有被拒绝**——算法仍然被封装、可替换、调用方不知道拿的是哪一种，变的只是载体。回报很具体：`partial(rng.randint, 1, 6)`、`iter([3, 4, 5]).__next__`、`lambda: 2 * base()` 全都是合法的骰子，一个新类都不用建。只有当这个部件需要暴露可断言的属性时（比如测试骰子的 `rolls_left`），才升级成一个可调用对象。
