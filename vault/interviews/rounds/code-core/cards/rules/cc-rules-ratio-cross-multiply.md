---
id: cc-rules-ratio-cross-multiply
node: rules.exact-ratio
type: cloze
---
To test `fraud / total >= num / den` without dividing, cross-multiply into {{c1::`fraud * den >= num * total`}}. The rewrite is order-preserving only while {{c2::both denominators are strictly positive}}, so guard `total > 0` first. Python integers are arbitrary precision, so the products cannot overflow — which is exactly why {{c3::the integer form is both faster and more exact than the float division}}.

## zh
要在不做除法的前提下判断 `fraud / total >= num / den`，交叉相乘成 {{c1::`fraud * den >= num * total`}}。这个改写只在 {{c2::两个分母都严格为正}} 时保序，所以先守卫 `total > 0`。Python 整数是任意精度的，乘积不会溢出 —— 这正是 {{c3::整数写法既更快又比浮点除法更精确}} 的原因。
