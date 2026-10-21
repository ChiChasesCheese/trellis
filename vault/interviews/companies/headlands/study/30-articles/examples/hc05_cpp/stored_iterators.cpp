// Which containers keep an iterator valid while OTHER elements come and go -- the property the id index relies on.
#include <iostream>
#include <list>
#include <map>
#include <vector>

int main() {
    // std::list: an iterator stays valid until its own element is erased.  splice moves the node without invalidating it.
    std::list<int> queue{10, 20, 30};
    auto second = std::next(queue.begin());                 // points at 20
    queue.push_back(40);
    queue.erase(queue.begin());                             // erase 10
    queue.splice(queue.end(), queue, second);               // move 20 to the back: same node, same iterator
    std::cout << "list after splice:";
    for (int x : queue) std::cout << ' ' << x;
    std::cout << "   *second = " << *second << "\n";

    // std::map: same guarantee for its nodes.
    std::map<long long, int> ladder{{100, 1}, {101, 2}, {102, 3}};
    auto level = ladder.find(101);
    ladder.erase(100);
    ladder.emplace(99, 0);
    std::cout << "map iterator still sees " << level->first << " -> " << level->second << "\n";

    // std::vector: any growth may move every element, so iterators and references become dangling.
    std::vector<int> v{1, 2, 3};
    const int* before = &v[0];
    v.reserve(1000);                                        // reallocates
    std::cout << "vector element moved: " << std::boolalpha << (before != &v[0]) << "\n";

    // A copy of a structure that stores iterators still holds iterators into the ORIGINAL.
    struct Indexed {
        std::list<int> items;
        std::list<int>::iterator first;
    };
    Indexed a{{1, 2, 3}, {}};
    a.first = a.items.begin();
    Indexed b = a;                                          // copies the list, copies the iterator value
    std::cout << "copy's iterator points into the copy's list: " << (&*b.first == &*b.items.begin()) << "\n";
}
