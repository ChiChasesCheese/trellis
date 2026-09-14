---
id: cc-python-pitfalls-negative-floordiv
node: python.pitfalls
type: cloze
---
In Python `-7 // 2` is {{c1::-4}} — floor, toward minus infinity — and `-7 % 2` is {{c1::1}}, taking the divisor's sign; C, Java, Go and JavaScript truncate toward zero and give {{c2::-3}} and {{c2::-1}}. It bites on hour buckets and on timestamps shifted by a negative offset, where the bucket index quietly moves by one.

## zh
在 Python 里 `-7 // 2` 是 {{c1::-4}} —— 向下取整、朝负无穷 —— 而 `-7 % 2` 是 {{c1::1}}，符号跟着除数；C、Java、Go 和 JavaScript 朝零截断，给出 {{c2::-3}} 和 {{c2::-1}}。它咬人的地方是小时分桶、以及被负偏移平移过的时间戳 —— 桶下标会悄悄错一位。
