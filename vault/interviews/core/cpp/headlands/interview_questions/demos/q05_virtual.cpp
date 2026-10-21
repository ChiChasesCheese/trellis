// Cost model of virtual functions: vptr per object, indirect call, no inlining.
#include <chrono>
#include <cstdio>
#include <memory>
#include <random>
#include <vector>

struct Plain { int x; int get() const { return x; } };
struct Virt  { int x; virtual int get() const { return x; } virtual ~Virt() = default; };

struct Shape { virtual double area() const = 0; virtual ~Shape() = default; };
struct Sq final : Shape { double s; explicit Sq(double v) : s(v) {} double area() const override { return s * s; } };
struct Ci final : Shape { double r; explicit Ci(double v) : r(v) {} double area() const override { return 3.14159 * r * r; } };

// Static polymorphism (CRTP): the base calls the derived function with no vtable.
template <class D> struct ShapeT { double area() const { return static_cast<const D*>(this)->area_impl(); } };
struct SqT : ShapeT<SqT> { double s; explicit SqT(double v) : s(v) {} double area_impl() const { return s * s; } };

double total_virtual(const std::vector<std::unique_ptr<Shape>>& v) {
    double t = 0;
    for (auto& p : v) t += p->area();
    return t;
}
double total_static(const std::vector<SqT>& v) {
    double t = 0;
    for (auto& p : v) t += p.area();
    return t;
}
template <class F> double ms(F&& f) {
    auto t0 = std::chrono::steady_clock::now(); f();
    return std::chrono::duration<double, std::milli>(std::chrono::steady_clock::now() - t0).count();
}
int main() {
    std::printf("sizeof(Plain)=%zu sizeof(Virt)=%zu (an 8-byte vptr, padded to 8-byte alignment)\n", sizeof(Plain), sizeof(Virt));
    std::mt19937 rng(1);
    const int N = 4'000'000;
    std::vector<std::unique_ptr<Shape>> mixed;
    std::vector<SqT> stat;
    for (int i = 0; i < N; ++i) {
        double v = 1.0 + (rng() % 10);
        if (rng() & 1) mixed.push_back(std::make_unique<Sq>(v)); else mixed.push_back(std::make_unique<Ci>(v));
        stat.emplace_back(v);
    }
    volatile double sink = 0;
    double t1 = ms([&] { for (int r = 0; r < 5; ++r) sink = total_virtual(mixed); });
    double t2 = ms([&] { for (int r = 0; r < 5; ++r) sink = total_static(stat); });
    std::printf("virtual, mixed types, boxed : %7.1f ms\n", t1);
    std::printf("CRTP, one type, contiguous  : %7.1f ms\n", t2);
    (void)sink;
}
