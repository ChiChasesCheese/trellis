"""Which tutorial recipes reproduce the game's Initial Test ($3,828, 168 sandwiches)?

The screenshots show rates, prices and times but not the recipes, so try every quantity 1..3 on every edge and keep
the ones the simulator matches exactly. The sandwich price $10 is derived: 3,828 - 3,000 + 24 x 35.50 = 1,680 = 168 x 10.
    python3 calibrate_tutorial.py
"""
import itertools

from factory import given_setting, prepare, simulate


def tutorial(q):
    b_d, j_s, j_w, s_b, s_p, s_j = q
    return prepare({
        "hours": 24, "start_cash": 3000,
        "nodes": {
            "peanut_butter": {"kind": "supplier", "row": 0, "rate": 15, "unit_cost": 0.5},
            "dough": {"kind": "supplier", "row": 1, "rate": 24, "unit_cost": 0.5},
            "sugar": {"kind": "supplier", "row": 2, "rate": 30, "unit_cost": 0.2},
            "strawberry": {"kind": "supplier", "row": 3, "rate": 20, "unit_cost": 0.5},
            "bread": {"kind": "maker", "row": 1, "rate": 10, "options": [{"name": "Crusty Bread", "inputs": {"dough": b_d}}]},
            "jam": {"kind": "maker", "row": 3, "rate": 20,
                    "options": [{"name": "Jam", "inputs": {"sugar": j_s, "strawberry": j_w}, "period": 2}]},
            "sandwich": {"kind": "seller", "row": 1, "rate": 12, "options": [
                {"name": "Sandwich", "inputs": {"bread": s_b, "peanut_butter": s_p, "jam": s_j}, "price": 10}]},
        },
    })


if __name__ == "__main__":
    hits = []
    for q in itertools.product((1, 2, 3), repeat=6):
        lv = tutorial(q)
        trace = []
        money = simulate(lv, given_setting(lv), trace)
        if abs(money - 3828) < 1e-6 and trace[-1]["sold"].get("Sandwich") == 168:
            hits.append(q)
    print("bread<-dough, jam<-sugar, jam<-strawberry, sandwich<-bread, sandwich<-pb, sandwich<-jam")
    for q in hits:
        print(q)
    print(len(hits), "of 729 match")
