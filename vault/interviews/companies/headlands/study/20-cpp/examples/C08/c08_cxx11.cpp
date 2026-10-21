// STD: c++11
// C++11 (the "modern C++" release). Compiled with -std=c++11 by build_all.sh so nothing newer sneaks in.
#include <array>
#include <atomic>
#include <chrono>
#include <iostream>
#include <memory>
#include <mutex>
#include <string>
#include <thread>
#include <tuple>
#include <unordered_map>
#include <utility>
#include <vector>

// [[snip:types]]
enum class Side : char { Buy, Sell };                  // scoped enum: no implicit int conversion, no name leakage
using Price = long;                                    // alias declaration (readable typedef, and can be templated)
template <class T> using Vec = std::vector<T>;         // alias TEMPLATE: impossible with typedef

struct Base { virtual ~Base() = default; virtual int f() const { return 1; } };
struct Derived final : Base {                          // final: no further subclassing
    int f() const override { return 2; }               // override: compile error if it does not really override
};
struct NoCopy { NoCopy() = default; NoCopy(const NoCopy&) = delete; };   // = delete / = default
// [[/snip]]

// [[snip:variadic]]
template <typename T> T sum() { return T(); }
template <typename T, typename... Rest> T sum(T first, Rest... rest) { return first + sum<T>(rest...); }   // variadic templates
// [[/snip]]

// [[snip:udl]]
constexpr long long operator""_k(unsigned long long v) { return static_cast<long long>(v) * 1000; }      // user-defined literal
// [[/snip]]

int main() {
    // [[snip:core]]
    auto n = 42;                                        // auto: type deduction for variables
    std::vector<int> v{1, 2, 3};                        // uniform / brace initialisation, std::initializer_list
    for (int x : v) n += x;                             // range-based for
    int* p = nullptr;                                   // nullptr: a real null pointer type (was 0 / NULL)
    static_assert(sizeof(int) >= 4, "compile-time assertion");
    auto lam = [&n](int k) { return n + k; };           // lambdas
    std::cout << "  n=" << n << " lam(1)=" << lam(1) << " p is " << (p == nullptr ? "null" : "set") << "\n";
    // [[/snip]]

    // [[snip:move]]
    std::unique_ptr<int> up(new int(5));                // unique_ptr/shared_ptr/weak_ptr arrive; auto_ptr is deprecated
    std::unique_ptr<int> up2 = std::move(up);           // rvalue references + std::move: move semantics
    std::shared_ptr<std::string> sp = std::make_shared<std::string>("shared");
    std::cout << "  moved ptr " << *up2 << ", shared " << *sp << " use_count " << sp.use_count() << "\n";
    // [[/snip]]

    // [[snip:lib]]
    std::unordered_map<std::string, int> m{{"a", 1}, {"b", 2}};   // hash containers
    std::array<int, 3> arr{{7, 8, 9}};                            // std::array
    std::tuple<int, std::string> tup(1, "x");                     // std::tuple, std::tie
    int one; std::string x;
    std::tie(one, x) = tup;
    std::cout << "  m[b]=" << m["b"] << " arr[2]=" << arr[2] << " tuple " << one << x << "\n";
    // [[/snip]]

    // [[snip:conc]]
    std::atomic<int> hits(0);                           // a memory model + std::thread, mutex, atomic, condition_variable
    std::mutex mu;
    int guarded = 0;
    std::vector<std::thread> ts;
    for (int i = 0; i < 4; ++i)
        ts.push_back(std::thread([&] { for (int j = 0; j < 1000; ++j) { ++hits; std::lock_guard<std::mutex> g(mu); ++guarded; } }));
    for (auto& t : ts) t.join();
    std::cout << "  threads: atomic=" << hits.load() << " guarded=" << guarded << "\n";
    auto t0 = std::chrono::steady_clock::now();            // <chrono>
    std::cout << "  chrono ok: " << (std::chrono::steady_clock::now() >= t0) << "\n";
    // [[/snip]]

    Derived d;
    Base& b = d;
    NoCopy nc; (void)nc;
    std::cout << "  override: " << b.f() << " sum: " << sum(1, 2, 3) << " literal: " << 5_k << " side: " << static_cast<int>(Side::Sell)
              << " raw: " << R"(C:\no\escape)" << "\n";
    Vec<Price> prices{1, 2};
    std::cout << "  alias template size " << prices.size() << "\n";
}
