// SAN: none
// C12: abstraction cost. Same computation through: virtual call, template (static dispatch), std::variant, std::function.
#include <chrono>
#include <cstdlib>
#include <functional>
#include <iostream>
#include <memory>
#include <random>
#include <variant>
#include <vector>

// [[snip:virtual]]
struct Shape { virtual ~Shape() = default; virtual double area() const = 0; };
struct Sq : Shape { double s; explicit Sq(double x) : s(x) {} double area() const override { return s * s; } };
struct Rect : Shape { double w, h; Rect(double a, double b) : w(a), h(b) {} double area() const override { return w * h; } };
struct Tri : Shape { double b, h; Tri(double x, double y) : b(x), h(y) {} double area() const override { return 0.5 * b * h; } };
// [[/snip]]

// [[snip:variant]]
struct SqV { double s; double area() const { return s * s; } };
struct RectV { double w, h; double area() const { return w * h; } };
struct TriV { double b, h; double area() const { return 0.5 * b * h; } };
using ShapeV = std::variant<SqV, RectV, TriV>;
// [[/snip]]

// [[snip:template]]
template <class S> double total_area(const std::vector<S>& v) { double t = 0; for (const auto& s : v) t += s.area(); return t; }   // resolved at compile time
// [[/snip]]

template <class F>
void bench(const char* name, std::size_t n, int reps, F&& f) {
    double warm = f();
    auto t0 = std::chrono::steady_clock::now();
    double acc = 0;
    for (int r = 0; r < reps; ++r) acc += f();
    auto t1 = std::chrono::steady_clock::now();
    volatile double sink = acc + warm;
    (void)sink;
    std::cout << "  " << name << ": " << std::chrono::duration<double, std::nano>(t1 - t0).count() / reps / static_cast<double>(n) << " ns/shape\n";
}

int main() {
    const std::size_t N = std::getenv("QUICK") ? 20'000 : 2'000'000;
    const int reps = std::getenv("QUICK") ? 2 : 10;
    std::mt19937 rng(3);
    std::vector<std::unique_ptr<Shape>> virt;
    std::vector<ShapeV> var;
    std::vector<SqV> homogeneous;
    std::vector<std::function<double()>> fns;
    for (std::size_t i = 0; i < N; ++i) {
        double a = 1 + static_cast<double>(rng() % 10), b = 1 + static_cast<double>(rng() % 10);
        switch (rng() % 3) {                         // random mix: the virtual call target is unpredictable
            case 0: virt.push_back(std::make_unique<Sq>(a)); var.push_back(SqV{a}); fns.push_back([a] { return a * a; }); break;
            case 1: virt.push_back(std::make_unique<Rect>(a, b)); var.push_back(RectV{a, b}); fns.push_back([a, b] { return a * b; }); break;
            default: virt.push_back(std::make_unique<Tri>(a, b)); var.push_back(TriV{a, b}); fns.push_back([a, b] { return 0.5 * a * b; }); break;
        }
        homogeneous.push_back(SqV{a});
    }
    std::cout << "sum of areas, " << N << " shapes:\n";
    bench("virtual call, random mix   ", N, reps, [&] { double t = 0; for (auto& s : virt) t += s->area(); return t; });
    bench("std::variant + visit       ", N, reps, [&] { double t = 0; for (auto& s : var) t += std::visit([](const auto& x) { return x.area(); }, s); return t; });
    bench("std::function per element  ", N, reps, [&] { double t = 0; for (auto& f : fns) t += f(); return t; });
    bench("template, one concrete type", N, reps, [&] { return total_area(homogeneous); });
}
