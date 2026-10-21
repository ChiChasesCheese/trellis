// Templates are instantiated per type; concepts give readable constraints.
#include <concepts>
#include <cstdio>
#include <string>
#include <type_traits>
#include <vector>

template <class T> T my_max(T a, T b) { return a < b ? b : a; }          // one source, one copy per T
template <class T> struct Box { T v; static constexpr std::size_t bytes = sizeof(T); };

template <class T>
concept Priceable = requires(T t) { { t.price() } -> std::convertible_to<double>; };
struct Bond { double price() const { return 99.5; } };
struct Rock {};

template <Priceable T> double mark(const T& t) { return t.price(); }

// C++11-style SFINAE for the same idea (what concepts replace)
template <class T> auto mark_old(const T& t) -> decltype(t.price()) { return t.price(); }

int main() {
    std::printf("%d %.1f %s\n", my_max(3, 7), my_max(2.5, 1.5), my_max(std::string("ab"), std::string("b")).c_str());
    std::printf("Box<char>::bytes=%zu Box<double>::bytes=%zu (no boxing: T is the real type)\n", Box<char>::bytes, Box<double>::bytes);
    std::printf("mark(Bond)=%.1f mark_old(Bond)=%.1f\n", mark(Bond{}), mark_old(Bond{}));
    std::printf("Priceable<Bond>=%d Priceable<Rock>=%d\n", Priceable<Bond>, Priceable<Rock>);
    static_assert(std::is_same_v<decltype(my_max(1, 2)), int>);
}
