// EXPECT: compile-fail
// C07: the payoff of concepts: the error names the violated requirement instead of 80 lines of template internals.
#include <concepts>
#include <string>

template <typename T>
concept Numeric = std::integral<T> || std::floating_point<T>;

template <Numeric T>
T twice(T x) { return x + x; }

int main() {
    return twice(std::string("oops")).size();      // std::string is not Numeric
}
