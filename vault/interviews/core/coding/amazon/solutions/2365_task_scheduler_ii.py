"""LC 2365 Task Scheduler II -- tasks in order; remember the last day each type ran; wait only if the cooldown is not over."""
from random import Random

# --- solution ---
def task_scheduler_ii(tasks, space):
    last = {}                                             # task type -> day it last ran
    day = 0
    for t in tasks:
        day += 1                                          # at least one day passes per task
        if t in last:
            day = max(day, last[t] + space + 1)           # need a gap of `space` days between equal types
        last[t] = day
    return day
# --- end ---

def _brute(tasks, space):
    day, i, history = 0, 0, []                            # history[d] = type run on day d (None = break)
    while i < len(tasks):
        day += 1
        recent = history[max(0, day - 1 - space):]
        if tasks[i] in recent:
            history.append(None)
        else:
            history.append(tasks[i])
            i += 1
    return day

if __name__ == "__main__":
    assert task_scheduler_ii([1, 2, 1, 2, 3, 1], 3) == 9
    assert task_scheduler_ii([5, 8, 8, 5], 2) == 6
    assert task_scheduler_ii([7], 1) == 1
    rng = Random(2365)
    for _ in range(500):
        tasks = [rng.randint(1, 4) for _ in range(rng.randint(1, 10))]
        sp = rng.randint(1, len(tasks))
        assert task_scheduler_ii(tasks, sp) == _brute(tasks, sp), (tasks, sp)
    print("ok 2365_task_scheduler_ii")
