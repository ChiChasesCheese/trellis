// map[key] on a missing key INSERTS a default element.  Lookups must use find / contains / at.
#include <iostream>
#include <unordered_map>

int main() {
    std::unordered_map<long long, int> index_of;
    index_of[7] = 3;
    const int wrong = index_of[99];            // "lookup" of an unknown id
    std::cout << "operator[] of unknown id returned " << wrong << ", size is now " << index_of.size() << "\n";
    std::cout << "contains(99) is now " << std::boolalpha << index_of.contains(99) << "   <- the unknown id became a live one\n";

    std::unordered_map<long long, int> clean{{7, 3}};
    if (const auto it = clean.find(99); it == clean.end()) std::cout << "find(99): not found, size still " << clean.size() << "\n";
}
