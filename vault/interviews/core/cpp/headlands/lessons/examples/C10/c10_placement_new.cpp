// C10: placement new separates "get memory" from "construct an object". It is how vector, optional, and pools work.
#include <cstddef>
#include <iostream>
#include <memory>
#include <new>
#include <string>

struct Order {
    long id; std::string sym;
    Order(long i, std::string s) : id(i), sym(std::move(s)) { std::cout << "  construct " << id << "\n"; }
    ~Order() { std::cout << "  destroy " << id << "\n"; }
};

// [[snip:slot]]
class Slot {                                         // a minimal std::optional<Order>
    alignas(Order) unsigned char storage_[sizeof(Order)];   // raw, correctly aligned bytes
    bool live_ = false;
public:
    template <class... A> Order& emplace(A&&... a) {
        Order* p = new (storage_) Order(std::forward<A>(a)...);   // placement new: construct AT this address, no allocation
        live_ = true;
        return *p;
    }
    void reset() {
        if (live_) { std::launder(reinterpret_cast<Order*>(storage_))->~Order(); live_ = false; }   // call the destructor by hand
    }
    Order& get() { return *std::launder(reinterpret_cast<Order*>(storage_)); }
    ~Slot() { reset(); }
};
// [[/snip]]

int main() {
    std::cout << "[slot]\n";
    Slot s;
    s.emplace(1L, "AAPL");
    std::cout << "  " << s.get().sym << "\n";
    s.reset();
    s.emplace(2L, "MSFT");                           // the same bytes, reused for a different object
    std::cout << "[uninitialized_* algorithms and construct_at]\n";
    alignas(Order) unsigned char buf[3 * sizeof(Order)];
    Order* base = reinterpret_cast<Order*>(buf);
    std::construct_at(base, 10L, "A");               // C++20 spelling of placement new
    std::construct_at(base + 1, 11L, "B");
    std::destroy_at(base + 1);                       // spelling of p->~Order()
    std::destroy_at(base);
    std::cout << "  alignof(Order)=" << alignof(Order) << " sizeof(Order)=" << sizeof(Order) << "\n";
}
