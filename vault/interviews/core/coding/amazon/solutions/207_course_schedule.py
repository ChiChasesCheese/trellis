"""LC 207 Course Schedule -- Kahn's topological sort: can every course be taken (no cycle)? Time O(V+E)."""
from collections import deque

# --- solution ---
def can_finish(num_courses, prerequisites):
    graph = [[] for _ in range(num_courses)]
    indegree = [0] * num_courses
    for course, pre in prerequisites:            # edge pre -> course
        graph[pre].append(course)
        indegree[course] += 1
    queue = deque(c for c in range(num_courses) if indegree[c] == 0)
    taken = 0
    while queue:
        c = queue.popleft()
        taken += 1
        for nxt in graph[c]:
            indegree[nxt] -= 1
            if indegree[nxt] == 0:               # all of nxt's prerequisites are done
                queue.append(nxt)
    return taken == num_courses                  # leftover nodes sit on a cycle


def find_order(num_courses, prerequisites):      # LC 210: same loop, keep the order
    graph = [[] for _ in range(num_courses)]
    indegree = [0] * num_courses
    for course, pre in prerequisites:
        graph[pre].append(course)
        indegree[course] += 1
    queue = deque(c for c in range(num_courses) if indegree[c] == 0)
    order = []
    while queue:
        c = queue.popleft()
        order.append(c)
        for nxt in graph[c]:
            indegree[nxt] -= 1
            if indegree[nxt] == 0:
                queue.append(nxt)
    return order if len(order) == num_courses else []
# --- end ---

if __name__ == "__main__":
    assert can_finish(2, [[1, 0]])
    assert not can_finish(2, [[1, 0], [0, 1]])
    assert can_finish(1, [])
    assert not can_finish(1, [[0, 0]])                         # self loop
    assert can_finish(4, [[1, 0], [2, 0], [3, 1], [3, 2]])     # diamond
    assert find_order(4, [[1, 0], [2, 0], [3, 1], [3, 2]])[0] == 0
    assert find_order(2, [[1, 0], [0, 1]]) == []
    print("ok 207_course_schedule")
