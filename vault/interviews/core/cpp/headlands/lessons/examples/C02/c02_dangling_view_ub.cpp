// EXPECT: run-fail
// C02: the hazard of views. The view outlives the string it points into: use-after-free that Java cannot have.
#include <iostream>
#include <string>
#include <string_view>

std::string make_name() { return std::string(64, 'x') + " (a name too long for the small-string buffer)"; }

int main() {
    std::string_view sv = make_name();   // the temporary std::string dies at the ';' -> sv dangles
    std::cout << sv.size() << "\n";      // reads freed heap memory: AddressSanitizer stops us
    std::cout << sv[0] << "\n";
}
