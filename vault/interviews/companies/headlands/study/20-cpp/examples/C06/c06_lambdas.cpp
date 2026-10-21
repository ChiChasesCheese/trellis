// C06: lambdas = anonymous function objects. Capture rules, lifetime hazards, std::function cost.
#include <functional>
#include <iostream>
#include <memory>
#include <string>
#include <vector>

// [[snip:captures]]
void captures() {
    int x = 10;
    auto by_val = [x] { return x; };              // copies x at creation: later changes are invisible
    auto by_ref = [&x] { return x; };             // refers to the live x: dangles if the lambda outlives x
    x = 20;
    std::cout << "  by value " << by_val() << ", by reference " << by_ref() << "\n";

    int counter = 0;
    auto inc = [counter]() mutable { return ++counter; };   // mutable: modify the lambda's own copy
    inc(); inc();
    std::cout << "  outer counter still " << counter << ", lambda's copy is at " << inc() << "\n";

    auto owned = std::make_unique<int>(5);
    auto taker = [p = std::move(owned)] { return *p * 2; };  // init-capture (C++14): move-only capture
    std::cout << "  moved-in capture: " << taker() << ", owned is " << (owned ? "set" : "null") << "\n";
}
// [[/snip]]

// [[snip:generic]]
void generic_and_recursion() {
    auto add = [](auto a, auto b) { return a + b; };         // generic lambda (C++14): a template operator()
    std::cout << "  " << add(1, 2) << " " << add(1.5, 2.25) << " " << add(std::string("a"), std::string("b")) << "\n";
    auto fact = [](auto&& self, int n) -> long { return n <= 1 ? 1 : n * self(self, n - 1); };   // recursion without std::function
    std::cout << "  10! = " << fact(fact, 10) << "\n";
    int v = [] { return 6 * 7; }();                          // immediately-invoked: initialise a const with logic
    std::cout << "  IIFE " << v << "\n";
}
// [[/snip]]

// [[snip:cost]]
void what_a_lambda_is() {
    int a = 1, b = 2;
    auto empty = [] { return 1; };
    auto two = [a, b] { return a + b; };
    auto big = [arr = std::vector<int>(100)] { return arr.size(); };
    std::function<int()> f = two;
    std::cout << "  sizeof: empty lambda " << sizeof(empty) << ", [a,b] " << sizeof(two) << ", [vector] " << sizeof(big)
              << ", std::function " << sizeof(f) << "\n";
    // A lambda has its own unique type, so a template parameter or `auto` call inlines it. std::function erases the
    // type behind an indirect call (and may heap-allocate a large capture): use it to STORE callbacks, not in hot loops.
}
// [[/snip]]

// [[snip:dangling]]
std::function<int()> make_counter() {
    int n = 0;
    return [n]() mutable { return ++n; };          // by VALUE: safe to return. [&n] here would dangle (UB).
}
// [[/snip]]

int main() {
    captures();
    generic_and_recursion();
    what_a_lambda_is();
    auto c = make_counter();
    c(); c();
    std::cout << "  returned counter: " << c() << "\n";
}
