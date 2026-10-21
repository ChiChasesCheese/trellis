// C03: unique_ptr = sole ownership, zero overhead. Also: where a raw pointer is still the right tool.
#include <cstdio>
#include <iostream>
#include <memory>
#include <string>
#include <utility>
#include <vector>

struct Order {
    int id;
    explicit Order(int i) : id(i) { std::cout << "  Order " << id << " created\n"; }
    ~Order() { std::cout << "  Order " << id << " destroyed\n"; }
};

// [[snip:factory]]
std::unique_ptr<Order> make_order(int id) {          // returning transfers ownership to the caller
    return std::make_unique<Order>(id);              // make_unique: one expression, exception safe
}

void inspect(const Order* o) {                       // raw pointer = "borrowing, I do not own it, may be null"
    std::cout << "  inspecting " << (o ? o->id : -1) << "\n";
}
void inspect_ref(const Order& o) { std::cout << "  inspecting ref " << o.id << "\n"; }   // better: cannot be null
void consume(std::unique_ptr<Order> o) {             // by value = "I take ownership"
    std::cout << "  consuming " << o->id << "\n";
}                                                    // destroyed here
// [[/snip]]

// [[snip:overhead]]
void sizes() {
    std::cout << "  sizeof(Order*)=" << sizeof(Order*) << " sizeof(unique_ptr<Order>)=" << sizeof(std::unique_ptr<Order>)
              << " sizeof(shared_ptr<Order>)=" << sizeof(std::shared_ptr<Order>) << "\n";
}
// [[/snip]]

// [[snip:deleter]]
struct FileCloser { void operator()(std::FILE* f) const { if (f) std::fclose(f); } };
using FilePtr = std::unique_ptr<std::FILE, FileCloser>;   // custom deleter in the type: still pointer-sized
// [[/snip]]

// [[snip:poly]]
struct Shape { virtual ~Shape() = default; virtual double area() const = 0; };   // virtual dtor is REQUIRED
struct Sq : Shape { double s; explicit Sq(double x) : s(x) {} double area() const override { return s * s; } };
struct Circ : Shape { double r; explicit Circ(double x) : r(x) {} double area() const override { return 3.14159 * r * r; } };
// [[/snip]]

int main() {
    std::cout << "[ownership]\n";
    auto a = make_order(1);
    inspect(a.get());            // get() hands out the raw pointer; the unique_ptr keeps ownership
    inspect_ref(*a);
    // auto b = a;               // does not compile: copying would mean two owners
    auto b = std::move(a);       // ownership moves; a is now empty
    std::cout << "  a is " << (a ? "full" : "null") << ", b->id=" << b->id << "\n";
    consume(std::move(b));
    std::cout << "[after consume]\n";

    std::cout << "[container of owners]\n";
    std::vector<std::unique_ptr<Order>> v;
    v.push_back(make_order(10));
    v.push_back(make_order(11));
    v.erase(v.begin());          // destroys Order 10
    std::cout << "  left: " << v.size() << "\n";

    std::cout << "[sizes]\n";
    sizes();

    std::cout << "[custom deleter]\n";
    FilePtr f(std::fopen("/tmp/c03_demo.txt", "w"));
    std::fputs("x", f.get());

    std::cout << "[polymorphism]\n";
    std::vector<std::unique_ptr<Shape>> shapes;
    shapes.push_back(std::make_unique<Sq>(2));
    shapes.push_back(std::make_unique<Circ>(1));
    double total = 0;
    for (const auto& s : shapes) total += s->area();
    std::cout << "  total area " << total << "\n";
    std::cout << "[end of main]\n";
}
