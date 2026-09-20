---
nodes: [problems.marketplaces.ride-sharing]
url: https://docs.python.org/3/library/fractions.html
---
# Python 文档：fractions —— Rational numbers

值得读：网约车的动态加价倍数必须参与金额运算，而 `1.2` 在二进制里并不是 `1.2`。
`Fraction(6, 5)` 是精确有理数，乘以整数分仍然精确，于是整套计价里只有最后 `int()` 那一处取整，
"明细相加 × 倍数 == 实付"这条等式在任何输入下都成立。文档里值得注意的两点：`Fraction` 之间的
比较是精确的（所以 `demand_surge` 里 `ratio >= threshold` 不会有边界抖动），以及
`Fraction(0.1)` 会忠实地把 float 的误差带进来——所以倍数要从整数对构造，不要从 float 构造。
配套要读的是[`threading`](https://docs.python.org/3/library/threading.html)：本题解的
`DriverPool` 靠 `Lock` 把"判断空闲"和"写入占用"合成一次原子操作，测试则用 `Barrier` 让
二十个线程同时起跑；这两件事 GIL 都不负责。
