from tasks3 import inc

def test_inc_zero():
    assert inc(0) == 1

def test_inc_negative():
    assert inc(-3) == -2
