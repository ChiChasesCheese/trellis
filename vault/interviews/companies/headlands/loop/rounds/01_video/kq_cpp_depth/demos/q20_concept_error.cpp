// EXPECTED TO FAIL: the constraint is checked at the call site.
#include <concepts>
template <class T>
concept Priceable = requires(T t) { { t.price() } -> std::convertible_to<double>; };
template <Priceable T> double mark(const T& t) { return t.price(); }
struct Rock {};
int main() { return static_cast<int>(mark(Rock{})); }
