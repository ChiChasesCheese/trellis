---
id: hl-j08-which-compile-quiz
node: java21.j08-var
type: qa
step: 23
---
## Q
哪些能编译？(a) `var x;` (b) `var y = null;` (c) `var z = new ArrayList<String>();` (d) `var f = () -> 42;` (e) `var a = 1, b = 2;`

## A
**只有 (c) 能编译。**
- (a) 没有初始化器；
- (b) `null` 没有类型；
- (d) lambda 没有目标类型；
- (e) 复合声明不允许。
