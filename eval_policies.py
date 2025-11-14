# from policy_test import get_win_percentages
# from policy_random import Policy_Random
# from policy_p55 import Policy_P55

# print("Evaluating 1000 games (alternating starts)…")
# print(get_win_percentages(1000, Policy_P55(), Policy_Random()))

import random
random.seed(42)    # choose any fixed int seed

from policy_test import get_win_percentages
from policy_random import Policy_Random
from policy_p55 import Policy_P55

print(get_win_percentages(1000, Policy_P55(), Policy_Random()))
