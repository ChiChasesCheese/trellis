"""LC 721 Accounts Merge -- union accounts that share an email; group emails by root. ~O(E * alpha * log E) with the sort."""
from collections import defaultdict
from random import Random

# --- solution ---
def accounts_merge(accounts):
    parent = list(range(len(accounts)))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    owner = {}                                         # email -> index of the first account that listed it
    for i, acc in enumerate(accounts):
        for email in acc[1:]:
            if email in owner:
                parent[find(i)] = find(owner[email])   # same email => same person
            else:
                owner[email] = i
    groups = defaultdict(set)
    for email, i in owner.items():
        groups[find(i)].add(email)
    return [[accounts[root][0]] + sorted(emails) for root, emails in groups.items()]
# --- end ---

def _brute(accounts):
    adj = defaultdict(set)
    name = {}
    for acc in accounts:
        for e in acc[1:]:
            name[e] = acc[0]
            adj[e].update(acc[1:])
    seen, out = set(), []
    for e in name:
        if e in seen:
            continue
        comp, stack = set(), [e]
        seen.add(e)
        while stack:
            u = stack.pop()
            comp.add(u)
            for v in adj[u]:
                if v not in seen:
                    seen.add(v)
                    stack.append(v)
        out.append([name[e]] + sorted(comp))
    return out

if __name__ == "__main__":
    accts = [["John", "johnsmith@mail.com", "john_newyork@mail.com"], ["John", "johnsmith@mail.com", "john00@mail.com"],
             ["Mary", "mary@mail.com"], ["John", "johnnybravo@mail.com"]]
    got = accounts_merge(accts)
    assert sorted(got) == sorted([["John", "john00@mail.com", "john_newyork@mail.com", "johnsmith@mail.com"],
                                  ["Mary", "mary@mail.com"], ["John", "johnnybravo@mail.com"]])
    assert accounts_merge([]) == []
    rng = Random(53)
    for _ in range(400):
        accts = []
        for _ in range(rng.randint(1, 7)):
            person = rng.randint(0, 2)                  # emails are namespaced by person, so merged groups share one name
            accts.append(["P%d" % person] + ["p%de%d" % (person, k) for k in rng.sample(range(4), rng.randint(1, 3))])
        got, want = accounts_merge(accts), _brute(accts)
        assert sorted(map(tuple, got)) == sorted(map(tuple, want)), accts
    print("ok 721_accounts_merge")
