---
id: hl-cq-q40-idioms-resources-streams
node: cpp-questions.j-cross-language
type: qa
step: 6
---
## Q
把这些 Java 习惯翻译成 C++：try-with-resources、`map.merge(w, 1, Integer::sum)`、`TreeMap`、`Optional<Integer>`、`stream().filter`、`synchronized`。

## A
```cpp
{ Resource r; /* use */ }                                       // try (var r = new Resource()) {}
std::unordered_map<std::string, int> counts;  counts[w]++;      // map.merge(w, 1, Integer::sum)
std::map<std::string, int> sorted(counts.begin(), counts.end()); // TreeMap
std::optional<int> idx = find_index(names, "y");  idx.value_or(-1);   // Optional<Integer>
auto evens = std::views::iota(1, 10)
           | std::views::filter([](int i) { return i % 2 == 0; });    // stream().filter
{ std::lock_guard g(m); ++n; }                                  // synchronized
```
