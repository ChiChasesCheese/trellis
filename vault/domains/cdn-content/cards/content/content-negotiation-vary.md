---
id: content-negotiation-vary
node: content.negotiation
type: qa
---
## Q
The origin chooses AVIF or JPEG from `Accept`, but sends no `Vary`. What cache failure follows?

## A
The shared cache may store the first representation under one URL and serve it to clients that did not advertise support. Emit `Vary: Accept` or make the selected format an explicit URL/key dimension, and ensure `Content-Type` matches the bytes. Normalize capability selection to a small supported set; keying on the raw `Accept` header can explode cardinality.

## Q zh
origin 根据 `Accept` 选择 AVIF 或 JPEG，却没有发送 `Vary`。会出现什么 cache failure？

## A zh
shared cache 可能把第一个 representation 存在该 URL 下，再发给没有声明支持的 client。应发送 `Vary: Accept`，或把 selected format 变成显式 URL/key dimension，并确保 `Content-Type` 与 bytes 匹配。capability selection 要 normalize 到小型支持集合；直接按 raw `Accept` header 建 key 会导致 cardinality explosion。
