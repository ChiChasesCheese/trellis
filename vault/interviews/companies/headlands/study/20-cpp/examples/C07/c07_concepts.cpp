// C07: C++20 concepts: name the requirements on template parameters (Java: bounded generics <T extends Comparable<T>>).
#include <concepts>
#include <iostream>
#include <string>
#include <vector>

// [[snip:define]]
template <typename T>
concept Numeric = std::integral<T> || std::floating_point<T>;

template <typename T>
concept HasPrice = requires(const T& t) {              // a requires-expression: "this code must compile"
    { t.price() } -> std::convertible_to<double>;
};
// [[/snip]]

// [[snip:use]]
template <Numeric T>                                    // constrained template parameter
T twice(T x) { return x + x; }

auto triple(Numeric auto x) { return x * 3; }           // abbreviated function template (C++20)

template <typename T>
    requires HasPrice<T>                                // requires-clause
double total(const std::vector<T>& xs) {
    double s = 0;
    for (const auto& x : xs) s += x.price();
    return s;
}

template <typename T>
concept Sortable = std::totally_ordered<T> && std::copyable<T>;

template <Sortable T>
T max_of(const T& a, const T& b) { return a < b ? b : a; }
// [[/snip]]

struct Bond { double p; double price() const { return p; } };
struct Cash { };

// [[snip:overload]]
void print_kind(std::integral auto) { std::cout << "  integral overload\n"; }          // more constrained wins ...
void print_kind(std::floating_point auto) { std::cout << "  floating overload\n"; }
void print_kind(auto) { std::cout << "  generic overload\n"; }
// [[/snip]]

int main() {
    std::cout << twice(21) << " " << twice(1.25) << " " << triple(5) << "\n";
    std::vector<Bond> bonds{{99.5}, {101.25}};
    std::cout << total(bonds) << "\n";
    static_assert(HasPrice<Bond> && !HasPrice<Cash>);
    std::cout << max_of(std::string("abc"), std::string("abd")) << " " << max_of(3, 9) << "\n";
    print_kind(1); print_kind(2.5); print_kind("text");
}
