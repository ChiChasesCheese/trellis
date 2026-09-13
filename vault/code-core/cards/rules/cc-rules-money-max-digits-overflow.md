---
id: cc-rules-money-max-digits-overflow
node: rules.money
type: qa
tags: [grown]
---
## Q
A card network's API limits a charge `amount` field to 12 digits of minor units, capping a single USD charge at $9,999,999,999.99. Your own database stores amounts in a 64-bit `int` column, which can hold numbers far larger than that without overflowing. Why does the money field still need an explicit maximum-value check?

## A
The integer type's range and the field's valid range are two different guarantees: a 64-bit `int` will happily store a number ten orders of magnitude past what any payment network will accept, so nothing about the storage type stops a bad calculation — a fee applied twice, a batch total, a corrupted import — from producing an amount the network rejects or truncates unexpectedly. 'Fits in the variable' says only that the bits don't overflow; 'valid as an amount' is a domain rule about what a real charge can be, and it has to be enforced with its own explicit bound check, independent of how large the underlying integer type happens to allow.

## Q zh
某银行卡网络的 API 把 charge 的 `amount` 字段限制在 12 位数的 minor unit 以内，单笔 USD charge 的上限因此是 $9,999,999,999.99。而你自己的数据库用一个 64 位的 `int` 列存储金额，它能存下比这大得多的数字而不会溢出。为什么金额字段仍然需要一个显式的最大值检查？

## A zh
整数类型的取值范围和这个字段的合法取值范围，是两种不同的保证：一个 64 位的 `int` 完全可以轻松存下比任何支付网络能接受的数字大十个数量级的值，所以存储类型本身完全不能阻止一次错误的计算——一笔手续费被算了两遍、一个批次的汇总、一次损坏的数据导入——产出一个会被网络拒绝或意外截断的金额。"能存进这个变量"只说明比特位不会溢出；"作为一个金额是合法的"是一条关于真实 charge 能是什么样子的领域规则，必须用它自己显式的边界检查来强制执行，跟底层整数类型实际能容纳多大的数字无关。
