---
id: cc-rules-money-json-int-precision
node: rules.money
type: qa
tags: [grown]
---
## Q
A payments API returns a charge as a JSON number — `{"amount": 19.99}` — instead of an integer count of cents. A client decodes this JSON in a language whose decoder turns every JSON number into an IEEE-754 double. What can go wrong, and why does sending an integer instead fix it?

## A
The JSON spec makes no promise that a decimal fraction like `19.99` survives decoding exactly; once it becomes a double, it inherits the same binary-fraction rounding behind `0.1 + 0.2 != 0.3`, in every language whose default decoder produces floats (JavaScript's `Number`, Python's `json` module). The client can end up holding a value that is not exactly 19.99. An integer such as `1999` (cents) has no fraction to approximate: a double represents every integer up to 2^53 (9,007,199,254,740,992) exactly, so the amount round-trips through JSON and back with zero error. The wire format has to obey the same 'no floats near money' rule as the in-process representation, not just the code that computes with it.

## Q zh
一个支付 API 把一笔charge 以 JSON number 的形式返回——`{"amount": 19.99}`——而不是以分为单位的整数。client 用一种把每个 JSON number 都解码成 IEEE-754 double 的语言来解析这段 JSON。这会出什么问题？为什么改成发送整数就能解决？

## A zh
JSON 规范并不保证像 `19.99` 这样的小数在解码时能被精确保留；一旦它变成 double，就会继承 `0.1 + 0.2 != 0.3` 背后同样的二进制小数舍入问题——在任何默认解码器产出 float 的语言里都是如此（JavaScript 的 `Number`、Python 的 `json` 模块）。client 最终拿到的值可能并不恰好等于 19.99。而像 `1999`（分）这样的整数没有小数需要近似：double 能精确表示直到 2^53（9,007,199,254,740,992）为止的每一个整数，所以这个金额经过 JSON 往返也不会有任何误差。传输格式必须遵守和进程内表示同样的"金钱附近不出现 float"规则，而不只是计算它的那部分代码要遵守。
