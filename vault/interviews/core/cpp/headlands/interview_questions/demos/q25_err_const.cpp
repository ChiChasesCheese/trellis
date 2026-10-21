#include <string>
struct Book {
    std::string title;
    void rename(const std::string& t) { title = t; }
    std::size_t length() { return title.size(); }          // forgot const
};
std::size_t total(const Book& b) { return b.length(); }    // const ref calls non-const member
int main() { Book b; return static_cast<int>(total(b)); }
