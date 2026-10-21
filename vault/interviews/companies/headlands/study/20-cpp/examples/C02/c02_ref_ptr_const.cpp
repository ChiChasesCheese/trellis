// C02: references vs pointers vs const. Every Java "reference" maps to one of these three things in C++.
#include <iostream>
#include <string>
#include <vector>

// [[snip:params]]
struct Big { std::vector<int> data = std::vector<int>(1000, 1); };

void by_value(Big b)         { b.data[0] = 42; }                // copies 4000+ bytes; caller unaffected
void by_ref(Big& b)          { b.data[0] = 42; }                // aliases the caller's object; may mutate
void by_const_ref(const Big& b) { std::cout << "  size=" << b.data.size() << "\n"; }   // read only, no copy
void by_ptr(Big* b)          { if (b) b->data[0] = 43; }        // may be null; reseatable; needs ->
// [[/snip]]

// [[snip:constpos]]
void const_positions() {
    int x = 1, y = 2;
    const int* p1 = &x;        // pointer to const int: *p1 = 5 is an error, p1 = &y is fine
    int* const p2 = &x;        // const pointer to int: *p2 = 5 is fine, p2 = &y is an error
    const int* const p3 = &x;  // neither can change
    p1 = &y;
    *p2 = 5;
    std::cout << "  *p1=" << *p1 << " *p2=" << *p2 << " *p3=" << *p3 << "\n";
    // Read declarations right-to-left: "p2 is a const pointer to int".
}
// [[/snip]]

// [[snip:constmember]]
class Counter {
    int n_ = 0;
    mutable int reads_ = 0;               // mutable: bookkeeping that does not change the logical value
public:
    void inc() { ++n_; }
    int get() const { ++reads_; return n_; }   // const member function: promises not to change *this
    int reads() const { return reads_; }
};

void use_const(const Counter& c) {
    // c.inc();                          // would not compile: inc() is not const
    std::cout << "  get=" << c.get() << " reads=" << c.reads() << "\n";
}
// [[/snip]]

// [[snip:ref_rules]]
void reference_rules() {
    int a = 1, b = 2;
    int& r = a;          // must be initialised; there is no "null reference"
    r = b;               // NOT rebinding: this assigns b's value to a
    std::cout << "  a=" << a << " b=" << b << " (r still names a)\n";

    std::vector<int> v{1, 2, 3};
    for (auto& e : v) e *= 2;                    // auto& : mutate in place
    long scratch = 0;
    for (auto e : v) { e *= 100; scratch += e; } // auto  : mutates a copy, v unchanged
    for (const auto& e : v) std::cout << "  " << e;
    std::cout << "  (scratch=" << scratch << ")\n";
}
// [[/snip]]

int main() {
    Big big;
    by_value(big);       std::cout << "after by_value  data[0]=" << big.data[0] << "\n";
    by_ref(big);         std::cout << "after by_ref    data[0]=" << big.data[0] << "\n";
    by_ptr(&big);        std::cout << "after by_ptr    data[0]=" << big.data[0] << "\n";
    by_ptr(nullptr);
    by_const_ref(big);
    std::cout << "sizeof(Big)=" << sizeof(Big) << " sizeof(Big*)=" << sizeof(Big*) << "\n";
    const_positions();
    Counter c; c.inc(); use_const(c);
    reference_rules();
}
