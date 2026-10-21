// C05: which operations keep references/iterators valid? Checked by comparing element addresses before and after.
#include <deque>
#include <iostream>
#include <list>
#include <map>
#include <unordered_map>
#include <vector>

template <class C>
bool same_address_after(C& c, auto op, auto get_ptr) {
    const void* before = get_ptr(c);
    op(c);
    return before == get_ptr(c);
}

int main() {
    std::cout << std::boolalpha;
    // [[snip:addr]]
    {
        std::vector<int> v{1, 2, 3};      // capacity == size: the next push_back must reallocate
        std::cout << "vector push_back at full capacity     : first element kept its address? "
                  << same_address_after(v, [](auto& c) { c.push_back(4); }, [](auto& c) { return &c.front(); }) << "\n";
        std::vector<int> r{1, 2, 3}; r.reserve(100);
        std::cout << "vector push_back with spare capacity  : first element kept its address? "
                  << same_address_after(r, [](auto& c) { c.push_back(4); }, [](auto& c) { return &c.front(); }) << "\n";
        std::deque<int> d{1, 2, 3};
        std::cout << "deque push_back x1000                 : first element kept its address? "
                  << same_address_after(d, [](auto& c) { for (int i = 0; i < 1000; ++i) c.push_back(i); }, [](auto& c) { return &c.front(); })
                  << "  (iterators ARE invalidated, references are not)\n";
        std::list<int> l{1, 2, 3};
        std::cout << "list push_back x1000                  : first element kept its address? "
                  << same_address_after(l, [](auto& c) { for (int i = 0; i < 1000; ++i) c.push_back(i); }, [](auto& c) { return &c.front(); }) << "\n";
        std::map<int, int> m{{1, 1}, {2, 2}};
        std::cout << "map insert x1000                      : first element kept its address? "
                  << same_address_after(m, [](auto& c) { for (int i = 10; i < 1010; ++i) c[i] = i; }, [](auto& c) { return &c.begin()->second; }) << "\n";
        std::unordered_map<int, int> u{{1, 1}, {2, 2}};
        auto buckets0 = u.bucket_count();
        std::cout << "unordered_map insert x1000 (rehash)   : first element kept its address? "
                  << same_address_after(u, [](auto& c) { for (int i = 10; i < 1010; ++i) c[i] = i; }, [](auto& c) { return &c.find(1)->second; })
                  << "  (bucket_count " << buckets0 << " -> " << u.bucket_count() << ", iterators invalidated by rehash, references not)\n";
    }
    // [[/snip]]

    // [[snip:erase]]
    {
        std::vector<int> v{1, 2, 3, 4, 5, 6};
        for (auto it = v.begin(); it != v.end();) {     // the correct erase-while-iterating loop
            if (*it % 2 == 0) it = v.erase(it);         // erase returns the NEXT valid iterator
            else ++it;
        }
        std::cout << "vector erase loop, odds left:";
        for (int x : v) std::cout << " " << x;
        std::cout << "\n";

        std::map<int, int> m{{1, 10}, {2, 20}, {3, 30}, {4, 40}};
        for (auto it = m.begin(); it != m.end();) {
            if (it->first % 2 == 0) it = m.erase(it);   // node containers: only the erased element's iterator dies
            else ++it;
        }
        std::cout << "map erase loop, keys left:";
        for (auto& [k, val] : m) std::cout << " " << k << "=" << val;
        std::cout << "\n";
    }
    // [[/snip]]
}
