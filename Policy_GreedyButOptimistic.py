
STARTING = -1
DESTINATION = 56
SAFE_SQUARES = [0, 8, 13, 21, 25, 26, 34, 39, 47, 51, 52, 53, 54, 55, 56]
P_HAS_D = {1: 43/216, 2: 43/216, 3: 43/216, 4: 43/216, 5: 43/216, 6: 35/216}

def _convert_for_opponent(pos: int) -> int:
    if pos <= 0 or pos > 50 or pos == 25:
        return -2
    return pos + 26 if pos <= 24 else pos - 26

def _is_safe(pos: int) -> bool:
    return pos in SAFE_SQUARES

def _simulate_newpos(cur: int, dice: int):
    if cur == STARTING:
        return 0 if dice == 6 else None
    nxt = cur + dice
    return nxt if nxt <= DESTINATION else None

def _prob_capture_next_turn(newpos: int, opp_positions: list[int]) -> float:
    if _is_safe(newpos):
        return 0.0
    opp_view = _convert_for_opponent(newpos)
    if opp_view == -2 or opp_view in SAFE_SQUARES:
        return 0.0

    probs = []
    for p in opp_positions:
        if p == STARTING or p in SAFE_SQUARES:
            continue
        delta = opp_view - p
        if 1 <= delta <= 6:
            probs.append(P_HAS_D[delta])

    if not probs:
        return 0.0

    one_minus = 1.0
    for pr in probs:
        one_minus *= (1.0 - pr)
    return 1.0 - one_minus

class Policy_GreedyButOptimistic:
    def __init__(self, weights=None):
        # Defaults tuned to be aggressive but safe. You can re-tune with your trainer.
        # self.w = {
        #     "win": 250.0,
        #     "capture": 70.0,
        #     "home_path": 35.0,
        #     "enter": 25.0,
        #     "to_safe": 14.0,
        #     "leave_safe": -9.0,
        #     "progress": 0.55,
        #     "risk_prob": -65.0,   
        # }
        self.w = {'win': 250.73362524085192, 'capture': 71.23368106429712, 'home_path': 34.15364631867389, 'enter': 27.01776903313076, 'to_safe': 12.760536139947293, 'leave_safe': -8.584200788411554, 'progress': 0.5219101253152619, 'risk_prob': -63.64405793192719}
        if weights:
            self.w.update(weights)

        self._memo = {}

    def _step_reward_and_apply(self, me_pos, opp_pos, gi, dice):
        me_new = list(me_pos)
        opp_new = list(opp_pos)
        cur = me_new[gi]
        newpos = _simulate_newpos(cur, dice)
        if newpos is None:
            return None, None, float("-inf")

        score = 0.0
        if newpos == DESTINATION:
            score += self.w["win"]
        newpos_for_opp = _convert_for_opponent(newpos)
        if newpos_for_opp != -2 and (newpos_for_opp in opp_new) and not _is_safe(newpos_for_opp):
            score += self.w["capture"]
            hit_idx = opp_new.index(newpos_for_opp)
            opp_new[hit_idx] = STARTING

        if cur == STARTING and dice == 6:
            score += self.w["enter"]

        if not _is_safe(cur) and _is_safe(newpos):
            score += self.w["to_safe"]
        if _is_safe(cur) and not _is_safe(newpos):
            score += self.w["leave_safe"]

        if 51 <= newpos <= 56:
            score += self.w["home_path"]
        base = 0 if cur == STARTING else cur
        score += self.w["progress"] * (newpos - base)

        risk = _prob_capture_next_turn(newpos, opp_pos)
        score += self.w["risk_prob"] * risk

        me_new[gi] = newpos
        return me_new, opp_new, score

    def _legal_turn_actions(self, me_pos, dice_list):
        acts = []
        for di, d in enumerate(dice_list):
            for gi, cur in enumerate(me_pos):
                if _simulate_newpos(cur, d) is not None:
                    acts.append((di, gi))
        return acts

    def _turn_value(self, me_pos, opp_pos, dice_list):
        if not dice_list:
            return 0.0
        best = 0.0
        for di, gi in self._legal_turn_actions(me_pos, dice_list):
            d = dice_list[di]
            me2, opp2, r = self._step_reward_and_apply(me_pos, opp_pos, gi, d)
            if me2 is None:
                continue
            rem = dice_list[:di] + dice_list[di+1:]
            val = r + self._turn_value(me2, opp2, rem)
            if val > best:
                best = val
        return best

    def get_action(self, state, action_space):
        if not action_space:
            return None

        gotis_red, gotis_yellow, roll, terminated, player_turn = state
        me = gotis_red if player_turn == 0 else gotis_yellow
        opp = gotis_yellow if player_turn == 0 else gotis_red
        me_pos  = [g.position for g in me.gotis]
        opp_pos = [g.position for g in opp.gotis]

        best_action, best_val = None, float("-inf")
        for (di, gi) in action_space:
            d = roll[di]
            me2, opp2, r = self._step_reward_and_apply(me_pos, opp_pos, gi, d)
            if me2 is None:
                continue
            rem = roll[:di] + roll[di+1:]
            total = r + self._turn_value(me2, opp2, rem)
            if total > best_val:
                best_val = total
                best_action = (di, gi)
        return best_action

