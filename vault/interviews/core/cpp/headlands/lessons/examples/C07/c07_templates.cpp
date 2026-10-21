// C07: templates = compile-time code generation (monomorphisation). Java generics are erased; these are stamped out per type.
#include <iostream>
#include <string>
#include <type_traits>
#include <typeinfo>
#include <utility>
#include <vector>

// [[snip:func]]
template <typename T>
T clamp_to(T v, T lo, T hi) { return v < lo ? lo : (v > hi ? hi : v); }   // one definition, one instance per T used
// [[/snip]]

// [[snip:class]]
template <typename T, std::size_t N>             // non-type parameter: N is a compile-time constant
class RingBuffer {
    T data_[N];                                  // inline storage, sized at compile time: no heap, no pointer
    std::size_t head_ = 0, size_ = 0;
public:
    bool push(const T& v) {
        if (size_ == N) return false;
        data_[(head_ + size_++) % N] = v;
        return true;
    }
    bool pop(T& out) {
        if (size_ == 0) return false;
        out = data_[head_]; head_ = (head_ + 1) % N; --size_;
        return true;
    }
    static constexpr std::size_t capacity() { return N; }
};
// [[/snip]]

// [[snip:variadic]]
template <typename... Ts>
auto sum_all(Ts... xs) { return (xs + ...); }               // fold expression (C++17): ((x1 + x2) + x3) ...

template <typename... Args>
void log_line(const char* tag, Args&&... args) {
    std::cout << "  [" << tag << "]";
    ((std::cout << ' ' << std::forward<Args>(args)), ...);   // fold over the comma operator: print each argument
    std::cout << "\n";
}
// [[/snip]]

// [[snip:iface]]
template <typename T>
std::string describe(const T& v) {
    if constexpr (std::is_integral_v<T>)             // chosen at COMPILE time; the other branches are not even compiled for T
        return "integer " + std::to_string(v);
    else if constexpr (std::is_floating_point_v<T>)
        return "float " + std::to_string(v);
    else
        return "something else: " + std::string(v);  // would be a compile error for int if this were a plain `if`
}
// [[/snip]]

// [[snip:spec]]
template <typename T> struct Name { static const char* get() { return "other"; } };
template <> struct Name<int> { static const char* get() { return "int"; } };          // full specialisation
template <typename T> struct Name<T*> { static const char* get() { return "pointer"; } };   // partial specialisation
// [[/snip]]

int main() {
    std::cout << clamp_to(15, 0, 10) << " " << clamp_to(-2.5, -1.0, 1.0) << " " << clamp_to<long>(3, 5, 9) << "\n";
    RingBuffer<int, 3> rb;
    for (int i = 1; i <= 4; ++i) std::cout << "  push " << i << " -> " << rb.push(i) << "\n";
    int out;
    rb.pop(out);
    std::cout << "  popped " << out << ", capacity " << RingBuffer<int, 3>::capacity() << ", sizeof " << sizeof(RingBuffer<int, 3>) << "\n";
    std::cout << sum_all(1, 2, 3) << " " << sum_all(1.5, 2, 3) << " " << sum_all(std::string("a"), std::string("b")) << "\n";
    log_line("fill", "AAPL", 100, 187.5);
    std::cout << "  " << describe(42) << "; " << describe(2.5) << "; " << describe("hi") << "\n";
    std::cout << "  " << Name<double>::get() << " " << Name<int>::get() << " " << Name<char*>::get() << "\n";
    std::pair p{1, std::string("x")};                       // CTAD (C++17): template arguments deduced from the constructor
    std::vector v{1, 2, 3};
    std::cout << "  CTAD: pair<int,string>=" << (typeid(p) == typeid(std::pair<int, std::string>))
              << " vector<int>=" << (typeid(v) == typeid(std::vector<int>)) << "\n";
}
