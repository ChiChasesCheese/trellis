// C++ objects are values: assignment copies, references alias, slicing cuts.
#include <cstdio>
#include <string>
#include <vector>

struct Order {
    std::string sym; int qty;
    static inline int copies = 0;
    Order(std::string s, int q) : sym(std::move(s)), qty(q) {}
    Order(const Order& o) : sym(o.sym), qty(o.qty) { ++copies; }
    Order& operator=(const Order& o) = default;
};
struct Animal { virtual std::string name() const { return "animal"; } virtual ~Animal() = default; };
struct Dog : Animal { std::string tag = "extra-data"; std::string name() const override { return "dog"; } };

void by_value(Order o)        { o.qty = -1; }
void by_ref(Order& o)         { o.qty = -2; }
void by_const_ref(const Order& o) { std::printf("  read-only qty=%d\n", o.qty); }
void by_pointer(Order* o)     { if (o) o->qty = -3; }

int main() {
    Order a("AAPL", 100);
    Order b = a;                 // Java: b is another name for the same object. C++: b is a NEW object.
    b.qty = 5;
    std::printf("a.qty=%d b.qty=%d (copies so far: %d)\n", a.qty, b.qty, Order::copies);

    Order& alias = a;            // THIS is the Java-like thing
    alias.qty = 7;
    std::printf("a.qty=%d after writing through a reference\n", a.qty);

    int before = Order::copies;
    by_value(a);      std::printf("by_value  -> a.qty=%d, copies +%d\n", a.qty, Order::copies - before);
    by_ref(a);        std::printf("by_ref    -> a.qty=%d\n", a.qty);
    by_const_ref(a);
    by_pointer(&a);   std::printf("by_pointer-> a.qty=%d\n", a.qty);

    std::vector<Order> v1{a, b};
    auto v2 = v1;                // deep copy of every element
    v2[0].qty = 999;
    std::printf("vector copy is deep: v1[0].qty=%d v2[0].qty=%d\n", v1[0].qty, v2[0].qty);

    Dog d;
    Animal sliced = d;           // copies only the Animal part: the Dog is cut off
    Animal& ref = d;
    std::printf("slicing: by value name()=%s, by reference name()=%s\n", sliced.name().c_str(), ref.name().c_str());

    std::vector<Animal> bad; bad.push_back(d);          // slicing again - use vector<unique_ptr<Animal>>
    std::printf("vector<Animal>[0].name() = %s\n", bad[0].name().c_str());
}
