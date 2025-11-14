
import random
random.seed(42) 
from policy_test import get_win_percentages
from policy_random import Policy_Random
from Policy_GreedyButOptimistic import Policy_GreedyButOptimistic
print(get_win_percentages(1000, Policy_GreedyButOptimistic(), Policy_Random()))
