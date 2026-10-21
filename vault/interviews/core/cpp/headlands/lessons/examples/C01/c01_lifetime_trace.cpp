// C01: object lifetime made visible. Constructors/destructors print, so scope rules show up in the output.
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>

// [[snip:tracer]]
struct Tracer {
    std::string name;
    explicit Tracer(std::string n) : name(std::move(n)) { std::cout << "  ctor " << name << "\n"; }
    Tracer(const Tracer& o) : name(o.name + "'") { std::cout << "  copy " << o.name << " -> " << name << "\n"; }
    ~Tracer() { std::cout << "  dtor " << name << "\n"; }
};
// [[/snip]]

// [[snip:order]]
struct Holder {
    Tracer first{"member-first"};     // members are built in DECLARATION order ...
    Tracer second{"member-second"};   // ... and destroyed in REVERSE order
    Holder() { std::cout << "  Holder body\n"; }
    ~Holder() { std::cout << "  ~Holder body\n"; }
};

void scope_order() {
    std::cout << "[scope_order]\n";
    Tracer a("a");
    {
        Tracer b("b");
        std::cout << "  inner scope ends\n";
    }                                 // b is destroyed HERE, deterministically (Java: some GC cycle, maybe never)
    Holder h;
    Tracer c("c");
    std::cout << "  function ends\n";
}                                     // destroyed in reverse: c, h (its members reversed), a
// [[/snip]]

// [[snip:unwind]]
void unwinding() {
    std::cout << "[unwinding]\n";
    try {
        Tracer x("x");
        Tracer y("y");
        throw std::runtime_error("boom");   // stack unwinding destroys y, then x
    } catch (const std::exception& e) {
        std::cout << "  caught " << e.what() << "\n";
    }
}
// [[/snip]]

// [[snip:temp]]
void temporaries() {
    std::cout << "[temporaries]\n";
    std::vector<Tracer> v;
    v.reserve(2);
    v.push_back(Tracer("tmp"));       // temporary is built, copied into the vector, destroyed at the ';'
    std::cout << "  after push_back\n";
    const Tracer& r = Tracer("lifetime-extended");   // binding to a const ref extends the temporary's life
    std::cout << "  using " << r.name << "\n";
}
// [[/snip]]

int main() {
    scope_order();
    unwinding();
    temporaries();
}
