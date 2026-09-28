"""Render a plan into viewer_template.html: python3 export_view.py best_plan.json out.html"""
import json
import os
import sys

from sim import BOARD, COST, Game, Rules

here = os.path.dirname(os.path.abspath(__file__))


def export(plan_path, out_path, subtitle=None):
    data = json.load(open(plan_path))
    plan = {tuple(k): v for k, v in data["plan"]}
    game = Game(BOARD, Rules())
    state, trace, events, arrive = game.initial, [], [], {}

    def snap(s):
        return {"cats": [[k[0], k[1], k[2], k[3], k[4], k[7]] for k in s[1]], "floors": list(s[2]), "money": s[4]}

    trace.append(snap(state))
    for _ in range(game.rules.turns):
        turn = state[0] + 1
        state = game.step(state, lambda color, fid, m: events.append([turn, color, *fid]) or plan.get(fid))
        for k in state[1]:
            if k[7] == "bed" and k[0] not in arrive:
                arrive[k[0]] = turn
        trace.append(snap(state))
    order = {c: i + 1 for i, c in enumerate(sorted(arrive, key=lambda c: (arrive[c], trace[arrive[c] - 1]["cats"][
        [k[0] for k in trace[0]["cats"]].index(c)][4])))}
    score = Game.score(state)
    assert score == data["score"], (score, data["score"])
    payload = {
        "board": BOARD,
        "buildings": [[r, c, kind] for (r, c), kind in game.buildings],
        "plan": [[r, c, f, v] for (r, c, f), v in sorted(plan.items())],
        "events": events, "trace": trace, "arrive": arrive, "order": order,
        "score": score, "spent": sum(COST[v] for v in plan.values()),
        "subtitle": subtitle or "按回合查看三只猫的路线。滑到任意回合，棋盘显示那一回合结束时的状态。",
    }
    html = open(os.path.join(here, "viewer_template.html")).read().replace("/*DATA*/null", json.dumps(payload, ensure_ascii=False))
    open(out_path, "w").write(html)
    return score


if __name__ == "__main__":
    print(export(sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else None))
