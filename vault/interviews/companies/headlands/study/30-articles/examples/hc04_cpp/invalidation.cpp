// push_back may reallocate: every pointer, reference and iterator into the vector dies.  Index, or copy first.
#include <iostream>
#include <vector>

struct Node { long long val; int parent; int depth; };

int add_child_buggy(std::vector<Node>& nodes, int p, long long x) {
    const Node& parent = nodes[p];                       // reference into the vector
    nodes.push_back(Node{x, p, 0});                      // may reallocate: `parent` now dangles
    nodes.back().depth = parent.depth + 1;               // use after free (ASan: heap-use-after-free)
    return static_cast<int>(nodes.size() - 1);
}

int add_child(std::vector<Node>& nodes, int p, long long x) {
    const Node parent = nodes[p];                        // copy the 16 bytes you need BEFORE growing
    nodes.push_back(Node{x, p, parent.depth + 1});
    return static_cast<int>(nodes.size() - 1);
}

int main() {
    std::vector<Node> nodes{Node{0, 0, 0}};
    int last = 0;
    for (int i = 1; i <= 100000; ++i) last = add_child(nodes, last, i);
    std::cout << "depth of last node: " << nodes[last].depth << "\n";
    if (false) add_child_buggy(nodes, last, 0);   // call it with a full vector and ASan reports heap-use-after-free
}
