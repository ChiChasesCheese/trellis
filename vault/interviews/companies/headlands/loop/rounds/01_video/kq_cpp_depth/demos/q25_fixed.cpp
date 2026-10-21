// The fixed versions of the six broken q25_err_*.cpp files, in one translation unit.
#include <cstdio>
#include <string>
#include <vector>

struct Book {                                                   // const-correctness: observers are const
    std::string title;
    void rename(const std::string& t) { title = t; }
    std::size_t length() const { return title.size(); }
};
std::size_t total(const Book& b) { return b.length(); }

void place(std::string sym, int qty, double px) { std::printf("place %s %d @ %.2f\n", sym.c_str(), qty, px); }

template <class C>
auto first(C& c) {
    typename C::value_type x = c.front();                       // dependent type name needs `typename`
    return x;
}

struct Tick { int px; int qty; };                               // semicolon

int sign(int x) {
    if (x > 0) return 1;
    if (x < 0) return -1;
    return 0;                                                   // every path returns
}

int main() {
    std::vector<int> v{1, 2, 3};                                // <vector> included
    long big = 5'000'000'000L;
    int narrowed = static_cast<int>(big);                       // explicit when narrowing is intended
    std::vector<int> w{1, static_cast<int>(2.5)};
    Book b{"Moby Dick"};
    place("AAPL", 100, 190.5);                                  // all three arguments
    v.push_back(7);
    Tick t{1, 2};
    std::printf("%zu %zu %d %d %d %d %d\n", v.size(), total(b), first(v), narrowed, w[1], t.px, sign(0));
}
