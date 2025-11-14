#it gives 90 accuracy
# import random
# from policy_random import Policy_Random
# from Policy_GreedyButOptimistic import Policy_GreedyButOptimistic
# from policy_test import get_win_percentages

# BASE = {
#     "win": 200.0, "capture": 50.0, "home_path": 30.0, "enter": 20.0,
#     "to_safe": 10.0, "leave_safe": -8.0, "progress": 0.5, "risk_prob": -5.0
# }

# def jitter(weights, scale=0.20):
#     out = {}
#     for k, v in weights.items():
#         out[k] = v * (1.0 + random.uniform(-scale, scale)) if abs(v) >= 1.0 else v + random.uniform(-scale, scale)
#     return out

# def evaluate(w, n=400):
#     return get_win_percentages(n, Policy_GreedyButOptimistic(weights=w), Policy_Random())[0]

# if __name__ == "__main__":
#     random.seed(42)
#     best_w, best_score = BASE.copy(), evaluate(BASE, n=200)
#     for it in range(20):
#         cand = jitter(best_w, 0.20)
#         score = evaluate(cand, n=400 if it > 10 else 200)
#         if score > best_score:
#             best_w, best_score = cand, score
#             print(f"[iter {it}] best={best_score:.2f}%  {best_w}")
#     print("FINAL:", best_score, best_w)
#     with open("best_weights_p55.txt", "w") as f:
#         f.write(str(best_w))
#     print("Best weights saved to best_weights_p55.txt")



#it gives 91 accuracy
# import random
# from policy_random import Policy_Random
# from Policy_GreedyButOptimistic import Policy_GreedyButOptimistic
# from policy_test import get_win_percentages

# BASE = {
#     "win": 250.0,
#     "capture": 70.0,
#     "home_path": 35.0,
#     "enter": 25.0,
#     "to_safe": 14.0,
#     "leave_safe": -9.0,
#     "progress": 0.55,
#     "risk_prob": -65.0
# }

# def jitter(weights, scale=0.20):
#     """Return a slightly perturbed version of the weights."""
#     out = {}
#     for k, v in weights.items():
#         if abs(v) >= 1.0:
#             out[k] = v * (1.0 + random.uniform(-scale, scale))
#         else:
#             out[k] = v + random.uniform(-scale, scale)
#     return out

# def evaluate(w, n=400):
#     return get_win_percentages(n, Policy_GreedyButOptimistic(weights=w), Policy_Random())[0]

# if __name__ == "__main__":
#     # Keep seed so that your experiments are reproducible
#     random.seed(42)

#     # Initial evaluation
#     best_w = BASE.copy()
#     best_score = evaluate(best_w, n=500)
#     print(f"Initial score: {best_score:.2f}% with weights {best_w}")

#     for it in range(20):
#         # Large jitter at start, smaller later for fine-tuning
#         if it < 5:
#             scale = 0.30
#         elif it < 12:
#             scale = 0.20
#         else:
#             scale = 0.10

#         cand = jitter(best_w, scale)
#         games = 1000 if it > 10 else 500
#         score = evaluate(cand, n=games)

#         # Only accept clearly better candidates (margin = 1%)
#         if score > best_score + 1.0:
#             best_w, best_score = cand, score
#             print(f"[iter {it}] New best: {best_score:.2f}% with {best_w}")

#     print("FINAL:", best_score, best_w)
#     with open("best_weights_p55.txt", "w") as f:
#         f.write(str(best_w))
#     print("Best weights saved to best_weights_p55.txt")



#it gives 92 accuracy
import random
from policy_random import Policy_Random
from Policy_GreedyButOptimistic import Policy_GreedyButOptimistic
from policy_test import get_win_percentages

BASE = {
    "win": 250.0,
    "capture": 70.0,
    "home_path": 35.0,
    "enter": 25.0,
    "to_safe": 14.0,
    "leave_safe": -9.0,
    "progress": 0.55,
    "risk_prob": -65.0,
}

def jitter(weights, scale=0.10):
    """Small perturbations only (±10%) for stable tuning."""
    out = {}
    for k, v in weights.items():
        if abs(v) >= 1.0:
            out[k] = v * (1.0 + random.uniform(-scale, scale))
        else:
            out[k] = v + random.uniform(-scale, scale)
    return out

def evaluate(weights, n_games=300):
    """Evaluate using a moderate number of games for more stable readout."""
    return get_win_percentages(n_games, Policy_GreedyButOptimistic(weights=weights), Policy_Random())[0]

if __name__ == "__main__":
    random.seed(42)

    best_w = BASE.copy()
    best_score = evaluate(best_w, n_games=300)
    print(f"Initial score: {best_score:.2f}% with weights {best_w}")

    for it in range(15):
        cand = jitter(best_w, scale=0.10)
        score = evaluate(cand, n_games=300)

        if score > best_score + 0.5:  
            best_w, best_score = cand, score
            print(f"[iter {it}] New best: {best_score:.2f}% with {best_w}")

    print("FINAL:", best_score, best_w)
    with open("best_weights_p55.txt", "w") as f:
        f.write(str(best_w))
    print("Best weights saved to best_weights_p55.txt")
