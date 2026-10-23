---
id: hl-cq-q40-idioms-oop-collections
node: cpp-questions.j-cross-language
type: qa
step: 5
---
## Q
把这些 Java 习惯翻译成 C++：`interface Shape`、`Shape s = new Rect(3,4)`、`record Point` + `equals` + `compareTo` + `hashCode`、`HashSet<Point>`。

## A
```cpp
struct Shape { virtual ~Shape() = default; virtual double area() const = 0; };   // interface Shape
std::unique_ptr<Shape> s = std::make_unique<Rect>(3, 4);                          // Shape s = new Rect(3,4);

struct Point { int x, y; auto operator<=>(const Point&) const = default; };       // record + equals + compareTo
template <> struct std::hash<Point> { std::size_t operator()(const Point& p) const noexcept { /* ... */ } };   // hashCode
std::unordered_set<Point> seen;                                                   // HashSet<Point>
```
