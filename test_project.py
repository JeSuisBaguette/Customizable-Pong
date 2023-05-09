import pytest
from project import instruction, validate


def test_instruction():
    assert instruction() == (
        "Press W/S to move the left-paddle up/down.\
\nPress Up-arrow/Down-arrow to move the right-paddle up/down.\
\nThe ball will start moving when the space key is pressed.\
\nYou can change the number of balls, ball-speed, or paddle-speed the game starts with in game parameters.\
\nYou can even change player names or the number of points required to win the game!\
\nIf you wish to skip all that, the game is also able to start with default parameters for all the above.\
\nFor your information, the default parameters are: ball-amount = 1, ball-speed = 5, paddle-speed = 7, target = 10"
    )
    with pytest.raises(TypeError):
        instruction(1)


def test_validate():
    assert validate(ball_amount="1") == True
    assert validate(ball_amount="0") == False
    assert validate(ball_speed="4") == True
    assert validate(ball_speed="10") == False
    assert validate(paddle_speed="15") == True
    assert validate(paddle_speed="-3") == False
    assert validate(end_score="94") == True
    assert validate(end_score="-1") == False