#include <vector>
template <class C>
auto first(C& c) {
    C::value_type x = c.front();      // dependent name needs `typename`
    return x;
}
int main() { std::vector<int> v{1}; return first(v); }
