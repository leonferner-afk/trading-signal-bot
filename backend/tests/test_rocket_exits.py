import numpy as np

from app.rockets import trailing_exit


def test_take_profit_sells_at_next_open_after_the_target_close():
    opens = np.array([10, 10, 11, 12, 14, 13], float)
    closes = np.array([10, 11, 12, 13.5, 13, 13], float)
    # Fill at opens[1]=10; +30% target -> close >= 13 first at index 3 -> sell at opens[4].
    assert trailing_exit(opens, closes, 0, trail=0.25, max_hold=60, take_profit=0.30) == (4, 14.0, "target")
    # Without a target the 25% trail never triggers here, so the exit isn't known yet.
    assert trailing_exit(opens, closes, 0, trail=0.25, max_hold=60) is None


def test_tighter_trail_exits_earlier():
    opens = np.array([10, 10, 10, 10, 10, 10], float)
    closes = np.array([10, 12, 10.7, 9, 9, 9], float)
    assert trailing_exit(opens, closes, 0, trail=0.10, max_hold=60)[2] == "trail"     # 10.7 <= 12*0.9
    assert trailing_exit(opens, closes, 0, trail=0.10, max_hold=60)[0] == 3
