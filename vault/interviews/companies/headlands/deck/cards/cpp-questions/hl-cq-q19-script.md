---
id: hl-cq-q19-script
node: cpp-questions.d-containers
type: qa
step: 17
---
## Q
用英文 60 秒回答：How do you erase elements from a container correctly? (erase-remove idiom, erase in a loop, `std::erase_if`)

## A
结构：`remove_if` 只前移不缩容（6 变 3）→ 循环里用 `erase` 返回的迭代器，C++20 `erase_if` → 顺序无关用 swap-and-pop → 绝不在 range-for 里删。

- `std::remove_if` doesn't shrink the container; it moves the elements to keep to the front and returns the new logical end. You must follow it with `erase` - the **erase-remove idiom**. In my test the size stayed 6 after `remove_if` and became 3 after `erase`.
- In a loop I use the iterator that `erase` returns instead of incrementing the invalidated one. In C++20 it's simply `std::erase_if(container, pred)`, which also returns the count.
- If order doesn't matter I **swap with the last element and pop**, which is O(1) instead of O(n).
- And I never erase inside a range-for - the iterator is invalidated.
