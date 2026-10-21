// EXPECTED TO FAIL under ASan: use after free via a dangling string_view.
#include <cstdio>
#include <string>
#include <string_view>
std::string_view first_word(const std::string& s) { return std::string_view(s).substr(0, s.find(' ')); }
int main() {
    std::string_view v;
    {
        std::string line = "AAPL 100 @ 190.5 and a tail long enough to avoid the small-string buffer";
        v = first_word(line);
    }                                           // line destroyed here
    std::printf("%c\n", v[0]);                  // dangling
}
