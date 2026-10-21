// Java idioms and their C++ spellings, in one compiling file.
#include <algorithm>
#include <compare>
#include <cstdio>
#include <functional>
#include <map>
#include <memory>
#include <mutex>
#include <optional>
#include <ranges>
#include <string>
#include <unordered_map>
#include <unordered_set>
#include <vector>

// interface Shape { double area(); }          ->  abstract class with a virtual destructor
struct Shape { virtual ~Shape() = default; virtual double area() const = 0; };
struct Rect : Shape { double w, h; Rect(double w_, double h_) : w(w_), h(h_) {} double area() const override { return w * h; } };

// record Point(int x, int y) + equals/hashCode/compareTo   ->  one struct, defaulted operators, a std::hash
struct Point {
    int x, y;
    auto operator<=>(const Point&) const = default;       // compareTo + equals
};
template <> struct std::hash<Point> {                      // hashCode
    std::size_t operator()(const Point& p) const noexcept { return std::hash<long long>{}((static_cast<long long>(p.x) << 32) ^ static_cast<unsigned>(p.y)); }
};

// try (var r = new Resource()) { ... }          ->  a scope and a destructor
struct Resource { Resource() { std::printf("  acquire\n"); } ~Resource() { std::printf("  release\n"); } };

// synchronized (this) { ... }                   ->  lock_guard
struct Counter { std::mutex m; int n = 0; void inc() { std::lock_guard g(m); ++n; } };

// Optional<Integer> find(...)                   ->  std::optional<int>
std::optional<int> find_index(const std::vector<std::string>& v, const std::string& s) {
    auto it = std::find(v.begin(), v.end(), s);
    if (it == v.end()) return std::nullopt;
    return static_cast<int>(it - v.begin());
}

int main() {
    std::unique_ptr<Shape> s = std::make_unique<Rect>(3, 4);                     // Shape s = new Rect(3,4);
    std::printf("area = %.1f\n", s->area());

    std::unordered_set<Point> seen{{1, 2}, {3, 4}};                              // HashSet<Point>
    std::printf("contains {3,4}: %d, {5,6}: %d, {1,2}<{1,3}: %d\n", seen.contains({3, 4}), seen.contains({5, 6}), Point{1, 2} < Point{1, 3});

    { Resource r; std::printf("  using resource\n"); }                            // try-with-resources

    std::unordered_map<std::string, int> counts;                                 // HashMap<String,Integer>
    for (const char* w : {"a", "b", "a", "c", "a"}) counts[w]++;                 // merge(w, 1, Integer::sum)
    std::map<std::string, int> sorted(counts.begin(), counts.end());             // TreeMap
    for (auto& [k, v] : sorted) std::printf("%s=%d ", k.c_str(), v);
    std::printf("\n");

    std::vector<std::string> names{"x", "y", "z"};                               // ArrayList<String>
    auto idx = find_index(names, "y");
    std::printf("index of y: %d, of q: %s\n", idx.value_or(-1), find_index(names, "q") ? "found" : "empty");

    auto evens = std::views::iota(1, 10) | std::views::filter([](int i) { return i % 2 == 0; });   // stream().filter
    int total = 0; for (int e : evens) total += e;
    std::printf("sum of evens = %d\n", total);

    std::function<int(int)> add2 = [](int x) { return x + 2; };                  // Function<Integer,Integer>
    Counter c; c.inc(); c.inc();
    std::printf("add2(5)=%d counter=%d\n", add2(5), c.n);
}
