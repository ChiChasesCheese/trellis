// A string_view into a std::vector<std::string> element goes stale when the vector reallocates and the strings move (short
// strings keep their characters INSIDE the std::string object).  The program only compares addresses; it never reads through
// a stale view.
#include <iostream>
#include <string>
#include <string_view>
#include <vector>

int main() {
    std::vector<std::string> names;
    names.reserve(1);
    names.push_back("AAPL");  // short string: characters live inside the std::string object
    const std::string_view view = names[0];
    const char* before = view.data();
    names.push_back("MSFT");  // exceeds capacity 1: reallocation moves the strings
    const char* after = names[0].data();
    std::cout << "view still points at element 0's characters: " << (before == after ? "yes" : "no") << "\n";

    // The safe pattern for this problem: build ALL the strings first (or keep them in a deque / a reserved vector), then take views.
    std::vector<std::string> stable = {"AAPL", "MSFT", "GOOG"};
    std::vector<std::string_view> views(stable.begin(), stable.end());
    std::cout << "views taken after the vector is complete: " << views[0] << " " << views[1] << " " << views[2] << "\n";
}
