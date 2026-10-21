// Updating a std::set key: "erase the old key, insert the new one" is wrong when old == new, and allocation can throw
// between the two steps.  A node handle edits the key in place and never allocates.
#include <iostream>
#include <set>
#include <string>
#include <utility>

using Key = std::pair<long long, std::string>;  // (total, ticker)

int main() {
    std::set<Key> ranking = {{10, "A"}, {7, "B"}};

    // Wrong when the total does not change (a zero-notional trade): insert finds the key already there, then erase removes it.
    {
        auto wrong = ranking;
        const Key old_key{10, "A"}, new_key{10, "A"};
        wrong.insert(new_key);  // no-op: equal key exists
        wrong.erase(old_key);   // removes the only entry for A
        std::cout << "insert-then-erase with old == new keeps " << wrong.size() << " of 2 entries\n";
    }

    // Right: extract the node, change the key through the node handle, put it back.  No allocation, any old/new relation.
    {
        auto right = ranking;
        auto node = right.extract(Key{10, "A"});
        node.value().first = 10;  // unchanged total
        right.insert(std::move(node));
        auto node2 = right.extract(Key{10, "A"});
        node2.value().first = 3;  // changed total: A moves behind B
        right.insert(std::move(node2));
        std::cout << "extract / edit / insert keeps " << right.size() << " entries; smallest is (" << right.begin()->first << ", "
                  << right.begin()->second << ")\n";
    }
}
