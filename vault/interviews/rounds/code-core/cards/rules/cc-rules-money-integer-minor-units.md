---
id: cc-rules-money-integer-minor-units
node: rules.money
type: cloze
---
Money is carried as {{c1::an `int` count of the currency's minor unit}} — cents, pence, yen — from the moment it is parsed to the moment it is rendered. `$12.34` lives in the program as {{c2::1234}}, addition and comparison are exact at any magnitude, and the only decimal point in the program is {{c3::the one the renderer inserts}}. A float anywhere on that path is a defect, not a style choice.

## zh
金钱从解析那一刻到渲染那一刻，始终以 {{c1::该货币最小单位的 `int` 计数}} 形式携带 —— 分、便士、日元。`$12.34` 在程序里就是 {{c2::1234}}，加法和比较在任何量级上都精确，而程序里唯一的小数点是 {{c3::渲染器插入的那一个}}。这条路径上任何位置出现 float 都是缺陷，不是风格选择。
