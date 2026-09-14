---
id: cc-transfer-quant-simulate-vs-closed-form
node: transfer.quant
type: cloze
---
When the closed form is not obvious, simulate: a Monte-Carlo estimate's standard error shrinks like {{c1::1/sqrt(N)}}, so {{c2::10^6}} trials buy roughly {{c3::3}} decimal places. Seed the generator so a surprising result can be re-run, and cross-check the simulation against one case you can compute by hand.

## zh
闭式解不明显时就模拟：蒙特卡洛估计的标准误按 {{c1::1/sqrt(N)}} 缩小，所以 {{c2::10^6}} 次试验大约买到 {{c3::3}} 位小数。给生成器设种子，好让意外结果能重跑；并拿一个你能手算的情形与模拟结果交叉验证。
