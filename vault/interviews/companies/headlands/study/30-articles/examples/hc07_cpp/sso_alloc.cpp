// Short std::strings live inside the string object (small-string optimisation): no heap allocation.
// A std::string_view parameter avoids the temporary std::string a `const std::string&` parameter would need.
#include <cstdlib>
#include <iostream>
#include <new>
#include <string>
#include <string_view>

static std::size_t g_news = 0;
void* operator new(std::size_t n) {
    ++g_news;
    if (void* p = std::malloc(n ? n : 1)) return p;
    throw std::bad_alloc();
}
void operator delete(void* p) noexcept { std::free(p); }
void operator delete(void* p, std::size_t) noexcept { std::free(p); }

std::size_t length_by_ref(const std::string& s) { return s.size(); }
std::size_t length_by_view(std::string_view s) { return s.size(); }

int main() {
    std::size_t before = g_news;
    { std::string ticker("AAPL"); (void)ticker; }
    std::cout << "std::string(\"AAPL\"):             " << g_news - before << " allocations\n";

    before = g_news;
    { std::string long_key(40, 'X'); (void)long_key; }
    std::cout << "std::string of 40 characters:    " << g_news - before << " allocation\n";

    const char* literal = "this literal is longer than the small buffer of a std::string";
    before = g_news;
    (void)length_by_ref(literal);  // builds a temporary std::string from the literal
    std::cout << "const std::string& parameter:    " << g_news - before << " allocation\n";
    before = g_news;
    (void)length_by_view(literal);
    std::cout << "std::string_view parameter:      " << g_news - before << " allocations\n";
}
