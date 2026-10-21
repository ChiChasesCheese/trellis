// Forwarding references and perfect forwarding; emplace vs push.
#include <cstdio>
#include <memory>
#include <string>
#include <utility>
#include <vector>

void sink(const std::string&) { std::printf("  sink(const&)  -> copy\n"); }
void sink(std::string&&) { std::printf("  sink(&&)      -> move\n"); }

template <class T> void wrong(T&& x) { sink(x); }                       // x is an lvalue inside: always the copy overload
template <class T> void right(T&& x) { sink(std::forward<T>(x)); }      // preserves lvalue/rvalue-ness

struct Order {
    static inline int ctor = 0, copy = 0, move = 0;
    std::string sym; int qty;
    Order(std::string s, int q) : sym(std::move(s)), qty(q) { ++ctor; }
    Order(const Order& o) : sym(o.sym), qty(o.qty) { ++copy; }
    Order(Order&& o) noexcept : sym(std::move(o.sym)), qty(o.qty) { ++move; }
};
static void report(const char* t) {
    std::printf("%-26s ctor=%d copy=%d move=%d\n", t, Order::ctor, Order::copy, Order::move);
    Order::ctor = Order::copy = Order::move = 0;
}
template <class T, class... A>                                         // the core of make_unique
std::unique_ptr<T> make(A&&... a) { return std::unique_ptr<T>(new T(std::forward<A>(a)...)); }

int main() {
    std::string s = "AAPL";
    std::printf("wrong(lvalue):\n"); wrong(s);
    std::printf("wrong(rvalue):\n"); wrong(std::string("tmp"));
    std::printf("right(lvalue):\n"); right(s);
    std::printf("right(rvalue):\n"); right(std::string("tmp"));

    std::vector<Order> v; v.reserve(4);
    v.push_back(Order("MSFT", 1));    report("push_back(Order(...))");
    v.emplace_back("MSFT", 1);        report("emplace_back(args...)");
    auto o = make<Order>("NVDA", 5);  report("make<Order>(args...)");
    std::printf("made %s x%d\n", o->sym.c_str(), o->qty);
}
