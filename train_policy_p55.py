import random
from policy_random import Policy_Random
from policy_p55 import Policy_P55
from policy_test import get_win_percentages

BASE = {
    "win": 200.0, "capture": 50.0, "home_path": 30.0, "enter": 20.0,
    "to_safe": 10.0, "leave_safe": -8.0, "progress": 0.5, "risk": -5.0
}

def jitter(weights, scale=0.20):
    out = {}
    for k, v in weights.items():
        out[k] = v * (1.0 + random.uniform(-scale, scale)) if abs(v) >= 1.0 else v + random.uniform(-scale, scale)
    return out

def evaluate(w, n=400):
    return get_win_percentages(n, Policy_P55(weights=w), Policy_Random())[0]

if __name__ == "__main__":
    random.seed(42)
    best_w, best_score = BASE.copy(), evaluate(BASE, n=200)
    for it in range(20):
        cand = jitter(best_w, 0.20)
        score = evaluate(cand, n=400 if it > 10 else 200)
        if score > best_score:
            best_w, best_score = cand, score
            print(f"[iter {it}] best={best_score:.2f}%  {best_w}")
    print("FINAL:", best_score, best_w)
