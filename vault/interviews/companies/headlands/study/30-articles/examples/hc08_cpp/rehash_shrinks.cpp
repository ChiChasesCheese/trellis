// unordered_map keeps its bucket array after erase; only rehash gives it back.
#include <iostream>
#include <unordered_map>

int main() {
    std::unordered_map<long long, int> m;
    m.reserve(100'000);
    for (long long i = 0; i < 100'000; ++i) m.emplace(i, 0);
    for (long long i = 10; i < 100'000; ++i) m.erase(i);
    std::cout << "after erasing down to " << m.size() << " keys: bucket_count = " << m.bucket_count() << "\n";
    m.rehash(64);
    std::cout << "after rehash(64):               bucket_count = " << m.bucket_count() << "\n";
}
