// C01: two lifetime surprises: a constructor that throws, and slicing (copying a derived object into a base object).
#include <iostream>
#include <memory>
#include <stdexcept>
#include <string>

// [[snip:ctor]]
struct Part {
    std::string n;
    explicit Part(std::string name) : n(std::move(name)) { std::cout << "  Part " << n << " built\n"; }
    ~Part() { std::cout << "  Part " << n << " destroyed\n"; }
};

struct Machine {
    Part a{"a"};
    Part b{"b"};
    Machine(bool fail) {
        std::cout << "  Machine body starts\n";
        if (fail) throw std::runtime_error("constructor failed");
    }
    ~Machine() { std::cout << "  ~Machine runs\n"; }
};
// [[/snip]]

// [[snip:slice]]
struct Animal { virtual std::string name() const { return "animal"; } virtual ~Animal() = default; };
struct Dog : Animal { std::string name() const override { return "dog"; } int tricks = 3; };

std::string by_value(Animal a) { return a.name(); }          // copies only the Animal part: Dog is "sliced" off
std::string by_ref(const Animal& a) { return a.name(); }     // no copy: virtual dispatch works
// [[/snip]]

int main() {
    std::cout << "[constructor throws]\n";
    try { Machine m(true); } catch (const std::exception& e) { std::cout << "  caught: " << e.what() << "\n"; }

    std::cout << "[slicing]\n";
    Dog d;
    std::cout << "  by_value: " << by_value(d) << ", by_ref: " << by_ref(d) << "\n";
    std::unique_ptr<Animal> p = std::make_unique<Dog>();
    std::cout << "  through base pointer: " << p->name() << "\n";
}
