#include <cctype>
#include <charconv>
#include <iostream>
#include <string>
#include <string_view>

// Returns true only if the WHOLE token is a base-10 int that fits.
bool strict_int(std::string_view tok, int& out) {
    auto [ptr, ec] = std::from_chars(tok.data(), tok.data() + tok.size(), out);
    return ec == std::errc{} && ptr == tok.data() + tok.size();
}

int main() {
    // std::stoi stops at the first bad character and does not tell you.
    std::cout << "stoi(\"12abc\") = " << std::stoi("12abc") << "\n";
    std::cout << "stoi(\" 7\")    = " << std::stoi(" 7") << "\n";
    std::cout << "stoi(\"+5\")    = " << std::stoi("+5") << "\n";
    try { (void)std::stoi("99999999999"); } catch (const std::out_of_range&) { std::cout << "stoi(\"99999999999\") throws out_of_range\n"; }

    int v = 0;
    for (std::string_view s : {"12", "12abc", " 7", "+5", "-5", "99999999999", ""})
        std::cout << "strict_int(\"" << s << "\") = " << std::boolalpha << strict_int(s, v) << "\n";

    // std::isspace takes an int that must be unsigned-char range or EOF: a plain char >= 0x80 is negative = UB.
    char c = static_cast<char>(0xE9);
    std::cout << "safe: " << (std::isspace(static_cast<unsigned char>(c)) != 0) << "\n";
}
